
from flask import Blueprint,request, jsonify
from repository.account_db_manager import AccountsDbManager
from service.account_service import AccountService
from http import HTTPStatus

accounts_router = Blueprint('accounts', __name__)

## Initialize the AccountService with the AccountDbManager instance.
account_service = AccountService(AccountsDbManager())



@accounts_router.route("<account_number>/balance", methods=["GET"])
def get_balance(account_number):
    """
    Retrieve the balance for a given account number.

    This function handles GET requests to fetch the balance of a specific account.
    It uses the account_service to retrieve the balance and returns the result as JSON.

    Args:
        account_number (str): The account number for which to retrieve the balance.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
            If the account is found, it returns a dictionary with the account number and balance,
            along with a 200 OK status.
            If the account is not found, it returns an error message with a 404 NOT FOUND status.
    """
    balance = account_service.get_account_balance(account_number)

    if balance is None:
        return jsonify({"error": "Account not found"}), HTTPStatus.NOT_FOUND

    return jsonify({"account_number": account_number, "balance": balance}), HTTPStatus.OK



@accounts_router.route("<account_number>/deposit", methods=["POST"])
def deposit(account_number):
    """
    Handle a deposit request for a specific account.

    This function processes a POST request to deposit money into an account.
    It retrieves the deposit amount from the JSON payload, attempts to make
    the deposit using the account service, and returns the result.

    Args:
        account_number (str): The account number to deposit money into.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
            If the account is found and the deposit is successful, it returns
            a dictionary with a success message and the updated balance, along
            with a 200 OK status.
            If the account is not found, it returns an error message with a
            404 NOT FOUND status.
            If the deposit fails (e.g., invalid amount), it returns an error
            message with a 400 BAD REQUEST status.
    """
    data = request.json
    amount = data.get("amount")

    result = account_service.deposit_to_account(account_number, amount)
    if result is None:
        return jsonify({"error": "Account not found"}),HTTPStatus.NOT_FOUND

    success, msg = result[0], result[1]
    status = HTTPStatus.OK if success else HTTPStatus.BAD_REQUEST
    return jsonify({"message": msg, "balance": account_service.get_account_balance(account_number)}), status


@accounts_router.route("<account_number>/withdraw", methods=["POST"])
def withdraw(account_number):
    """
    Handle a withdrawal request for a specific account.

    This function processes a POST request to withdraw money from an account.
    It retrieves the withdrawal amount from the JSON payload, attempts to make
    the withdrawal using the account service, and returns the result.

    Args:
        account_number (str): The account number to withdraw money from.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
            If the account is found and the withdrawal is successful, it returns
            a dictionary with a success message and the updated balance, along
            with a 200 OK status.
            If the account is not found, it returns an error message with a
            404 NOT FOUND status.
            If the withdrawal fails (e.g., insufficient funds), it returns an error
            message with a 400 BAD REQUEST status.
    """
    data = request.json
    amount = data.get("amount")


    result = account_service.withdraw_from_account(account_number, amount)

    if result is None:
        return jsonify({"error": "Account not found"}), HTTPStatus.NOT_FOUND


    success, msg = result[0], result[1]
    status = HTTPStatus.OK if success else HTTPStatus.BAD_REQUEST
    return jsonify({"message": msg, "balance": account_service.get_account_balance(account_number)}), status
