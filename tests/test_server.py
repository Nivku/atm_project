# test_atm.py
import pytest
from client.atm import Atm
import os
import multiprocessing
import server
import time
import json

SERVER_URL = "https://atm-project-812779890687.me-west1.run.app"

# Load accounts from JSON once for test reference
db_path = os.path.join(os.path.dirname(__file__), "..", "data", "accounts.json")
with open(db_path, "r") as f:
    data = json.load(f)
accounts = data.get("accounts", [])[:5]  # first 5 accounts




@pytest.fixture
def atm():
    """Return a new ATM instance for each test."""
    return Atm(server=SERVER_URL)


def test_get_balance(atm):
    """Test getting valid balance"""
    for acc in accounts:
        balance = atm.get_balance(acc["Account_Number"])
        assert balance == acc["Balance"]


def test_deposit(atm):
    """Test depositing valid amount"""
    for acc in accounts:
        deposit_amount = 100
        data, status = atm.deposit(acc["Account_Number"], deposit_amount)
        assert status == 200

        # update local account balance for subsequent tests
        acc["Balance"] += deposit_amount

        assert data["balance"] == acc["Balance"]


def test_withdraw_success(atm):
    """Test withdrawing valid amount"""
    for acc in accounts:
        deposit_amount = 200
        atm.deposit(acc["Account_Number"], deposit_amount)
        acc["Balance"] += deposit_amount

        withdraw_amount = 150
        data, status = atm.withdraw(acc["Account_Number"], withdraw_amount)
        assert status == 200
        acc["Balance"] -= withdraw_amount
        assert data["balance"] == acc["Balance"]


def test_withdraw_insufficient_funds(atm):
    """Test withdrawing more than available balance"""
    for acc in accounts:
        large_amount = 10_000_000
        data, status = atm.withdraw(acc["Account_Number"], large_amount)
        assert status == 400


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


def test_invalid_account(atm):
    """Test getting balance and deposit/withdraw with invalid account"""
    invalid_account = "invalid123"
    balance = atm.get_balance(invalid_account)
    assert balance is None

    data, status = atm.deposit(invalid_account, 100)
    assert status == 404

    data, status = atm.withdraw(invalid_account, 100)
    assert status == 404


