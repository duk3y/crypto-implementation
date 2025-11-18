# DukeDollar: Educational Blockchain Implementation

A simple, educational blockchain implementation in Python that demonstrates core cryptocurrency concepts including wallets, transactions, mining, and chain validation.

## Features

- **Wallet Management**: Generate cryptographic key pairs and addresses
- **Transactions**: Create and verify signed transactions between wallets
- **Mining**: Proof-of-work mining with adjustable difficulty
- **Balance Tracking**: Query wallet balances across the blockchain
- **Chain Validation**: Verify blockchain integrity
- **Genesis Block**: Initialize your blockchain with a custom message

## Prerequisites

- Python 3.6+
- Bash shell (Linux/macOS) or WSL/Git Bash (Windows)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dukedollar.git
cd dukedollar
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install rsa
```

## Quick Start

Run the basic test to see DukeDollar in action:

```bash
make test
```

Or manually:
```bash
chmod +x cryptomoney.sh basic-test.sh
./basic-test.sh
```

## Usage

### Command Reference

All commands are executed through the `cryptomoney.sh` wrapper script:

#### Get Cryptocurrency Name
```bash
./cryptomoney.sh name
```

#### Create Genesis Block
```bash
./cryptomoney.sh genesis
```
Creates `block_0.txt` with an initial message.

#### Generate a Wallet
```bash
./cryptomoney.sh generate <wallet_file>
```
Example:
```bash
./cryptomoney.sh generate alice.wallet.txt
```

#### Get Wallet Address
```bash
./cryptomoney.sh address <wallet_file>
```
Returns the wallet's public tag (16-character hash).

#### Fund a Wallet
```bash
./cryptomoney.sh fund <tag> <amount> <transaction_file>
```
Creates coins from the special "bigfoot" account. Example:
```bash
./cryptomoney.sh fund a1b2c3d4e5f6g7h8 100 funding.txt
```

#### Transfer Funds
```bash
./cryptomoney.sh transfer <source_wallet> <destination_tag> <amount> <transaction_file>
```
Example:
```bash
./cryptomoney.sh transfer alice.wallet.txt b8c7d6e5f4a3b2c1 25 transfer.txt
```

#### Verify Transaction
```bash
./cryptomoney.sh verify <wallet_file> <transaction_file>
```
Verifies signature and adds valid transactions to mempool.

#### Check Balance
```bash
./cryptomoney.sh balance <tag>
```
Shows current balance for a wallet address.

#### Mine Block
```bash
./cryptomoney.sh mine <difficulty>
```
Mines pending transactions from mempool into a new block. Difficulty determines number of leading zeros required in hash.

#### Validate Blockchain
```bash
./cryptomoney.sh validate
```
Verifies the integrity of the entire blockchain.

## Project Structure

```
dukedollar/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── Makefile                  # Build and test automation
├── cryptomoney.sh           # Shell wrapper script
├── cmoney.py                # Core blockchain implementation
├── basic-test.sh            # Integration test script
├── examples/                # Example usage scripts
│   └── tutorial.sh          # Step-by-step tutorial
├── docs/                    # Additional documentation
│   ├── ARCHITECTURE.md      # System design overview
│   └── TUTORIAL.md          # Detailed tutorial
└── .gitignore              # Git ignore file
```

## How It Works

### Wallets
Wallets consist of RSA public/private key pairs. The wallet address is derived from the first 16 characters of the SHA-256 hash of the public key.

### Transactions
Transactions include:
- Sender's wallet tag
- Recipient's wallet tag
- Amount
- Timestamp
- Digital signature (for non-funding transactions)

### Mining
Mining uses proof-of-work with SHA-256 hashing. Miners search for a nonce that produces a block hash with the required number of leading zeros.

### Blockchain Structure
Each block (except genesis) contains:
- Hash of previous block
- List of transactions
- Nonce value

## Examples

See `examples/tutorial.sh` for a complete walkthrough, or run:

```bash
make tutorial
```

## Development

### Run Tests
```bash
make test
```

### Clean Generated Files
```bash
make clean
```

## Educational Notes

This is a simplified blockchain for educational purposes. It demonstrates core concepts but lacks many features required for production use:

- **Security**: Uses RSA-1024 (real systems use stronger cryptography)
- **Network**: Single-node only (no peer-to-peer networking)
- **Consensus**: Simple proof-of-work (no distributed consensus)
- **Scalability**: File-based storage (no database)
- **Features**: No transaction fees, smart contracts, or advanced features

## Learning Resources

- [Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
- [Blockchain Basics](https://www.investopedia.com/terms/b/blockchain.asp)
- [Proof of Work Explained](https://en.bitcoin.it/wiki/Proof_of_work)

## Contributing

Contributions are welcome! This is an educational project, so clarity and documentation are prioritized. Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Created as an educational demonstration of blockchain technology principles.

---

**Disclaimer**: This is educational software. Do not use for real cryptocurrency or financial applications.
