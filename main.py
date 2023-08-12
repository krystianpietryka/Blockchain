import helper_functions
import chart_functions
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import configparser

# TODO generate also decimal values, check if do not break strings
# Configure proper formatters
# Create additional execution logs returning function exec info
# create random usernames

transaction_mean_price = 70
transaction_standard_deviation = 40
amount_of_random_transactions = 300
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

# Get connection string to db from config file
config = configparser.ConfigParser()
config.read('config.ini')
uri = config['mongodb']['connection_string']

client = MongoClient(uri, server_api=ServerApi('1'))

db = client["blockchain_db"]
transactions_collection= db["transactions"]
transaction_pool_collection = db["transaction_pool"]
users_collection= db["users"]
currencies_collection= db["currencies"]
blocks_collection= db["blocks"]
blockchain_collection= db["blockchain"]

#Create genesis block
genesis_block = helper_functions.create_genesis_block(blocks_collection, blockchain_collection)

#Create random users
helper_functions.create_x_random_users(users_collection, 150, 2, 50, 200, 2)

# Create random currencies
helper_functions.create_x_random_currencies(currencies_collection, amount_of_random_currencies, currency_mean_price, currency_standard_deviation, amount_of_crypto_code_syllables, crypto_syllables, amount_of_crypto_code_letters)

# Create random transactions
helper_functions.create_x_random_transactions(transaction_pool_collection, currencies_collection, users_collection, transaction_mean_price, transaction_standard_deviation, amount_of_random_transactions, transactions_collection)

# Create new blocks
helper_functions.create_x_blocks(20, blockchain_collection, block_size_limit, blocks_collection, difficulty=1 )

helper_functions.set_random_user_balances(users_collection)

# # Define the filter criteria (use an empty filter to update all documents in the collection)
# filter_criteria = {}

# # Define the update operation
# update_operation = {"$set": {"amount": 1}}

# # Perform the update for all documents in the collection
# result = transaction_pool_collection.update_many(filter_criteria, update_operation)
# result = transactions_collection.update_many(filter_criteria, update_operation)

# Assign transaction to blocks
helper_functions.assign_transactions_to_blocks(transaction_pool_collection, blocks_collection, users_collection)

# # Display chart
# chart_functions.chart_currency_part(global_transaction_list, currency_list)
