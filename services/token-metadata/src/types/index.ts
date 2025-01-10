export interface CreateNFTRequest {
  wallet_address: string
  name: string
  metadata_url: string
  creator_id: string
}

export interface APIResponse<T = any> {
  success: boolean
  data: T | null
  error: {
    code: string
    message: string
  } | null
}

export interface TokenMetadata {
  address: string          // The metadata account address
  mint: string            // Mint address
  metadata: {
    name: string
    uri: string
    symbol: string
    sellerFeeBasisPoints: number
    updateAuthority: string
    creators?: Array<{
      address: string
      verified: boolean
      share: number
    }>
    primarySaleHappened: boolean
    isMutable: boolean
    tokenStandard?: string
    collection?: {
      verified: boolean
      address: string
    } | null
    editionNonce?: number
  }
  edition?: {
    isOriginal: boolean
    maxSupply?: number    // Only for master editions
    supply?: number       // Only for master editions
  }
  tokenAccount: string
  balance: number
}

export interface FetchByOwnerResponse {
  tokens: TokenMetadata[]
}
