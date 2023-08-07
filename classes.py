import hashlib

class Currency:
    def __init__(self, code, name, value = 0):
        self.code = code
        self.name = name
        self.value = value

    def display_info(self):
        print("\n--------------------------------------------")
        print("code: ", self.code)
        print("name: ", self.name)
        print("value: ", self.value)
        print("--------------------------------------------\n")


class Transaction:
    def __init__(self, uid, sender_key, receiver_key, input, output, fee, currency, amount):
        self.sender_key = sender_key
        self.receiver_key = receiver_key
        self.currency = currency
        self.amount = amount
        self.uid = uid
        self.input = input
        self.output = output
        self.fee = fee

    def display_info(self):
        print("\n--------------------------------------------")
        print("uid: ", self.uid)
        print("sender_key: ", self.sender_key)
        print("receiver_key: ", self.receiver_key)
        print("input: ", self.input)
        print("fee: ", self.fee)
        print("currency: ", self.currency)
        print("amount: ", self.amount)
        print("--------------------------------------------\n")

class User:
    def __init__(self, user_id, balance=0, inputs=None):
        self.user_id = user_id
        self.balance = balance
        self.inputs = inputs if inputs is not None else {}

    def add_balance(self, amount):
        self.balance += amount

    def subtract_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Insufficient balance")

    def add_input(self, input_name, quantity):
        if input_name in self.inputs:
            self.inputs[input_name] += quantity
        else:
            self.inputs[input_name] = quantity

    def subtract_input(self, input_name, quantity):
        if input_name in self.inputs and self.inputs[input_name] >= quantity:
            self.inputs[input_name] -= quantity
        else:
            raise ValueError("Insufficient inputs")

    def get_portfolio(self):
        print("\n--------------------------------------------")
        print("user_id: ", self.user_id)
        print("balance: ",  self.balance)
        print("inputs: ", self.inputs)
        print("--------------------------------------------\n")



class Block:
    def __init__(self, index, timestamp, previous_hash, transactions, nonce, max_transactions):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.max_transactions = max_transactions

    def add_transaction(self, transaction):
        if len(self.transactions) < self.max_transactions:

            self.transactions.append(transaction.uid)
            return True
        return False
        
    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{''.join([item for item in self.transactions])}{self.previous_hash}{self.nonce}"
        hash_object = hashlib.sha256()
        hash_object.update(block_string.encode())
        hex_digest = hash_object.hexdigest()
        return hex_digest
    
    def display_info(self):
        print("\n--------------------------------------------")
        print("Index: ", self.index)
        print("Timestamp: ", self.timestamp)
        print("transactions: ", self.transactions)
        print("Previous Hash: ", self.previous_hash)
        print("Current Hash: ", self.compute_hash())
        print("Nonce: ", self.nonce)
        print("max_transactions: ", self.max_transactions)
        print("--------------------------------------------\n")