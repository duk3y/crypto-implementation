import sys, hashlib, binascii, rsa, datetime, os

# gets the hash of a file; from https://stackoverflow.com/a/44873382
def hashFile(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

# given an array of bytes, return a hex reprenstation of it
def bytesToString(data):
    return binascii.hexlify(data)

# given a hex reprensetation, convert it to an array of bytes
def stringToBytes(hexstr):
    return binascii.a2b_hex(hexstr)

# Load the wallet keys from a filename
def loadWallet(filename):
    with open(filename, mode='rb') as file:
        keydata = file.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    pubkey = rsa.PublicKey.load_pkcs1(keydata)
    return pubkey, privkey

# save the wallet to a file
def saveWallet(pubkey, privkey, filename):
    # Save the keys to a key format (outputs bytes)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    privkeyBytes = privkey.save_pkcs1(format='PEM')
    # Convert those bytes to strings to write to a file (gibberish, but a string...)
    pubkeyString = pubkeyBytes.decode('ascii')
    privkeyString = privkeyBytes.decode('ascii')
    # Write both keys to the wallet file
    with open(filename, 'w') as file:
        file.write(pubkeyString)
        file.write(privkeyString)
    return

# some code snippets for how to use the rsa module
#
# ----------------------------------------
# signing a transaction statement: let:
#
# - 'keystring' be the contents of the saved key file
# - 'message' be what we are verifying: the first four lines of the transaction statement
#
# privkey = rsa.PrivateKey.load_pkcs1(keystring)
# sig = rsa.sign(bytes(message.encode('ascii')), privkey, 'SHA-256')
#
# You can write the signature to the file as sig.hex()
#
# ----------------------------------------
# verifying a signature: let:
#
# - 'keystring' be the contents of the saved key file
# - 'sig' be the signature in the transaction statement, which is a series of hex characters
# - 'message' be what we are verifying: the first four lines of the transaction statement (note that this code takes the hash for you)
#
# pubkey = rsa.PublicKey.load_pkcs1(keystring)
# rsa.verify(bytes(message.encode('ascii')), bytes.fromhex(sig), pubkey)

# Feel free to edit the name of your cryptocurrency!
def name():
    return("DukeDollar")

def genesis():
    # create genesis block with quote
    file = open("block_0.txt", "w")
    file.write("Genesis block created!")
    file.close()

    return("The genesis block has been created in 'block_0.txt'.")

def generate(filename):
    # create keys
    public_key, private_key = rsa.newkeys(1024)

    # create wallet
    saveWallet(public_key, private_key, filename)

    # create tag (first 16 characters of public key)
    tag = hashlib.sha256(public_key.save_pkcs1()).hexdigest()[:16]

    return(f"New wallet generated in '{filename}' with tag {tag}.")

def address(filename):
    # load wallet
    public_key, _ = loadWallet(filename)

    # print tag
    tag = hashlib.sha256(public_key.save_pkcs1()).hexdigest()[:16]
    return(tag)

def fund(tag_a, amount, transaction_file):
    special_id = 'bigfoot'

    # create transaction
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction = (
        f"From: {special_id}\n"
        f"To: {tag_a}\n"
        f"Amount: {amount}\n"
        f"Date: {timestamp}\n"
    )
    
    with open(transaction_file, 'w') as file:
        file.write(transaction)  

    return(f"Funded wallet {tag_a} with {amount} {name()}s on {timestamp}")
    

def transfer(source_wallet, destination_tag, amount, transaction_file):
    _, source_privkey = loadWallet(source_wallet)

    # create transaction
    source_tag = address(source_wallet)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction = (
        f"From: {source_tag}\n"
        f"To: {destination_tag}\n"
        f"Amount: {amount}\n"
        f"Date: {timestamp}\n"
    )

    # sign transaction
    signature = rsa.sign(transaction.encode('ascii'), source_privkey, 'SHA-256').hex()
    
    with open(transaction_file, 'w') as file:
        file.write(transaction)
        file.write(signature)

    return f"Transferred {amount} from {source_wallet} to {destination_tag} and the statement to '{transaction_file}' on date {timestamp}"

def balance(wallet_tag):
    total_balance = 0

    # process blocks
    for filename in sorted(os.listdir()):
        if filename.startswith("block_") and filename.endswith(".txt"):
            with open(f"{filename}", "r") as file:
                lines = file.readlines()
                for line in lines[1:]:  # Skip the first line (hash of the previous block)
                    if line.strip():  # Ignore blank lines
                        parts = line.split()
                        if len(parts) >= 5 and parts[1] == "transferred":
                            source = parts[0]
                            destination = parts[4]
                            amount = int(parts[2])
                            if source == wallet_tag:
                                total_balance -= amount
                            if destination == wallet_tag:
                                total_balance += amount

    # process mempool if it exists
    if os.path.exists("mempool.txt"):
        with open("mempool.txt", "r") as file:
            for line in file:
                parts = line.split()
                if len(parts) >= 5 and parts[1] == "transferred":
                    source = parts[0]
                    destination = parts[4]
                    amount = int(parts[2])
                    if source == wallet_tag:
                        total_balance -= amount
                    if destination == wallet_tag:
                        total_balance += amount

    return(total_balance)

def verify(wallet_name, statement):
    sender_pubkey, _ = loadWallet(wallet_name)

    # read transaction details
    with open(statement, "r") as file:
        lines = file.readlines()

    # recreate message
    from_line = lines[0].split(": ")[1].strip()
    to_line = lines[1].split(": ")[1].strip()
    amount_line = int(lines[2].split(": ")[1].strip())
    date_line = lines[3].split(": ")[1].strip()

    # check for bigfoot id
    if from_line == "bigfoot":
        # directly add to mempool (no verification needed)
        transaction_line = f"{from_line} transferred {amount_line} to {to_line} on {date_line}\n"
        with open("mempool.txt", "a") as mempool:
            mempool.write(transaction_line)
        
        return (f"Bigfoot transaction in file '{statement}' is valid and was written to the mempool.")

    # if not, proceed with normal verification
    signature = lines[4].strip()
    message = "".join(lines[:4])

    # verify signature
    try:
        rsa.verify(message.encode('ascii'), bytes.fromhex(signature), sender_pubkey)
    except rsa.VerificationError:
        return (f"Invalid signature in transaction '{statement}'.")
    
    # check balance
    sender_balance = balance(from_line)
    if sender_balance < amount_line:
        return (f"Insufficient funds in wallet '{wallet_name}' for transaction '{statement}'.")

    # add transaction to mempool
    transaction_line = f"{from_line} transferred {amount_line} to {to_line} on {date_line}\n"
    with open("mempool.txt", "a") as mempool:
        mempool.write(transaction_line)

    return (f"The transaction in file '{statement}' with wallet '{wallet_name}' is valid, and was written to the mempool.")

def mine(difficulty):
    difficulty = int(difficulty)
    
    # get prev block's hash
    blocks = sorted([f for f in os.listdir() if f.startswith("block_") and f.endswith(".txt")])
    if not blocks:
        print("No blocks found. Ensure the genesis block is created.")
        return
    last_block_file = blocks[-1]
    prev_hash = hashFile(last_block_file)

    # get transactions from mempool
    if not os.path.exists("mempool.txt") or os.stat("mempool.txt").st_size == 0:
        print("Mempool is empty. No transactions to mine.")
        return
    with open("mempool.txt", "r") as mempool:
        transactions = mempool.readlines()

    # find valid nonce
    nonce = 0
    while True:
        block_content = f"{prev_hash}\n{''.join(transactions)}{nonce}\n"
        block_hash = hashlib.sha256(block_content.encode("utf-8")).hexdigest()
        if block_hash.startswith("0" * difficulty):
            break
        nonce += 1

    # new block
    new_block_file = f"block_{len(blocks)}.txt"
    with open(new_block_file, "w") as block:
        block.write(f"{prev_hash}\n")
        block.writelines(transactions)
        block.write(f"{nonce}\n")

    # clear mempool 
    with open("mempool.txt", "w") as mempool:
        pass

    return(f"Mempool transactions moved to {new_block_file} and mined with difficulty {difficulty} and nonce {nonce}")

def validate():
    # get blocks
    blocks = sorted([f for f in os.listdir() if f.startswith("block_") and f.endswith(".txt")])
 
    # if only genesis block
    if len(blocks) == 1:
        return True
    
    # validate hashes
    for i in range(1, len(blocks)):
        current_block = blocks[i]
        previous_block = blocks[i - 1]

        # read stored hash from prev block
        with open(current_block, "r") as file:
            stored_prev_hash = file.readline().strip() 

        # compute previous block's hash
        actual_prev_hash = hashFile(previous_block)

        # compare hashes
        if stored_prev_hash != actual_prev_hash:
            return False
        
    return True


if __name__ == "__main__":
    length = len(sys.argv)
    if sys.argv[1] == "name":
        print(name())
    if sys.argv[1] == "genesis":
        print(genesis())
    if sys.argv[1] == "generate":
        print(generate(sys.argv[2]))
    if sys.argv[1] == "address":
        print(address(sys.argv[2]))
    if sys.argv[1] == "fund":
        print(fund(sys.argv[2], int(sys.argv[3]), sys.argv[4]))
    if sys.argv[1] == "transfer":
        print(transfer(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]))
    if sys.argv[1] == "balance":
        print(balance(sys.argv[2]))
    if sys.argv[1] == "verify":
        print(verify(sys.argv[2], sys.argv[3]))
    if sys.argv[1] == "mine":
        print(mine(sys.argv[2]))
    if sys.argv[1] == "validate":
        print(validate())