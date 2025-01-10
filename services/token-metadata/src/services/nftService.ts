import { createUmi } from '@metaplex-foundation/umi-bundle-defaults'
import { createNft, mplTokenMetadata } from '@metaplex-foundation/mpl-token-metadata'
import { fetchAllDigitalAssetWithTokenByOwner  } from '@metaplex-foundation/mpl-token-metadata'
import { Option } from '@metaplex-foundation/umi'
import { isSome } from '@metaplex-foundation/umi-options'
import { 
  percentAmount, 
  keypairIdentity, 
  generateSigner,
  createSignerFromKeypair,
  publicKey,
  TransactionBuilder,
  Umi,
  Transaction,
} from '@metaplex-foundation/umi'
import { 
  setComputeUnitLimit,
  setComputeUnitPrice,
} from "@metaplex-foundation/mpl-toolbox"
import { Keypair } from "@solana/web3.js"
import { base58, base64 } from "@metaplex-foundation/umi/serializers"
import bs58 from "bs58"
import { config } from '../config/config'
import { CreateNFTRequest, TokenMetadata } from '../types'
import logger from '../utils/logger'

export class NFTService {
  private umi: Umi;
  private signer;

  constructor() {
    logger.info('Initializing NFTService...')
    
    try {
      this.umi = createUmi(config.rpcEndpoint)
      logger.debug('Created Umi instance', {
        rpcEndpoint: config.rpcEndpoint
      })
      
      const secretKey = bs58.decode(config.walletPrivateKey)
      const keypair = Keypair.fromSecretKey(secretKey)
      logger.info('Wallet keypair created', {
        publicKey: keypair.publicKey.toBase58()
      })

      this.signer = createSignerFromKeypair(this.umi, {
        publicKey: publicKey(keypair.publicKey.toBase58()),
        secretKey: keypair.secretKey,
      })
      
      this.umi = this.umi
        .use(mplTokenMetadata())
        .use(keypairIdentity(this.signer))
      
      logger.info('NFTService initialized successfully')
      
    } catch (error: any) {
      logger.error('Failed to initialize NFTService', {
        error: {
          message: error.message,
          stack: error.stack
        }
      })
      throw error
    }
  }

  private async getPriorityFee(
    transaction: TransactionBuilder
  ): Promise<number> {
    try {
      // Get unique writable accounts
      const distinctPublicKeys = new Set<string>();
      transaction.items.forEach(item => {
        item.instruction.keys.forEach(key => {
          if (key.isWritable) {
            distinctPublicKeys.add(key.pubkey.toString());
          }
        });
      });

      // Query recent prioritization fees
      const response = await fetch(this.umi.rpc.getEndpoint(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          jsonrpc: "2.0",
          id: 1,
          method: "getRecentPrioritizationFees",
          params: [Array.from(distinctPublicKeys)],
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch priority fees: ${response.status}`);
      }

      const data = await response.json() as {
        result: { prioritizationFee: number; slot: number; }[];
      };

      logger.info('getPriorityFee data:', data)

      // Calculate average of top 100 fees
      const fees = data.result?.map(entry => entry.prioritizationFee) || [];
      const topFees = fees.sort((a, b) => b - a).slice(0, 100);
      const averageFee = topFees.length > 0 
        ? Math.ceil(topFees.reduce((sum, fee) => sum + fee, 0) / topFees.length)
        : 50000; // Default fallback

      logger.debug('Calculated priority fee', { averageFee });
      return averageFee;

    } catch (error) {
      logger.warn('Failed to calculate priority fee, using default', { error });
      return 50000; // Fallback to default fee
    }
  }

  async createNFT(params: CreateNFTRequest): Promise<{ signature: string; nft_address: string }> {
    const operationId = Date.now().toString()
    
    logger.info('Starting NFT creation', {
      operationId,
      params: {
        name: params.name,
        metadata_url: params.metadata_url,
        creator_id: params.creator_id
      }
    })

    try {      
      // Generate mint signer
      const mint = generateSigner(this.umi)
      logger.info('Generated new mint signer', {
        operationId,
        mintAddress: mint.publicKey,
        payerAddress: this.signer.publicKey
      })

      // Calculate optimal priority fee first to save time
      logger.info('Calculating priority fee...')
      const priorityFee = Math.max(100000, await this.getPriorityFee(
        createNft(this.umi, {
          mint,
          name: params.name,
          uri: params.metadata_url,
          sellerFeeBasisPoints: percentAmount(0),
          payer: this.signer,
          authority: this.signer,
          creators: [{
            address: publicKey(params.creator_id),
            verified: false,
            share: 100
          }]
        })
      ))
      logger.info('Priority fee calculated', { priorityFee })

      // Function to create and send transaction with fresh blockhash
      const executeTransaction = async (retryCount = 0): Promise<{ signature: string; nft_address: string }> => {
        const maxRetries = 3;
        try {
          // Get fresh blockhash
          const latestBlockhash = await this.umi.rpc.getLatestBlockhash();
          logger.info('Got fresh blockhash', {
            operationId,
            blockhash: latestBlockhash.blockhash,
            lastValidBlockHeight: latestBlockhash.lastValidBlockHeight,
            retryCount
          });

          // Build transaction with fresh blockhash
          const transaction = createNft(this.umi, {
            mint,
            name: params.name,
            uri: params.metadata_url,
            sellerFeeBasisPoints: percentAmount(0),
            payer: this.signer,
            authority: this.signer,
            creators: [{
              address: publicKey(params.creator_id),
              verified: false,
              share: 100
            }],
            collection: null,
            uses: null,
            isMutable: false
          })
            .prepend(setComputeUnitPrice(this.umi, { 
              microLamports: retryCount > 0 ? priorityFee * (retryCount + 1) : priorityFee 
            }))
            .prepend(setComputeUnitLimit(this.umi, { units: 800_000 }))
            .setBlockhash(latestBlockhash.blockhash);

          logger.info('Sending transaction', {
            operationId,
            retryCount,
            priorityFee: retryCount > 0 ? priorityFee * (retryCount + 1) : priorityFee,
            blockhash: latestBlockhash.blockhash
          });

          // Send and confirm with shorter timeout
          const { signature } = await transaction.sendAndConfirm(this.umi, {
            send: {
              skipPreflight: true,
            },
            confirm: {
              commitment: 'confirmed',
            }
          });

          return {
            signature: bs58.encode(signature),
            nft_address: mint.publicKey.toString()
          };
        } catch (error: any) {
          if (retryCount < maxRetries && 
              (error.message.includes('block height exceeded') || 
               error.message.includes('timeout'))) {
            logger.warn(`Transaction attempt ${retryCount + 1} failed, retrying...`, {
              operationId,
              error: error.message,
              retryCount
            });
            // Exponential backoff
            await new Promise(resolve => setTimeout(resolve, Math.pow(2, retryCount) * 1000));
            return executeTransaction(retryCount + 1);
          }
          throw error;
        }
      };

      // Execute transaction with retry logic
      const result = await executeTransaction();

      logger.info('NFT created successfully', {
        operationId,
        signature: result.signature,
        nftAddress: result.nft_address,
        name: params.name
      });

      return result;

    } catch (error: any) {
      logger.error('Failed to create NFT', {
        operationId,
        error: {
          message: error.message,
          stack: error.stack,
          name: error.name,
          code: error.code,
          logs: error.logs || [],
        }
      })
      throw error
    }
  }

  async fetchByOwner(owner: string): Promise<TokenMetadata[]> {
    try {
      const ownerKey = publicKey(owner)
      
      logger.info('Fetching digital assets by owner', {
        owner: ownerKey.toString()
      })
      
      const assets = await fetchAllDigitalAssetWithTokenByOwner(this.umi, ownerKey)
      
      const tokens: TokenMetadata[] = assets.map(asset => ({
        address: asset.publicKey.toString(),
        mint: asset.mint.publicKey.toString(),
        metadata: {
          name: asset.metadata.name,
          uri: asset.metadata.uri,
          symbol: asset.metadata.symbol,
          sellerFeeBasisPoints: asset.metadata.sellerFeeBasisPoints,
          updateAuthority: asset.metadata.updateAuthority.toString(),
          creators: isSome(asset.metadata.creators)
          ? asset.metadata.creators.value.map(c => ({
              address: c.address.toString(),
              verified: c.verified,
              share: c.share
            }))
          : undefined,
          primarySaleHappened: asset.metadata.primarySaleHappened,
          isMutable: asset.metadata.isMutable,
          tokenStandard: isSome(asset.metadata.tokenStandard) 
            ? asset.metadata.tokenStandard.value.toString()
            : undefined,
          collection: isSome(asset.metadata.collection)
            ? {
                verified: asset.metadata.collection.value.verified,
                address: asset.metadata.collection.value.key.toString()
              }
            : null,
          editionNonce: isSome(asset.metadata.editionNonce)
            ? asset.metadata.editionNonce.value
            : undefined
        },
        edition: asset.edition ? {
          isOriginal: asset.edition.isOriginal,
          ...(asset.edition.isOriginal && {
            maxSupply: Number(asset.edition.maxSupply),
            supply: Number(asset.edition.supply)
          })
        } : undefined,
        tokenAccount: asset.token?.mint.toString() || '',
        balance: Number(asset.token?.amount || 0)
      }))
  
      logger.info('Successfully fetched digital assets', {
        owner: ownerKey.toString(),
        tokens: tokens
      })
  
      return tokens
    } catch (error) {
      logger.error('Failed to fetch tokens by owner', { 
        owner,
        error: error instanceof Error ? error.message : 'Unknown error'
      })
      throw error
    }
  }

}