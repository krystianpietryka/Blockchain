import classes
import hashlib
import random
import string
from datetime import datetime

now = datetime.now()

def generate_hash(string):
    hash_object = hashlib.sha256()
    hash_object.update(string.encode())
    hex_digest = hash_object.hexdigest()
    return hex_digest

def generate_random_list():
    length = random.randint(1, 10)  # Generate a random length between 1 and 10
    random_list = [random.randint(1, 100) for _ in range(length)]  # Generate random values
    return random_list
       
def create_user(user_list):
    new_user_id = generate_hash(generate_random_string(random.randint(1,100)))
    new_user = classes.User(new_user_id)
    user_list.append(new_user)

def create_currency(currency_list, code, name, value):
    new_currency = classes.Currency(code,name,value)
    currency_list.append(new_currency)

def concat_transaction_attributes(sender_key, receiver_key, input, output, fee, currency, amount):
    attributes_string = str(sender_key) + str(receiver_key) +  ''.join([str(item) for item in input]) + ''.join([str(item) for item in output]) + str(fee) + str(currency) + str(amount)
    hashed_attributes_string = generate_hash(attributes_string)
    return hashed_attributes_string

def create_transaction(transaction_pool, sender_key, receiver_key, input, output, fee, currency, amount):
    new_uid = concat_transaction_attributes(sender_key, receiver_key, input, output, fee, currency, amount)
    new_transaction = classes.Transaction(new_uid, sender_key, receiver_key, input, output, fee, currency, amount)
    transaction_pool.append(new_transaction)

def create_random_transaction(transaction_pool, sender_key, receiver_key, currency):
    random_input = generate_random_list()
    random_output = [random.randint(1, 100)]
    random_fee = random.randint(1, 100)
    random_amount = random.randint(1, 100)
    create_transaction(transaction_pool, sender_key, receiver_key, random_input, random_output, random_fee, currency, random_amount)

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))



def concat_block_attributes(index, timestamp, previous_hash, data, nonce):
    attributes_string = str(index) + str(timestamp) + str(previous_hash) + ''.join([item for item in data]) + str(nonce)
    return attributes_string

def create_genesis_block():
    return classes.Block(0, now, None, ["Genesis Block"], None)

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = now
    previous_hash = previous_block.compute_hash()
    new_block = classes.Block(index, timestamp, previous_hash, data, 0)

    # Proof of Work (for demonstration purposes)
    while not new_block.compute_hash().startswith("0000"):
        new_block.nonce += 1

    return new_block

def create_x_blocks(amount, blockchain):
    for i in range(amount):
        new_name = 'Transaction_' + str(now) + "_" + str(i)
        new_block = create_new_block(blockchain[-1], new_name)
        blockchain.append(new_block)

