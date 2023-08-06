from datetime import datetime
import helper_functions
import random


# TODO read inputs, return value if over the needed limit
# divide transactions into blocks per limit
# generate also decimal values, check if do not break strings

now = datetime.now()
block_size_limit = 100
first_index = 0
transaction_pool = []
user_list = []
currency_list = []

genesis_block = helper_functions.create_genesis_block()

blockchain = [genesis_block]

for i in range(200):
    helper_functions.create_user(user_list)

for i in range(200):
    helper_functions.create_currency(currency_list, helper_functions.generate_random_string(3).upper(), helper_functions.generate_random_string(random.randint(5,16)), random.randint(1, 12))

for currency in currency_list:
    currency.display_info()

# for user in user_list:
#     user.get_portfolio()

for i in range(50):
    helper_functions.create_random_transaction(transaction_pool, random.choice(user_list).user_id, random.choice(user_list).user_id, random.choice(currency_list).code)

for t in transaction_pool:
    t.display_info()


# # Create new blocks
# helper_functions.create_x_blocks(30, blockchain)

# # Display the blockchain
# for block in blockchain:
#     block.display_info()
