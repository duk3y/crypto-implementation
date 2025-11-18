.PHONY: test clean help install setup venv

help:
	@echo "DukeDollar - Educational Blockchain"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup     - Create venv and install dependencies (first time)"
	@echo "  make test      - Run the basic test script"
	@echo "  make test-all  - Run comprehensive test suite"
	@echo "  make clean     - Remove all generated files"
	@echo "  make install   - Install required Python dependencies"
	@echo "  make help      - Show this help message"
	@echo ""
	@echo "Quick start: make setup && make test"

setup: venv install
	@echo ""
	@echo "Setup complete!"
	@echo "Virtual environment created in ./venv"
	@echo ""
	@echo "To activate manually:"
	@echo "  source venv/bin/activate"

venv:
	@echo "Creating virtual environment..."
	@test -d venv || python3 -m venv venv
	@echo "Virtual environment created in ./venv"

install:
	@echo "Installing required Python packages..."
	@./venv/bin/pip install rsa
	@echo "Dependencies installed!"

test-all: 
	@chmod +x test-all.sh
	@./test-all.sh

test: clean
	@echo "Running basic blockchain test..."
	@chmod +x cryptomoney.sh basic-test.sh
	@./basic-test.sh

clean:
	@echo "Cleaning up generated files..."
	@rm -f *.wallet.txt 2>/dev/null || true
	@rm -f block_*.txt 2>/dev/null || true
	@rm -f mempool.txt 2>/dev/null || true
	@rm -f fund1.txt fund2.txt 2>/dev/null || true
	@rm -f transfer1.txt transfer2.txt 2>/dev/null || true
	@rm -f bad-transfer.txt 2>/dev/null || true
	@rm -f *-funding.txt *-to-*.txt 2>/dev/null || true
	@rm -f test1.wallet.txt test2.wallet.txt 2>/dev/null || true
	@rm -f debug*.txt debug*.wallet.txt 2>/dev/null || true
	@echo "Clean complete!"