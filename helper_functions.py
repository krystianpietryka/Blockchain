import hashlib
import random
import string
from datetime import datetime
import numpy as np
import os
import pymongo
from loggers import logger_error, logger_info, logger_details

now = datetime.now()
current_date = datetime.now().strftime("%Y-%m-%d")
current_hour = datetime.now().strftime("%H:%M").replace(":", "_")

def log_info(text):
    logger_info.info(f'{text}')

def log_error(text):
    logger_error.info(f'{text}')

def log_details(text):
    logger_details.info(f'{text}')

def log_info_and_details(text):
    logger_info.info(f'{text}')
    logger_details.info(f'{text}')

def drop_database(client, db_name):
    log_info_and_details(f"Dropping {db_name}")
    client.drop_database(db_name)

def recreate_db(client, db_name, blocks_collection, blockchain_collection, clients_collection, amount_of_random_clients,
                users_collection, amount_of_random_users, amount_of_random_user_input_values, user_input_min_value,
                  user_input_max_value, user_balance_decimal_places, currencies_collection, amount_of_random_currencies, 
                  currency_mean_price, currency_standard_deviation, amount_of_crypto_code_syllables, crypto_syllables, 
                  amount_of_crypto_code_letters, transaction_pool_collection, transaction_mean_price, transaction_standard_deviation,
                  amount_of_random_transactions, transactions_collection, block_size_limit):

    # Drop db if exists
    drop_database(client, db_name)

    # Create genesis block
    create_genesis_block(blocks_collection, blockchain_collection)

    # Create random clients
    create_x_random_clients(clients_collection, amount_of_random_clients)

    #Create random users
    create_x_random_users(users_collection, clients_collection,  amount_of_random_users, amount_of_random_user_input_values,
                           user_input_min_value, user_input_max_value, user_balance_decimal_places)

    # Create random currencies
    create_x_random_currencies(currencies_collection, amount_of_random_currencies, currency_mean_price, currency_standard_deviation,
                                amount_of_crypto_code_syllables, crypto_syllables, amount_of_crypto_code_letters)

    # Create random transactions
    create_x_random_transactions(transaction_pool_collection, currencies_collection, users_collection, transaction_mean_price,
                                  transaction_standard_deviation, amount_of_random_transactions, transactions_collection)

    # Create new blocks
    create_x_blocks(20, blockchain_collection, block_size_limit, blocks_collection, difficulty=1 )

    # Assign transaction to blocks
    assign_transactions_to_blocks(transaction_pool_collection, blocks_collection, users_collection)

def generate_hash(string):
    hash_object = hashlib.sha256()
    hash_object.update(string.encode())
    hex_digest = hash_object.hexdigest()
    return hex_digest

def generate_random_list():
    length = random.randint(1, 10)  # Generate a random length between 1 and 10
    random_list = [random.randint(1, 100) for _ in range(length)]  # Generate random values
    return random_list

def set_random_user_balances(users_collection):
    filter_criteria = {
    "$or": [{"balance": 0}, {"balance": None}]}
    users_with_zero_balance = list(users_collection.find(filter_criteria))
    for user in users_with_zero_balance:
        new_balance = user.get("balance", 0) + random.randint(80, 200)
        users_collection.update_one({"_id": user["_id"]}, {"$set": {"balance": new_balance}})

def generate_random_decimal_list(x, min_value, max_value, decimal_places):
    random_decimal_list = [round(random.uniform(min_value, max_value), decimal_places) for _ in range(x)]
    return random_decimal_list

def create_random_email(login):
    domain = "@example.com"
    email = login + domain
    return email

def create_random_login():
    login =  ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return login 

def get_random_name(file_path):
    try:
        with open(file_path, "r", encoding='UTF-8') as file:
            lines = file.readlines()
            # Choose a random line (name) from the file
            random_name = random.choice(lines).strip()
            return random_name
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def generate_random_ssn():
    # Generate a random 9-digit number
    ssn = ''.join(random.choices('0123456789', k=9))
    # Format the number as a string with dashes (###-##-####)
    formatted_ssn = f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}"
    return formatted_ssn

def generate_random_street_name():
    # Common street name components
    street_components = ["Main", "Maple", "Oak", "Elm", "Cedar", "Pine", "Birch", "Avenue", "Street", "Lane", "Road", "Drive"]
    # Randomly choose 2-3 components from the list
    num_components = random.randint(2, 3)
    selected_components = random.sample(street_components, num_components)
    # Combine the selected components to create the street name
    street_name = ' '.join(selected_components)
    return street_name

def create_x_random_clients(clients_collection, amount):
    log_info_and_details(f'Creating {amount} random clients')
    script_directory = os.path.dirname(os.path.abspath(__file__))
    first_names_directory = os.path.join(script_directory, "client_data_lists/first_names.txt")
    last_names_directory = os.path.join(script_directory, "client_data_lists/last_names.txt")
    cities_directory = os.path.join(script_directory, "client_data_lists/cities.txt")
    for _ in range(amount):
        first_name = get_random_name(first_names_directory)
        last_name = get_random_name(last_names_directory)
        age = random.randint(18, 99)
        ssn = generate_random_ssn() 
        city = get_random_name(cities_directory)
        street = generate_random_street_name()
        house_number = random.randint(0, 200)
        create_client(clients_collection, first_name, last_name, age, ssn, city, street, house_number)

def create_client(clients_collection, first_name, last_name, age, ssn, city, street, house_number):
    new_client = {}
    new_client["first_name"] = first_name
    new_client["last_name"] = last_name
    new_client["age"] = age
    new_client["ssn"] = ssn
    new_client["city"] = city
    new_client["street"] = street
    new_client["house_number"] = house_number
    new_client["date_of_creation"] = current_date
    log_details(new_client)
    clients_collection.insert_one(new_client)

def create_random_password(length=12, use_uppercase=True, use_digits=True, use_special_chars=True):
    chars = string.ascii_lowercase
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special_chars:
        chars += string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def create_x_random_users(users_collection, clients_collection, amount_of_users, amount_of_random_values, min_value, max_value,  decimal_places):
    log_info_and_details(f'Creating {amount_of_users} random users')
    client_ids = [doc["_id"] for doc in clients_collection.find({}, {"_id": 1})]
    for _ in range(amount_of_users):
        random_client_id = random.choice(client_ids)
        inputs = generate_random_decimal_list(amount_of_random_values, min_value, max_value, decimal_places)
        balance = sum(inputs)
        login = create_random_login()
        email = create_random_email(login)
        password = create_random_password()
        create_user(users_collection, random_client_id, balance, inputs, email, login, password)

def create_user(users_collection, client_id, balance, inputs, email, login, password):
    new_user = {}
    new_user["balance"] = balance
    new_user["inputs"] = inputs
    new_user["email"] = email
    new_user["login"] = login
    new_user["password"] = password
    new_user["date_of_creation"] = current_date
    log_details(new_user)
    users_collection.insert_one(new_user)

def create_random_values(mean_price, standard_deviation, amount):
    values = np.random.normal(mean_price, standard_deviation, amount)
    # Make sure prices are not negative
    values = np.maximum(values, 0)
    return values    

def generate_random_crypto_name(syllable_count, syllable_list):
    if syllable_count <= 0:
        return ""
    name = ""
    for _ in range(syllable_count):
        name += random.choice(syllable_list)
    return name.capitalize()

def generate_random_crypto_name_letters(length, letter_list):
    if length <= 0:
        return ""
    name = ""
    for _ in range(length):
        name += random.choice(letter_list)
    return name.capitalize()

def generate_crypto_code(amount_of_letters, crypto_name):
    crypto_name = crypto_name.replace(" ", "")
    return crypto_name[:amount_of_letters].upper()

def create_currency(currencies_collection, code, name, value):
    new_currency = {}
    new_currency['code'] = code
    new_currency['name'] = name
    new_currency['value'] = value
    log_details(new_currency)
    currencies_collection.insert_one(new_currency)

def create_x_random_currencies(currencies_collection, amount, mean_price, standard_deviation, syllable_count, syllable_list, amount_of_code_letters):
    log_info_and_details(f"Creating {amount} random currencies")
    currency_values = create_random_values(mean_price, standard_deviation, amount)
    for currency_value in currency_values:
        name = generate_random_crypto_name(syllable_count, syllable_list)
        code = generate_crypto_code(amount_of_code_letters, name)
        create_currency(currencies_collection, code, name, currency_value) 

def concat_transaction_attributes(sender_key, receiver_key, input, output, fee, currency, amount):
    attributes_string = str(sender_key) + str(receiver_key) +  ''.join([str(item) for item in input]) + ''.join([str(item) for item in output]) + str(fee) + str(currency) + str(amount)
    hashed_attributes_string = generate_hash(attributes_string)
    return hashed_attributes_string

def create_transaction(transaction_pool_collection, sender_key, receiver_key, input, output, fee, currency, amount, transactions_collection):
    new_transaction = {}
    new_transaction['sender_key'] = sender_key
    new_transaction['receiver_key'] = receiver_key
    new_transaction['currency'] = currency
    new_transaction['amount'] = amount
    new_transaction['input'] = input
    new_transaction['output'] = output
    new_transaction['fee'] = fee
    log_details(new_transaction)
    transactions_collection.insert_one(new_transaction)
    transaction_pool_collection.insert_one(new_transaction)

def create_random_transaction_values(mean_price, standard_deviation, amount_of_transactions):
    transaction_prices = np.random.normal(mean_price, standard_deviation, amount_of_transactions)
    # Make sure prices are not negative
    transaction_prices = np.maximum(transaction_prices, 0)
    return transaction_prices

def create_x_random_transactions(transaction_pool_collection,  currencies_collection, users_collection, mean_price, standard_deviation, amount_of_transactions, transactions_collection):
    log_info_and_details(f"Creating {amount_of_transactions} random transactions")
    transaction_prices = create_random_values(mean_price, standard_deviation, amount_of_transactions)
    user_ids = [doc["_id"] for doc in users_collection.find({}, {"_id": 1})]
    currencies_ids = [doc["_id"] for doc in currencies_collection.find({}, {"_id": 1})]
    for price in transaction_prices:
        sender_key = random.choice(user_ids)
        receiver_key = random.choice(user_ids)
        if receiver_key == sender_key:
            receiver_key = random.choice(user_ids)
        random_input = generate_random_list()
        random_output = [random.randint(1, 100)]
        random_fee = random.randint(1, 100)
        currency = random.choice(currencies_ids)
        create_transaction(transaction_pool_collection, sender_key, receiver_key, random_input,
                        random_output, random_fee, currency, price, transactions_collection)

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def concat_block_attributes(index, timestamp, previous_hash, transactions, nonce):
    attributes_string = str(index) + str(timestamp) + str(previous_hash) + ''.join([item for item in transactions]) + str(nonce)
    return attributes_string

def create_genesis_block(blocks_collection, blockchain_collection):
    log_info_and_details(f"Creating genesis block")
    new_block = {}
    new_block['timestamp'] = now
    new_block['transactions'] = ['Genesis Block']
    new_block['previous_hash'] = None
    new_block['nonce'] = None
    new_block['max_transactions'] = 0
    new_block['is_full'] = 0
    insert_result  = blocks_collection.insert_one(new_block)
    inserted_id = insert_result.inserted_id
    new_blockchain_node = {"previous_block_id": None, "block_id": inserted_id}
    blockchain_collection.insert_one(new_blockchain_node)
    return inserted_id

def compute_hash(block_dict):
    block_string = f"{block_dict['timestamp']}{''.join([str(item) for item in block_dict['transactions']])}{block_dict['previous_hash']}{block_dict['nonce']}"
    hash_object = hashlib.sha256()
    hash_object.update(block_string.encode())
    hex_digest = hash_object.hexdigest()
    return hex_digest

def create_new_block(blockchain_collection, max_transactions, difficulty, blocks_collection):
    new_blockchain_node = {}
    previous_block = blocks_collection.find_one(sort=[("_id", pymongo.DESCENDING)])
    previous_block_index = previous_block["_id"]
    previous_hash = compute_hash(previous_block)
    new_block = {}
    new_block['timestamp'] = now
    new_block['transactions'] = []
    new_block['previous_hash'] = previous_hash
    new_block['nonce'] = 0
    new_block['max_transactions'] = max_transactions
    new_block['is_full'] = 0
    insert_result  = blocks_collection.insert_one(new_block)
    inserted_id = insert_result.inserted_id
    # Proof of Work (for demonstration purposes)
    while not compute_hash(new_block).startswith((difficulty * "0")):
        new_block["nonce"] += 1
    new_blockchain_node["previous_block_id"] = previous_block_index
    new_blockchain_node["block_id"] = inserted_id
    log_details(new_block)
    log_details(new_blockchain_node)
    blockchain_collection.insert_one(new_blockchain_node)

def create_x_blocks(amount, blockchain_collection, max_transactions, blocks_collection,  difficulty):
    log_info_and_details(f"Creating {amount} blocks")
    for _ in range(amount):  
            create_new_block(blockchain_collection, max_transactions, difficulty, blocks_collection)

def validate_transaction(transaction, users_collection):
    user_ids = [doc["_id"] for doc in users_collection.find({}, {"_id": 1})]
    sender_id = transaction["sender_key"]
    filter_criteria = {"_id": sender_id}
    sender = users_collection.find_one(filter_criteria)
    transaction_amount = transaction["amount"]
    if sender_id not in user_ids:
        log_details(f'user {sender_id} not in users list.')
        return False
    if sender["balance"] < transaction_amount:
        log_details(f'user balance too low. balance:{sender["balance"]}, transaction_amount: {transaction_amount}')
        return False
    if transaction_amount <= 0:
        log_details(f'invalid transaction amount {transaction_amount}.')
        return False
    return True


def validate_add_transaction(blocks_collection, block_id, transaction_id):
    filter_criteria = {"_id": block_id}
    block = blocks_collection.find_one(filter_criteria)
    if len(block["transactions"]) < block["max_transactions"]:
        update_query = {"$push": {"transactions": transaction_id}}
        blocks_collection.update_one(filter_criteria, update_query)
        return True
    else:
        update_query = {"$set": {"is_full": 1}}
        log_details(f"Setting {block_id} to full")
        blocks_collection.update_one(filter_criteria, update_query)
        return False
    
def assign_transactions_to_blocks(transaction_pool_collection, blocks_collection, users_collection):
    transaction_pool_find = transaction_pool_collection.find()
    blocks_list = list(blocks_collection.find())  # Convert cursor to a list
    transactions_list = list(transaction_pool_find)
    log_info_and_details(f"Assigning {len(transactions_list)} transactions to blocks")
    for transaction in transactions_list:
        transaction_id = transaction["_id"]
        valid = validate_transaction(transaction, users_collection)
        if valid:
            assigned = False
            for block in blocks_list:
                block_id = block["_id"]
                validate_add = validate_add_transaction(blocks_collection, block_id, transaction_id)
                if validate_add:
                    assigned = True
                    filter_criteria = {"_id": transaction_id}
                    log_details(f"{transaction_id} assigned to {block_id}")
                    transaction_pool_collection.delete_one(filter_criteria)
                    break  # Stop searching for a block to assign this transaction

            if not assigned:
                log_details(f"Transaction {transaction_id} could not be assigned to any block.")
                pass
        else:
            log_details(f"Transaction {transaction_id} could not be verified.")
            pass