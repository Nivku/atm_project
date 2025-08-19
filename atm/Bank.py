# bank.py
import shortuuid
from .account import Account

class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, initial_balance=0):
        account_id = shortuuid.uuid()[:10]  # unique, short, readable
        new_account = Account(account_id, initial_balance)
        self.accounts[account_id] = new_account
        return new_account


    def get_account_balance(self, account_id):
        account = self.accounts.get(account_id)
        if account:
            return account.balance
        else:
            return None

    def withdraw_money_from_account(self, account_id, amount):
        account = self.accounts.get(account_id)
        if account:
            return account.withdraw(amount)
        else:
            return None

    def deposit_money_to_account(self, account_id, amount):
        account = self.accounts.get(account_id)
        if account:
            return account.deposit(amount)
        else:
            return None
