from datetime import datetime
import helper_functions
import random


# TODO read inputs, return value if over the needed limit
# generate also decimal values, check if do not break strings

now = datetime.now()
block_size_limit = 5
first_index = 0
transaction_pool = []
user_list = []
currency_list = []
not_full_blocks = []

genesis_block = helper_functions.create_genesis_block()

blockchain = [genesis_block]

for i in range(1501):
    helper_functions.create_user(user_list)

for i in range(70):
    helper_functions.create_currency(currency_list, helper_functions.generate_random_string(3).upper(), helper_functions.generate_random_string(random.randint(5,16)), random.randint(1, 12))

# for currency in currency_list:
#     currency.display_info()

# for user in user_list:
#     user.get_portfolio()

for i in range(508):
    helper_functions.create_random_transaction(transaction_pool, random.choice(user_list).user_id, random.choice(user_list).user_id, random.choice(currency_list).code)

# for t in transaction_pool:
#     t.display_info()


# Create new blocks
helper_functions.create_x_blocks(100, blockchain, block_size_limit)

helper_functions.assign_transactions_to_blocks(transaction_pool, blockchain)

# Display the blockchain
# for block in blockchain:
#     block.display_info()

# print(transaction_pool)