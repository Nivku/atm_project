# ATM Project

## Overview
This project implements a simple **ATM system** using Python and Flask.  
It allows basic operations such as:
- Checking balance
- Depositing money
- Withdrawing money

---

## Approach
I started by breaking the problem into layers:

1. **Data layer** – since we could use a local DB, I decided to create a class called `AccountDbManager.class`. This class has simple methods for managing the database. 
So at the beginning, the class loads a JSON file, which is the "db," and then inserts it into a dict to imitate a real DB that we can work with. 


2. **Service layer** – Contains the business logic for deposit, withdraw, and balance operations `AccountService.class`.
The main thinking behind it was that in the future, maybe we need to create different services for different banks, for example. 
Every `AccountService.class` can hold a different DB to work through the api of `AccountDbManager.class`. 


3. **Server layer** – A Flask server (`server.py`) that exposes REST endpoints so users (or clients) can interact with the system.
The server holds an object of `AccountService` and, through the service, the server sends requests. 


4. **Client layer** - This layer holds the api of (`Atm.class`). This class implements the methods - `get_balance`, `deposit`,`withdraw 
    The constructor of this class gets a server that it can send requests to and get back responses. 

This separation made the code cleaner, easier to test, and flexible for future changes.

---

## Design Decisions
- **Separation**:  
  I decided to encapsulate data access, business logic, and server code. Each part has its own responsibility.
    The logic behind it was to make it easy for me to debug and think about extensions in the future. 
    I have created folders for every layer to make it readable and easier to navigate.

  
- **Work with JSON**:  
I decided to imitate a DB, so in the beginning, I uploaded the `accounts.json` to the `AccountDbManager.class`, and I then created 
a dict, which was from now on the "fake" DB. All the updates were on the dict, which the `AccountDbManager` holds. In a real situation, it does not make sense, but the idea was to create 
the same structure of working with db after I loaded the JSON. 


- **Error handling**:  
  - Returning proper HTTP status codes (e.g., `404` for not found, `400` for invalid requests).  
  - Preventing overdrafts by checking the balance before withdrawal. 

---

## Challenges
- **DB handling and classes**:  
At first, I struggled with whether to create an `Account.class` and put all the business logic. It did not make sense 
since it forced me to hold a dict (dict) whose key is `Account_number` and the value of `Account.class`. I decided to cancel it since  
the work with the regular DB can't provide you object, only fields, and I wanted to be close to reality. 


- **Unique account numbers**:  
  Ensuring each account gets a unique ID requires careful handling. I considered libraries for UUIDs but decided to generate IDs programmatically. 


- **Concurrency**:  
  I thought about what happens if two withdrawals happen at the same time. While not fully solved, the design could be extended with locks or a database.


- **Tests**:  
  I had to write tests that take into account the current state of the server.
Since it runs and receives requests and the database is local, this is something that had to be taken into account because it can't be accessed from tests. 

---



# How to Run

## ATM Chatbot

I created simple command-line ATM chatbot that interacts with a remote server to manage bank accounts.
You can view balances, deposit, withdraw, and list of available accounts on the server. this is not part
of the work and I created it to make it easy to use the API of the `Atm`.

---

## Features

- List all account IDs
- Check balance for a specific account
- Deposit money into an account
- Withdraw money from an account
- Easy-to-use command-line interface

---


Install dependencies and run the Chatbot:

```bash
pip install -r requirements.txt

python chat_bot.py


````

also you can run the tests. `test_local_host.py` creates local service and tests it.
`test_server.py` using the atm Api on the server on Google cloud, the tests of the server might take 1-3 min since the
server is pretty slow.
run test:

```bash

pytest tests/ -v

```