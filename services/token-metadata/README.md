# Token Metadata Service

A REST API service that wraps functionality from @metaplex-foundation/mpl-token-metadata for creating NFTs on Solana.

## Features

- Create NFT with metadata
- Fetch NFTs by owner
- Transaction confirmation and retry mechanism
- Mainnet support
- RESTful API interface

## API

### Create NFT
```http
POST /api/nft/create
```

Parameters:
```typescript
{
  "wallet_address": string,  // Solana wallet address
  "name": string,           // NFT name
  "metadata_url": string,   // Metadata JSON URL
  "creator_id": string      // Creator wallet address
}
```

Response:
```typescript
{
  "success": boolean,
  "data": {
    "signature": string,    // Transaction signature
    "nft_address": string  // NFT token address
  } | null,
  "error": {
    "code": string,
    "message": string
  } | null
}
```

### Fetch NFTs by Owner
```http
GET /api/nft/owner/:owner
```

Parameters:
- `owner` (path parameter): Solana wallet address

Response:
```typescript
{
  "success": boolean,
  "data": {
    "tokens": Array<{
      "address": string,      // Metadata account address
      "mint": string,        // Mint address
      "metadata": {
        "name": string,
        "uri": string,
        "symbol": string,
        "sellerFeeBasisPoints": number,
        "updateAuthority": string,
        "creators": Array<{
          "address": string,
          "verified": boolean,
          "share": number
        }>,
        "primarySaleHappened": boolean,
        "isMutable": boolean,
        "tokenStandard": string,
        "collection": {
          "verified": boolean,
          "address": string
        } | null
      },
      "edition": {           // Optional edition info
        "isOriginal": boolean,
        "maxSupply": number, // Only for master editions
        "supply": number     // Only for master editions
      },
      "tokenAccount": string, // Token account address
      "balance": number      // Token balance
    }>
  } | null,
  "error": {
    "code": string,
    "message": string
  } | null
}
```

Error Codes:
- `CREATE_NFT_ERROR`: General NFT creation error
- `INVALID_ADDRESS`: Invalid wallet or creator address
- `TRANSACTION_ERROR`: Transaction failed
- `CONFIRMATION_ERROR`: Transaction confirmation timeout
- `FETCH_ERROR`: Failed to fetch NFTs


## Configuration

Environment variables:
```
RPC_ENDPOINT=https://api.mainnet-beta.solana.com
MAX_RETRIES=3
CONFIRMATION_TIMEOUT=30000
PORT=3000
```

## Installation

```bash
npm install
```

## Development

```bash
# Run in development mode
npm run dev

# Build
npm run build

# Start production server
npm start

# Run tests
npm test
```

## Project Structure

```
services/token-metadata/
├── src/
│   ├── config/         # Configuration
│   ├── controllers/    # Request handlers
│   ├── services/       # Business logic
│   ├── types/         # TypeScript types
│   ├── utils/         # Helper functions
│   └── index.ts       # Application entry
├── tests/
│   └── integration/   # Integration tests
├── package.json
├── tsconfig.json
└── README.md
```

## Dependencies

- Node.js >= 16
- @metaplex-foundation/mpl-token-metadata
- @solana/web3.js
- Express
- TypeScript

## Security Considerations

- No authentication required (internal service)
- Input validation for all parameters
- Transaction confirmation retry mechanism
- Error handling with appropriate status codes
- Rate limiting recommended for production

## Testing

Integration tests are included to verify:
- NFT creation
- Transaction confirmation
- Error handling
- Input validation

## License

MIT
