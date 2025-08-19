# tests/test_server.py
import pytest
from server import app, bank

@pytest.fixture
def client():
    """Flask test client"""
    with app.test_client() as client:
        yield client

@pytest.fixture
def create_accounts():
    """Create 10 accounts with different initial balances"""
    account_ids = []
    for i in range(10):
        initial_balance = 1000 + i * 100  # e.g., 1000, 1100, 1200, ..., 1900
        account = bank.add_new_account(initial_balance=initial_balance)
        account_ids.append((account.get_account_id(), initial_balance))
    return account_ids

def test_home(client):
    """Test the home route"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"ATM server is running!" in response.data

def test_get_balance(client, create_accounts):
    """Test getting balance for all 10 accounts"""
    for account_id, initial_balance in create_accounts:
        response = client.get(f"/balance/{account_id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["account_id"] == account_id
        assert data["balance"] == initial_balance

def test_deposit(client, create_accounts):
    """Test depositing money into all accounts"""
    for account_id, initial_balance in create_accounts:
        response = client.post("/deposit", json={"account_id": account_id, "amount": 200})
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert data["balance"] == initial_balance + 200

def test_withdraw_success(client, create_accounts):
    """Test withdrawing money successfully from all accounts"""
    for account_id, initial_balance in create_accounts:
        # First deposit 100 to have enough balance for withdrawal test
        client.post("/deposit", json={"account_id": account_id, "amount": 100})
        response = client.post("/withdraw", json={"account_id": account_id, "amount": 150})
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert data["balance"] == initial_balance + 100 - 150  # new balance after deposit and withdrawal



def test_withdraw_insufficient_funds(client, create_accounts):
    """Test withdrawing more than balance for all accounts"""
    for account_id, _ in create_accounts:
        response = client.post("/withdraw", json={"account_id": account_id, "amount": 10000})
        assert response.status_code == 400
        data = response.get_json()
        assert "Insufficient funds" in data["message"]

def test_invalid_account(client):
    """Test operations on non-existing account"""
    fake_id = "doesnotexist"

    # Balance
    response = client.get(f"/balance/{fake_id}")
    assert response.status_code == 404

    # Deposit
    response = client.post("/deposit", json={"account_id": fake_id, "amount": 50})
    assert response.status_code == 404

    # Withdraw
    response = client.post("/withdraw", json={"account_id": fake_id, "amount": 50})
    assert response.status_code == 404
