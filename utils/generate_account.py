# utils/generate_accounts.py
import json
import os
import shortuuid
import random


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "accounts.json")

def generate_accounts(num_accounts=100):
    accounts = []
    for _ in range(num_accounts):
        account_number = shortuuid.uuid()[:10]
        balance = round(random.uniform(100, 10000), 2)
        accounts.append({
            "Account_Number": account_number,
            "Balance": balance
        })

    data = {"accounts": accounts}

    # Ensure data folder exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    # Save JSON
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Generated {num_accounts} accounts in {DATA_FILE}")

if __name__ == "__main__":
    generate_accounts()
