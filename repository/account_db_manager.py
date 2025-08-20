import json
import shortuuid
import os

class AccountDbManager:
    def __init__(self, json_file= os.path.join(os.path.dirname(__file__), "..", "data", "accounts.json")):
        """
        Initialize Bank.
        Load accounts from JSON file if provided.
        """
        self.accounts = {}
        self.json_file = json_file
        if json_file:
            self._load_accounts(json_file)

    def _load_accounts(self, json_file):
        """Load accounts from JSON into memory"""
        if not os.path.exists(json_file):
            self.accounts = {}
            return

        with open(json_file, "r") as f:
            data = json.load(f)

        for acc in data.get("accounts", []):
            account_number = acc["Account_Number"]
            balance = acc["Balance"]
            self.accounts[account_number] = balance


    def add_account(self, initial_balance=0):
        """Create a new account and persist it"""
        account_number = shortuuid.uuid()[:10]
        self.accounts[account_number] = initial_balance
        return account_number

    def get_account(self, account_number):
        """Get an account by its ID"""
        if account_number in self.accounts:
            return account_number,self.accounts[account_number]
        else:
            return None

    def update_account(self, account_number, new_balance):
        if account_number in self.accounts:
            self.accounts[account_number] = new_balance
            return True
        else:
            return False


    def print_accounts(self):
        """Print all accounts in the bank"""
        for account_number,balance in self.accounts:
            print(f"Account Number: {account_number}, Balance: {balance}")

