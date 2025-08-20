


class AccountService:
    """
    A service class for managing bank account operations.
    """

    def __init__(self, db):
        """
        Initialize the AccountService with a database connection.

        :param db: The database object for account operations
        """
        self.account_db = db

    def get_account_balance(self, account_number):
        """
        Retrieve the balance of a given account.

        :param account_number: The account number to check
        :return: The account balance if the account exists, None otherwise
        """
        account = self.account_db.get_account(account_number)
        if not account:
            return None
        return account[1]

    def deposit_to_account(self, account_number, amount):
        """
        Deposit money into a given account.

        :param account_number: The account number to deposit into
        :param amount: The amount to deposit
        :return: A tuple (success, message)
                 - If successful: (True, "Deposit successful.")
                 - If account doesn't exist: (None, None)
                 - If amount is invalid: (False, error message)
        """

        account = self.account_db.get_account(account_number)
        if not account:
            return None
        if not isinstance(amount, (int, float)):
            return False, "Amount must be a number"
        if amount <= 0:
            return False, "Deposit must be positive"

        self.account_db.update_account(account_number, account[1] + amount)
        return True, f"Deposit successful."

    def withdraw_from_account(self, account_number, amount):
        """
        Withdraw money from a given account.

        :param account_number: The account number to withdraw from
        :param amount: The amount to withdraw
        :return: A tuple (success, message)
                 - If successful: (True, "Withdrawal successful.")
                 - If account doesn't exist: (None, None)
                 - If amount is invalid or insufficient funds: (False, error message)
        """
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
