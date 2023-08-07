import classes
import hashlib
import random
import string
from datetime import datetime
import copy

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

def create_transaction(transaction_pool, global_transaction_list, sender_key, receiver_key, input, output, fee, currency, amount):
    new_uid = concat_transaction_attributes(sender_key, receiver_key, input, output, fee, currency, amount)
    new_transaction = classes.Transaction(new_uid, sender_key, receiver_key, input, output, fee, currency, amount)
    transaction_pool.append(new_transaction)
    global_transaction_list.append(new_transaction)

def create_random_transaction(transaction_pool, global_transaction_list, sender_key, receiver_key, currency):
    random_input = generate_random_list()
    random_output = [random.randint(1, 100)]
    random_fee = random.randint(1, 100)
    random_amount = random.randint(1, 100)
    create_transaction(transaction_pool, global_transaction_list, sender_key, receiver_key, random_input,
                        random_output, random_fee, currency, random_amount)

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def concat_block_attributes(index, timestamp, previous_hash, transactions, nonce):
    attributes_string = str(index) + str(timestamp) + str(previous_hash) + ''.join([item for item in transactions]) + str(nonce)
    return attributes_string

def create_genesis_block():
    return classes.Block(0, now, None, ['Genesis Block'], None, 0)

def create_new_block(previous_block, max_transactions, difficulty):
    index = previous_block.index + 1
    timestamp = now
    previous_hash = previous_block.compute_hash()
    new_block = classes.Block(index, timestamp, previous_hash, [], 0, max_transactions)

    # Proof of Work (for demonstration purposes)
    while not new_block.compute_hash().startswith((difficulty * "0")):
        new_block.nonce += 1

    return new_block

def create_x_blocks(amount, blockchain, max_transactions, difficulty):
    for _ in range(amount):
        new_block = create_new_block(blockchain[-1], max_transactions, difficulty)
        blockchain.append(new_block)

def get_user_by_id(user_list, user_id):
    for user in user_list:
        if user.user_id == user_id:
            return user
    return None  # Return None if user is not found

def validate_transaction(transaction, user_list):
    sender = get_user_by_id(user_list, transaction.sender_key)
    transaction_amount = transaction.amount
    if sender not in user_list:
        return False, f'user {transaction.sender_key} not in users list.'
    if sender.balance < transaction_amount:
        return False, 'user balance too low.'
    if transaction_amount <= 0:
        return False, f'invalid transaction amount {transaction_amount}.'
    return True, 'Transaction valid'

def assign_transactions_to_blocks(transaction_pool, blockchain, user_list):
    transaction_pool_copy = copy.copy(transaction_pool)
    for transaction in transaction_pool_copy:
        valid, check_result_message = validate_transaction(transaction, user_list)
        if valid:
            assigned = False
            for block in blockchain:
                if block.add_transaction(transaction):
                    assigned = True
                    transaction_pool.remove(transaction)
                    break
            if not assigned:
                print(f"Transaction {transaction.uid} could not be assigned to any block.")
                # print('Terminating assignments until next transaction assignment round.')
        else:
            print(check_result_message)
            print(f"Transaction {transaction.uid} could not be verified.")
            pass

