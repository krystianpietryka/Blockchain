import inspect
import classes
import hashlib
import random
import string
from datetime import datetime
import copy
import numpy as np
import os

now = datetime.now()
current_date = datetime.now().strftime("%Y-%m-%d")
current_hour = datetime.now().strftime("%H:%M").replace(":", "_")

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
    return crypto_name[:3].upper()

def create_currency(currency_list, code, name, value):
    new_currency = classes.Currency(code,name,value)
    currency_list.append(new_currency)

def create_x_random_currencies(currency_list, amount, mean_price, standard_deviation, syllable_count, syllable_list, amount_of_code_letters):
    currency_values = create_random_values(mean_price, standard_deviation, amount)
    for currency_value in currency_values:
        name = generate_random_crypto_name(syllable_count, syllable_list)
        code = generate_crypto_code(amount_of_code_letters, name)
        create_currency(currency_list, code, name, currency_value) 

def concat_transaction_attributes(sender_key, receiver_key, input, output, fee, currency, amount):
    attributes_string = str(sender_key) + str(receiver_key) +  ''.join([str(item) for item in input]) + ''.join([str(item) for item in output]) + str(fee) + str(currency) + str(amount)
    hashed_attributes_string = generate_hash(attributes_string)
    return hashed_attributes_string

def create_transaction(transaction_pool, global_transaction_list, sender_key, receiver_key, input, output, fee, currency, amount):
    new_uid = concat_transaction_attributes(sender_key, receiver_key, input, output, fee, currency, amount)
    new_transaction = classes.Transaction(new_uid, sender_key, receiver_key, input, output, fee, currency, amount)
    transaction_pool.append(new_transaction)
    global_transaction_list.append(new_transaction)

def create_random_transaction_values(mean_price, standard_deviation, amount_of_transactions):
    transaction_prices = np.random.normal(mean_price, standard_deviation, amount_of_transactions)
    # Make sure prices are not negative
    transaction_prices = np.maximum(transaction_prices, 0)
    return transaction_prices

def create_x_random_transactions(transaction_pool, global_transaction_list, currency_list, user_list, mean_price, standard_deviation, amount_of_transactions):
    transaction_prices = create_random_values(mean_price, standard_deviation, amount_of_transactions)
    for price in transaction_prices:
        sender_key = random.choice(user_list).user_id
        receiver_key = random.choice(user_list).user_id
        if receiver_key == sender_key:
            receiver_key = random.choice(user_list).user_id
        random_input = generate_random_list()
        random_output = [random.randint(1, 100)]
        random_fee = random.randint(1, 100)
        currency = random.choice(currency_list).code
        create_transaction(transaction_pool, global_transaction_list, sender_key, receiver_key, random_input,
                        random_output, random_fee, currency, price)

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

def get_instances_of_class(class_name):
    return [instance for instance in class_name.instances]

def convert_class_name_to_user_friendly_format(class_name):
    class_name_user_friendly = str(class_name).replace(" ", "").replace("<", "").replace(">", "").replace("'", "").replace("classes", "")
    return class_name_user_friendly

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def create_current_log_folders():
    # Main log folder
    script_directory = os.path.dirname(os.path.abspath(__file__))
    main_log_folder_name = 'Logs'
    main_log_file_directory = os.path.join(script_directory, main_log_folder_name)
    create_folder_if_not_exists(main_log_file_directory)
    # Current Date
    current_date_log_folder_name = current_date
    current_date_log_folder_directory = os.path.join(main_log_file_directory, current_date_log_folder_name)
    create_folder_if_not_exists(current_date_log_folder_directory)
    # Current Hour
    current_hour_log_folder_name = current_hour
    current_hour_log_folder_directory = os.path.join(current_date_log_folder_directory, current_hour_log_folder_name)
    create_folder_if_not_exists(current_hour_log_folder_directory)
    return current_hour_log_folder_directory

def get_all_classes(module):
    classes = []
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            classes.append(obj)
    return classes

def log_all_class_objects_data(class_names_list):
    class_log_folder_name = 'Class'
    log_file_directory =  os.path.join(create_current_log_folders(), class_log_folder_name)
    create_folder_if_not_exists(log_file_directory)
    for class_name in class_names_list:
        log_file_name = f'{convert_class_name_to_user_friendly_format(class_name)}.log.txt'
        log_file_path = os.path.join(log_file_directory, log_file_name) 
        log_parameters_of_class_objects(class_name, log_file_path)

def log_parameters_of_class_objects(class_name, log_file_path):
    instances = get_instances_of_class(class_name)
    with open(log_file_path, 'w') as log_file:
        log_file.write(f"\n{convert_class_name_to_user_friendly_format(class_name)}")
        for instance in instances:
            log_file.write("\n=======================================================")
            log_file.write((f"\nObject ID: {id(instance)}"))
            attributes = vars(instance)
            for attr, value in attributes.items():
                log_file.write(f"\n{attr} : {value}")

