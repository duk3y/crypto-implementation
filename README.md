# DukeDollar - Educational Blockchain Implementation

A simple educational cryptocurrency implementation in Python to demonstrate blockchain concepts including wallets, transactions, mining, and validation.

## Features

- Wallet generation with RSA key pairs
- Transaction creation and signing
- Transaction verification
- Proof-of-work mining
- Blockchain validation
- Balance tracking

## Prerequisites

- Python 3.x
- pip3

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/duk3y/crypto-implementation.git
   cd crypto-implementation
   ```

2. Set up the environment (creates virtual environment and installs dependencies):
   ```bash
   make setup
   ```

3. Run the basic test to see the blockchain in action:
   ```bash
   make test
   ```

### Manual Setup (Alternative)

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install rsa

# Run tests
./basic-test.sh

# Deactivate when done
deactivate
```

**Note:** The scripts will automatically use the virtual environment if it exists, so you don't need to manually activate it for each command.

## Project Structure

```
.
├── cmoney.py           # Core blockchain implementation
├── cryptomoney.sh      # Shell wrapper script
├── basic-test.sh       # Example usage script
├── Makefile           # Build and test commands
└── README.md          # This file
```

## Usage

### Initialize the Blockchain

Create the genesis block:
```bash
./cryptomoney.sh genesis
```

### Create Wallets

Generate a new wallet:
```bash
./cryptomoney.sh generate alice.wallet.txt
```

Get wallet address (tag):
```bash
./cryptomoney.sh address alice.wallet.txt
```

### Transactions

Fund a wallet (system transaction):
```bash
./cryptomoney.sh fund <wallet_tag> <amount> <transaction_file>
```

Transfer between wallets:
```bash
./cryptomoney.sh transfer <source_wallet> <destination_tag> <amount> <transaction_file>
```

Verify a transaction:
```bash
./cryptomoney.sh verify <wallet_file> <transaction_file>
```

### Mining

Mine pending transactions:
```bash
./cryptomoney.sh mine <difficulty>
```
Where difficulty is the number of leading zeros required in the block hash.

### Query

Check wallet balance:
```bash
./cryptomoney.sh balance <wallet_tag>
```

Validate the blockchain:
```bash
./cryptomoney.sh validate
```

## How It Works

1. **Wallets**: Each wallet contains an RSA key pair (public/private keys). The wallet tag is the first 16 characters of the SHA-256 hash of the public key.

2. **Transactions**: Transactions are signed with the sender's private key and verified using their public key. Valid transactions are added to the mempool.

3. **Mining**: Mining takes all transactions from the mempool and creates a new block by finding a nonce that produces a hash with the required number of leading zeros (proof-of-work).

4. **Blockchain**: Each block contains the hash of the previous block, creating a chain. The blockchain can be validated by verifying all block hashes.

## Example Workflow

```bash
# Initialize
./cryptomoney.sh genesis

# Create wallets
./cryptomoney.sh generate alice.wallet.txt
./cryptomoney.sh generate bob.wallet.txt

# Get wallet addresses
alice=$(./cryptomoney.sh address alice.wallet.txt)
bob=$(./cryptomoney.sh address bob.wallet.txt)

# Fund wallets
./cryptomoney.sh fund $alice 100 fund-alice.txt
./cryptomoney.sh verify alice.wallet.txt fund-alice.txt

# Transfer money
./cryptomoney.sh transfer alice.wallet.txt $bob 25 alice-to-bob.txt
./cryptomoney.sh verify alice.wallet.txt alice-to-bob.txt

# Mine the block
./cryptomoney.sh mine 2

# Check balances
./cryptomoney.sh balance $alice
./cryptomoney.sh balance $bob

# Validate blockchain
./cryptomoney.sh validate
```

## Educational Notes

This implementation demonstrates:
- **Digital signatures**: Using RSA to sign and verify transactions
- **Proof-of-work**: Mining blocks by finding valid nonces
- **Blockchain structure**: Linking blocks through cryptographic hashes
- **UTXO-like model**: Tracking balances through transaction history

## Limitations

This is a simplified educational implementation and lacks many features of production blockchains:
- No peer-to-peer networking
- No consensus mechanism beyond proof-of-work
- Simple balance calculation (not UTXO-based)
- No transaction fees
- Limited security features

## License

Educational use only.

## Contributing

This is an educational project. Feel free to fork and experiment!
