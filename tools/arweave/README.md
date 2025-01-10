# Arweave CLI Tools

Command line tools for Arweave wallet management and balance checking.

## Quick Start

```bash
# Generate new wallet
python generate_wallet.py

# Check wallet balance
python check_balance.py --address YOUR_WALLET_ADDRESS
```

## Wallet Generation Tool

Generate new Arweave wallet and QR code for deposits.

```bash
python generate_wallet.py [--output wallet.json]

Options:
  --output    Path to save wallet JWK file (default: arweave-key.json)
```

Example output:
```
Wallet generated successfully!
Address: xyz123...
Balance: 0.0 AR

To get AR tokens:
1. Visit https://faucet.arweave.net
2. Use exchange like Binance or Gate.io
3. Send AR to address: xyz123...
```

## Balance Checker Tool

Check wallet balance using address or JWK file.

```bash
python check_balance.py [--address ADDRESS | --jwk WALLET_FILE]

Options:
  --address   Arweave wallet address
  --jwk       Path to JWK wallet file

Examples:
  # Check by address
  python check_balance.py --address xyz123...

  # Check by wallet file
  python check_balance.py --jwk wallet.json
```

Example output:
```
Address: xyz123...
Balance: 10.523000 AR
Balance (Winston): 10523000000000
AR Price: $5.67
Value: $59.67
```

## Common Operations

1. Create new wallet and check balance:
```bash
# Generate wallet
python generate_wallet.py --output my_wallet.json

# Check initial balance
python check_balance.py --jwk my_wallet.json
```
