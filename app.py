# server.py
from flask import Flask, request, jsonify
from atm import  Bank

app = Flask(__name__)
bank = Bank.Bank()

# Pre-create some accounts
acc1 = bank.create_account(1000)
acc2 = bank.create_account(500)
print("Created accounts:", acc1.account_id, acc2.account_id)


@app.route("/")
def home():
    return "ATM server is running!"

@app.route("/balance/<account_id>", methods=["GET"])
def get_balance(account_id):
    balance = bank.get_account_balance(account_id)
    if not balance:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"account_id": account_id, "balance": balance})

@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.json
    account_id = data.get("account_id")
    amount = data.get("amount")
    result = bank.deposit_money_to_account(account_id,amount)

    if result is  None:
        return jsonify({"error": "Account not found"}), 404

    success, msg = result[0],result[1]
    status = 200 if success else 400
    return jsonify({"message": msg, "balance": bank.get_account_balance(account_id)}), status

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.json
    account_id = data.get("account_id")
    amount = data.get("amount")
    result = bank.withdraw_money_from_account(account_id,amount)
    if result is None:
        return jsonify({"error": "Account not found"}), 404

    success, msg = result[0], result[1]
    status = 200 if success else 400
    return jsonify({"message": msg, "balance": bank.get_account_balance(account_id)}), status

if __name__ == "__main__":
    app.run(debug=True)
