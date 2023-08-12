import hashlib

class Currency:
    instances = []
    def __init__(self, code, name, value = 0):
        self.code = code
        self.name = name
        self.value = value
        Currency.instances.append(self)  # Add instance to the instances list

    def display_info(self):
        print("\n--------------------------------------------")
        print("code: ", self.code)
        print("name: ", self.name)
        print("value: ", self.value)
        print("--------------------------------------------\n")

class Transaction:
    instances = []
    def __init__(self,  sender_key, receiver_key, input, output, fee, currency, amount):
        self.sender_key = sender_key
        self.receiver_key = receiver_key
        self.currency = currency
        self.amount = amount
        self.input = input
        self.output = output
        self.fee = fee
        Transaction.instances.append(self)  # Add instance to the instances list

    def display_info(self):
        print("\n--------------------------------------------")
        print("sender_key: ", self.sender_key)
        print("receiver_key: ", self.receiver_key)
        print("input: ", self.input)
        print("fee: ", self.fee)
        print("currency: ", self.currency)
        print("amount: ", self.amount)
        print("--------------------------------------------\n")
    
class User:
    instances = []
    def __init__(self, balance=0, inputs=None):
        self.balance = balance
        self.inputs = inputs if inputs is not None else {}
        User.instances.append(self)  # Add instance to the instances list

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
        print("balance: ",  self.balance)
        print("inputs: ", self.inputs)
        print("--------------------------------------------\n")

class Block:
    instances = []
    def __init__(self, timestamp, previous_hash, transactions, nonce, max_transactions, is_full):
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.max_transactions = max_transactions
        self.is_full = is_full
        Block.instances.append(self)  # Add instance to the instances list
      
    def compute_hash(self):
        block_string = f"{self.timestamp}{''.join([item for item in self.transactions])}{self.previous_hash}{self.nonce}"
        hash_object = hashlib.sha256()
        hash_object.update(block_string.encode())
        hex_digest = hash_object.hexdigest()
        return hex_digest
    
    def display_info(self):
        print("\n--------------------------------------------")
        print("Timestamp: ", self.timestamp)
        print("transactions: ", self.transactions)
        print("Previous Hash: ", self.previous_hash)
        print("Current Hash: ", self.compute_hash())
        print("Nonce: ", self.nonce)
        print("max_transactions: ", self.max_transactions)
        print("--------------------------------------------\n")