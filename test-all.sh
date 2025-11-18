#!/bin/bash

# Comprehensive test script for DukeDollar blockchain
# This script tests all major functionality

# Don't exit on error - we want to count passes/fails
# set -e

PASS=0
FAIL=0
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "DukeDollar Comprehensive Test Suite"
echo "=========================================="
echo ""

# Helper function to check if command succeeded
check_result() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1${NC}"
        ((PASS++))
    else
        echo -e "${RED}✗ $1${NC}"
        ((FAIL++))
    fi
}

# Helper function to check if file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓ File $1 exists${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗ File $1 missing${NC}"
        ((FAIL++))
        return 1
    fi
}

# Clean start
echo -e "${YELLOW}Cleaning environment...${NC}"
make clean > /dev/null 2>&1

echo ""
echo "Test 1: Name command"
result=$(./cryptomoney.sh name)
[ "$result" = "DukeDollar" ]
check_result "Name returns 'DukeDollar'"

echo ""
echo "Test 2: Genesis block"
./cryptomoney.sh genesis > /dev/null 2>&1
check_file "block_0.txt"

echo ""
echo "Test 3: Wallet generation"
./cryptomoney.sh generate test1.wallet.txt > /dev/null 2>&1
check_file "test1.wallet.txt"
./cryptomoney.sh generate test2.wallet.txt > /dev/null 2>&1
check_file "test2.wallet.txt"

echo ""
echo "Test 4: Address extraction"
tag1=$(./cryptomoney.sh address test1.wallet.txt)
[ ${#tag1} -eq 16 ]
check_result "Address is 16 characters long"

echo ""
echo "Test 5: Funding transaction"
tag1=$(./cryptomoney.sh address test1.wallet.txt)
./cryptomoney.sh fund $tag1 100 fund1.txt > /dev/null 2>&1
check_file "fund1.txt"

echo ""
echo "Test 6: Verify funding (bigfoot)"
./cryptomoney.sh verify test1.wallet.txt fund1.txt > /dev/null 2>&1
check_result "Funding verification succeeds"
check_file "mempool.txt"

echo ""
echo "Test 7: Balance check"
balance=$(./cryptomoney.sh balance $tag1)
[ "$balance" -eq 100 ]
check_result "Balance is 100 after funding"

echo ""
echo "Test 8: Transfer transaction"
tag2=$(./cryptomoney.sh address test2.wallet.txt)
./cryptomoney.sh transfer test1.wallet.txt $tag2 30 transfer1.txt > /dev/null 2>&1
check_file "transfer1.txt"

echo ""
echo "Test 9: Verify transfer"
./cryptomoney.sh verify test1.wallet.txt transfer1.txt > /dev/null 2>&1
check_result "Transfer verification succeeds"

echo ""
echo "Test 10: Balance after transfer (before mining)"
balance1=$(./cryptomoney.sh balance $tag1)
balance2=$(./cryptomoney.sh balance $tag2)
[ "$balance1" -eq 70 ] && [ "$balance2" -eq 30 ]
check_result "Balances correct (70 and 30)"

echo ""
echo "Test 11: Mining"
./cryptomoney.sh mine 2 > /dev/null 2>&1
check_file "block_1.txt"

echo ""
echo "Test 12: Mempool cleared after mining"
if [ ! -s mempool.txt ]; then
    echo -e "${GREEN}✓ Mempool is empty after mining${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ Mempool not empty${NC}"
    ((FAIL++))
fi

echo ""
echo "Test 13: Mining difficulty check"
hash=$(sha256sum block_1.txt | awk '{print $1}')
if [[ $hash == 00* ]]; then
    echo -e "${GREEN}✓ Block hash has 2 leading zeros${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ Block hash doesn't meet difficulty${NC}"
    ((FAIL++))
fi

echo ""
echo "Test 14: Balance after mining"
balance1=$(./cryptomoney.sh balance $tag1)
balance2=$(./cryptomoney.sh balance $tag2)
[ "$balance1" -eq 70 ] && [ "$balance2" -eq 30 ]
check_result "Balances still correct after mining"

echo ""
echo "Test 15: Blockchain validation"
result=$(./cryptomoney.sh validate)
[ "$result" = "True" ]
check_result "Blockchain validates correctly"

echo ""
echo "Test 16: Insufficient funds detection"
./cryptomoney.sh transfer test1.wallet.txt $tag2 1000 bad-transfer.txt > /dev/null 2>&1
result=$(./cryptomoney.sh verify test1.wallet.txt bad-transfer.txt 2>&1)
if echo "$result" | grep -q "Insufficient funds"; then
    echo -e "${GREEN}✓ Insufficient funds properly detected${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ Insufficient funds not detected${NC}"
    echo "  Result was: $result"
    ((FAIL++))
fi

echo ""
echo "Test 17: Multiple blocks"
./cryptomoney.sh fund $tag2 50 fund2.txt > /dev/null 2>&1
./cryptomoney.sh verify test2.wallet.txt fund2.txt > /dev/null 2>&1
./cryptomoney.sh mine 2 > /dev/null 2>&1
check_file "block_2.txt"

echo ""
echo "Test 18: Validation after multiple blocks"
result=$(./cryptomoney.sh validate)
[ "$result" = "True" ]
check_result "Blockchain still validates with multiple blocks"

echo ""
echo "Test 19: Tamper detection"
cp block_1.txt block_1.txt.backup
echo "TAMPERED" >> block_1.txt
result=$(./cryptomoney.sh validate)
mv block_1.txt.backup block_1.txt
[ "$result" = "False" ]
check_result "Tampered blockchain detected"

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "Tests Passed: ${GREEN}$PASS${NC}"
echo -e "Tests Failed: ${RED}$FAIL${NC}"
echo "=========================================="

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    echo "Your blockchain implementation is working correctly!"
    exit 0
else
    echo -e "${RED}Some tests failed. Please review the output above.${NC}"
    exit 1
fi