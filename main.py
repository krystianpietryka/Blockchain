from datetime import datetime
import helper_functions
import chart_functions
import random
import classes

# TODO generate also decimal values, check if do not break strings

global_transaction_list = []
transaction_pool = []
user_list = []
currency_list = []
not_full_blocks = []

first_index = 0
transaction_mean_price = 200
transaction_standard_deviation = 170
amount_of_random_transactions = 100
amount_of_random_blocks = 30
block_size_limit = 5

amount_of_random_currencies = 15
currency_mean_price = 3000
currency_standard_deviation = 1200
amount_of_crypto_code_syllables = 2
amount_of_crypto_code_letters = 3
crypto_syllables = ['bit', 'coin', 'eth', 'rip', 'do', 'ge', 'lite', 'mo', 'neo', 'mon',
                     'ero', 'zec', 'asu', 'to', 'kusa', 'isa', 'gi', 'cot', 'sap', 'min', 'max', 'mop', 'rak', 'sur', 'taz', 'pat', 'rok', 'cas', 'cal', 'cass',
                     'zap', 'zoe', 'top', 'tor', 'bot', 'bat', 'le', 'la', 'lo', 'li', 'byte', 'no', 'coin']
letters = 'abcdefghijklmnopqrstuvwxyz'

# Create genesis block
genesis_block = helper_functions.create_genesis_block()

# Create blockchain including genesis block
blockchain = [genesis_block]

# Create random users
for i in range(1501):
    helper_functions.create_user(user_list)

# Assign random balance to users
for user in user_list:
    user.balance = random.randint(0,100) 

# Create random currencies
helper_functions.create_x_random_currencies(currency_list, amount_of_random_currencies, currency_mean_price, currency_standard_deviation, amount_of_crypto_code_syllables, crypto_syllables, amount_of_crypto_code_letters)

# Create random transactions
helper_functions.create_x_random_transactions(transaction_pool, global_transaction_list, currency_list, user_list, transaction_mean_price, transaction_standard_deviation, amount_of_random_transactions)

# Log all class and object data
helper_functions.log_all_class_objects_data(helper_functions.get_all_classes(classes))

# Create new blocks
helper_functions.create_x_blocks(50, blockchain, block_size_limit, difficulty=1)

# Assign transaction to blocks
helper_functions.assign_transactions_to_blocks(transaction_pool, blockchain, user_list)

# Display chart
chart_functions.chart_currency_part(global_transaction_list, currency_list)


