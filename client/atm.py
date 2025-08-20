import requests

class Atm:
    def __init__(self, server=None):
        """
        Initialize Bank.
        Load accounts from JSON file if provided.
        """
        self.server_url = server


    def get_account_balance(self, account_number):
        """
        Retrieve the balance of a specified account from the server.

        This function sends a GET request to the server to fetch the balance
        of the account associated with the given account number.

        Parameters:
        account_number (str): The unique identifier of the account whose balance is to be retrieved.

        Returns:
        float or None: The account balance if the request is successful (status code 200),
                       or None if the request fails or the account is not found.
        """
        
        url = f"{self.server_url}/accounts/{account_number}/balance"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["balance"]
        return None
    

    def deposit_money_to_account(self, account_number, amount):
        """
        Deposit money into a specified account.

        This function sends a POST request to the server to deposit the specified amount
        into the account associated with the given account number.

        Parameters:
        account_number (str): The unique identifier of the account to deposit money into.
        amount (float): The amount of money to deposit.

        Returns:
        tuple: A tuple containing two elements:
            - dict: The JSON response from the server, which includes either a success message
                    or an error message.
            - int: The HTTP status code of the response.

        Note:
        If the account is not found (status code 404), an error message is printed.
        Otherwise, a success message is printed.
        """
        url = f"{self.server_url}/accounts/{account_number}/deposit"
        response = requests.post(url, json={"amount": amount})
        if response.status_code == 404:
            print(response.json()["error"])
        else:
            print(response.json()["message"])
        return response.json(), response.status_code



    def withdraw_money_from_account(self, account_number, amount):
        """
        Withdraw money from a specified account.

        This function sends a POST request to the server to withdraw the specified amount
        from the account associated with the given account number.

        Parameters:
        account_number (str): The unique identifier of the account to withdraw money from.
        amount (float): The amount of money to withdraw.

        Returns:
        tuple: A tuple containing two elements:
            - dict: The JSON response from the server, which includes either a success message
                    or an error message.
            - int: The HTTP status code of the response.

        Note:
        If the account is not found (status code 404), an error message is printed.
        Otherwise, a success message is printed.
        """
        url = f"{self.server_url}/accounts/{account_number}/withdraw"
        response = requests.post(url, json={"amount": amount})
        if response.status_code == 404:
            print(response.json()["error"])
        else:
            print(response.json()["message"])
        return response.json(), response.status_code



