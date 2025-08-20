import pytest
from client.atm import Atm
import os
import json

SERVER_URL = "https://atm-project-812779890687.me-west1.run.app"

# Load accounts from JSON once for test reference
db_path = os.path.join(os.path.dirname(__file__), "..", "data", "accounts.json")
with open(db_path, "r") as f:
    data = json.load(f)
accounts = data.get("accounts", [])[:10]  # first 5 accounts



@pytest.fixture
def atm():
    """Return a new ATM instance for each test."""
    return Atm(server=SERVER_URL)



def test_deposit(atm):
    """Test depositing valid amount"""
    for acc in accounts:

        balance_before = atm.get_balance(acc["Account_Number"])
        deposit_amount = 100
        data, status = atm.deposit(acc["Account_Number"], deposit_amount)
        assert status == 200

        assert data["balance"] ==  pytest.approx(balance_before + 100)


def test_withdraw_success(atm):
    """Test withdrawing valid amount"""
    for acc in accounts:
        deposit_amount = 200
        balance_before = atm.get_balance(acc["Account_Number"])
        atm.deposit(acc["Account_Number"], deposit_amount)

        withdraw_amount = 150
        data, status = atm.withdraw(acc["Account_Number"], withdraw_amount)
        assert status == 200
        assert data["balance"] ==pytest.approx(balance_before + 50)




def test_deposit_validation(atm):
    """Test depositing and withdrawing with invalid inputs"""
    for acc in accounts:
        # Deposit negative amount
        data, status = atm.deposit(acc["Account_Number"], -100)
        assert status == 400

        # Deposit non-numeric amount
        data, status = atm.deposit(acc["Account_Number"], "abc")
        assert status == 400


def test_withdraw_validation(atm):
    """Test depositing and withdrawing with invalid inputs"""
    for acc in accounts:
        # Withdraw negative amount
        data, status = atm.withdraw(acc["Account_Number"], -50)
        assert status == 400

        # Withdraw non-numeric amount
        data, status = atm.withdraw(acc["Account_Number"], "xyz")
        assert status == 400


def test_withdraw_insufficient_funds(atm):
    """Test withdrawing an amount larger than the current balance."""
    for acc in accounts:
        # Get the current balance
        initial_balance = atm.get_balance(acc["Account_Number"])

        large_amount = initial_balance + 100

        # Attempt to withdraw the large amount
        data, status = atm.withdraw(acc["Account_Number"], large_amount)

        # Assert that the request failed with a 400 status code
        assert status == 400


def test_invalid_account(atm):
    """Test getting balance and deposit/withdraw with invalid account"""
    invalid_account = "invalid123"
    balance = atm.get_balance(invalid_account)
    assert balance is None

    data, status = atm.deposit(invalid_account, 100)
    assert status == 404

    data, status = atm.withdraw(invalid_account, 100)
    assert status == 404




