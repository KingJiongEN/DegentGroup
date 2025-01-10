#!/bin/bash

# Make script exit on first error
set -e

# Change to project root directory (assuming script is in scripts folder)
cd "$(dirname "$0")/.."

# Run the OKEX client test_get_all_token_balances test
pytest tests/plugins/plugin_solana/tools/check_balance_test.py -k "test_check_wallet_balance" -v --log-cli-level=INFO -s

# Add some visual separation
echo ""
echo "Integration test completed!"