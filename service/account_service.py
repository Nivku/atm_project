# account_service.py
# open to extension, hold the busniess logic and account details

## The DB stores data.
##The Account class stores behavior + rules around that data.
##This separation makes your code cleaner, safer, and easier to extend.

class AccountService:
    def __init__(self, db):
        self.account_db = db

    def get_balance(self, account_number):
        account = self.account_db.get_account(account_number)
        if not account:
            return None
        return account[1]

    def deposit(self, account_number, amount):
        account = self.account_db.get_account(account_number)
        if not account:
            return None
        if not isinstance(amount, (int, float)):
            return False, "Amount must be a number"
        if amount <= 0:
            return False, "Deposit must be positive"

        self.account_db.update_account(account_number, account[1] + amount)
        return True, f"Deposit successful."

    def withdraw(self, account_number, amount):
        account = self.account_db.get_account(account_number)
        if not account:
            return None

        if not isinstance(amount, (int, float)):
            return False, "Amount must be a number"
        if amount <= 0:
            return False, "Withdrawal must be positive"
        if amount > account[1]:
            return False, "Insufficient funds"
        self.account_db.update_account(account_number, account[1] - amount)
        return True, f"Withdrawal successful. "
