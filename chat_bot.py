from client.atm import Atm
import os
import json



db_path = os.path.join(os.path.dirname(__file__),"data", "accounts.json")
with open(db_path, "r") as f:
    data = json.load(f)
accounts = data.get("accounts", [])  # first 5 accounts
account_numbers = [acc["Account_Number"] for acc in accounts]





def chatbot():
    print("=== ATM Chatbot ===")
    print("Available commands:")
    print(" show accounts      -> list all account IDs")
    print(" balance <account_number>       -> show balance of account")
    print(" deposit <account_number> <amount> -> deposit money")
    print(" withdraw <account_number> <amount> -> withdraw money")
    print(" exit               -> quit")
    print()

    atm = Atm("https://atm-project-812779890687.me-west1.run.app")
    while True:
        user_input = input("You: ").strip().split()

        if not user_input:
            continue

        cmd = user_input[0].lower()

        if cmd == "exit":
            print("Bot: Goodbye!")
            break

        elif cmd == "show":
            if len(user_input) > 1 and user_input[1] == "accounts":
                print("Bot: Accounts ->", account_numbers)
            else:
                print("Bot: Did you mean 'show accounts'?")

        elif cmd == "balance":
            if len(user_input) < 2:
                print("Bot: Please provide account number. Example: balance 101")
                continue

            account_number = (user_input[1])
            atm.get_balance(account_number)


        elif cmd == "deposit":
            if len(user_input) < 3:
                print("Bot: Usage: deposit <id> <amount>")
                continue
            account_number = (user_input[1])
            amount = (user_input[2])
            is_integer = amount.isdigit() or (amount.startswith("-") and amount[1:].isdigit())
            if not is_integer:
                print("Bot: Account number must be an integer.")
                continue

            atm.deposit(account_number, float(amount))

        elif cmd == "withdraw":
            if len(user_input) < 3:
                print("Bot: Usage: withdraw <id> <amount>")
                continue
            account_number = (user_input[1])
            amount = (user_input[2])
            is_integer = amount.isdigit() or (amount.startswith("-") and amount[1:].isdigit())
            if not is_integer:
                print("Bot: Account number must be an integer.")
                continue
            atm.withdraw(account_number, float(amount))


        else:
            print("Bot: Unknown command.")
            print("Available commands:")
            print(" show accounts      -> list all account Account_Numbers")
            print(" balance <account_number>       -> show balance of account")
            print(" deposit <account_number> <amount> -> deposit money")
            print(" withdraw <account_number> <amount> -> withdraw money")
            print(" exit               -> quit")
            print()


if __name__ == "__main__":
    chatbot()
