from flask import Blueprint,request, jsonify
from repository.account_db_manager import AccountDbManager
from service.account_service import AccountService
import os
from http import HTTPStatus

accounts_router = Blueprint('accounts', __name__)

## Initialize the AccountService with the AccountDbManager instance.

account_service = AccountService(AccountDbManager())



@accounts_router.route("<account_number>/balance", methods=["GET"])
def get_balance(account_number):

    balance = account_service.get_balance(account_number)

    if balance is None:
        return jsonify({"error": "Account not found"}), HTTPStatus.NOT_FOUND

    return jsonify({"account_number": account_number, "balance": balance}), HTTPStatus.OK



@accounts_router.route("<account_number>/deposit", methods=["POST"])
def deposit(account_number):
    data = request.json
    amount = data.get("amount")

    result = account_service.deposit(account_number,amount)
    if result is None:
        return jsonify({"error": "Account not found"}),HTTPStatus.NOT_FOUND

    success, msg = result[0], result[1]
    status = HTTPStatus.OK if success else HTTPStatus.BAD_REQUEST
    return jsonify({"message": msg, "balance": account_service.get_balance(account_number)}), status


@accounts_router.route("<account_number>/withdraw", methods=["POST"])
def withdraw(account_number):
    data = request.json
    amount = data.get("amount")


    result = account_service.withdraw(account_number, amount)

    if result is None:
        return jsonify({"error": "Account not found"}), HTTPStatus.NOT_FOUND


    success, msg = result[0], result[1]
    status = HTTPStatus.OK if success else HTTPStatus.BAD_REQUEST
    return jsonify({"message": msg, "balance": account_service.get_balance(account_number) }), status
