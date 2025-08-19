class Account:

    def __init__(self):
        self.__account_number = 0
        self.__account_balance = 0

    def get_balance(self):
        return self.__account_balance

    def deposit(self, amount):
        if amount > 0:
            self.__account_balance += amount
            print(f'Deposit of {amount} successful. New balance: {self.__account_balance}')
            return True

    def get_account_number(self):
        return self.__account_balance
