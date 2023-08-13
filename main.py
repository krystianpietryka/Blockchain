import helper_functions
import chart_functions
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import configparser

# TODO
# Configure proper formatters
# Check for duplicate data while inserting
# Create additional execution logs returning function exec info

transaction_mean_price = 70
transaction_standard_deviation = 40
amount_of_random_transactions = 100
amount_of_random_user_input_values = 2
user_input_min_value = 50
user_input_max_value = 100
user_balance_decimal_places = 2
amount_of_random_blocks = 30
block_size_limit = 5

amount_of_random_currencies = 15
amount_of_random_clients = 100
amount_of_random_users = 150
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
clients_collection = db["clients"]

helper_functions.recreate_db(client, db, blocks_collection, blockchain_collection, clients_collection, amount_of_random_clients,
                users_collection, amount_of_random_users, amount_of_random_user_input_values, user_input_min_value,
                  user_input_max_value, user_balance_decimal_places, currencies_collection, amount_of_random_currencies, 
                  currency_mean_price, currency_standard_deviation, amount_of_crypto_code_syllables, crypto_syllables, 
                  amount_of_crypto_code_letters, transaction_pool_collection, transaction_mean_price, transaction_standard_deviation,
                  amount_of_random_transactions, transactions_collection, block_size_limit)

# # Display chart
# chart_functions.chart_currency_part(transactions_collection, currencies_collection)
