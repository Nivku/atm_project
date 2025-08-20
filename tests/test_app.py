# tests/test_atm_client.py
import pytest
from atm.atm import Atm
from server import app, db

# --- Fixture: Flask test client ---
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# --- Fixture: ATM client that uses Flask test client ---
@pytest.fixture
def atm_client(client):
    class TestATM:
        def get_account_balance(self, account_id):
            resp = client.get(f"/accounts/{account_id}/balance")
            if resp.status_code == 200:
                return resp.get_json()["balance"]
            return None

        def deposit_money_to_account(self, account_id, amount):
            resp = client.post(f"/accounts/{account_id}/deposit", json={"amount": amount})
            return resp.get_json(), resp.status_code

        def withdraw_money_from_account(self, account_id, amount):
            resp = client.post(f"/accounts/{account_id}/withdraw", json={"amount": amount})
            return resp.get_json(), resp.status_code

    return TestATM()

# --- Fixture: create accounts in DB ---
@pytest.fixture
def create_accounts():
    account_ids = []
    for i in range(5):
        initial_balance = 1000 + i * 100
        account = db.add_account(initial_balance)
        account_ids.append((account.get_account_number(), initial_balance))
        db.print_accounts()
    return account_ids

# --- Tests ---
def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"ATM server is running!" in resp.data

def test_get_balance(atm_client, create_accounts):
    for account_id, initial_balance in create_accounts:
        balance = atm_client.get_account_balance(account_id)
        assert balance == initial_balance

def test_deposit(atm_client, create_accounts):
    for account_id, initial_balance in create_accounts:
        data, status = atm_client.deposit_money_to_account(account_id, 200)
        assert status == 200
        assert "message" in data
        assert data["balance"] == initial_balance + 200

def test_withdraw_success(atm_client, create_accounts):
    for account_id, initial_balance in create_accounts:
        atm_client.deposit_money_to_account(account_id, 100)
        data, status = atm_client.withdraw_money_from_account(account_id, 150)
        assert status == 200
        expected_balance = initial_balance + 100 - 150
        assert data["balance"] == expected_balance

def test_withdraw_insufficient_funds(atm_client, create_accounts):
    for account_id, _ in create_accounts:
        data, status = atm_client.withdraw_money_from_account(account_id, 10000)
        assert status == 400
        assert "Insufficient funds" in data["message"]

def test_invalid_account(atm_client):
    fake_id = "doesnotexist"
    balance = atm_client.get_account_balance(fake_id)
    assert balance is None

    data, status = atm_client.deposit_money_to_account(fake_id, 50)
    assert status == 404

    data, status = atm_client.withdraw_money_from_account(fake_id, 50)
    assert status == 404
