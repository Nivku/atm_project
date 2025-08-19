# account.py
class Account:
    def __init__(self, account_id, initial_balance=0):
        self.account_id = account_id
        self.balance = initial_balance

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount <= 0:
            return False, "Deposit must be positive"
        self.balance += amount
        return True, f"Deposit successful."


    def withdraw(self, amount):
        if amount <= 0:
            return False, "Withdrawal must be positive"
        if amount > self.balance:
            return False, "Insufficient funds"
        self.balance -= amount
        return True, f"Withdrawal successful. "
