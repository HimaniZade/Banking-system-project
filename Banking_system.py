import random
from datetime import datetime

# Stores all bank accounts
accounts = {}


# -----------------------------
# Utility Functions
# -----------------------------

def generate_account_number():
    """Generate a unique 10-digit account number."""
    while True:
        account_number = str(random.randint(1000000000, 9999999999))

        if account_number not in accounts:
            return account_number


def get_current_time():
    """Return current date and time."""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def add_transaction(account_number, transaction_type, amount, details=""):
    """Add a transaction to account history."""
    transaction = {
        "type": transaction_type,
        "amount": amount,
        "date": get_current_time(),
        "details": details
    }

    accounts[account_number]["transactions"].append(transaction)


# -----------------------------
# Create Account
# -----------------------------

def create_account():
    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter your name: ").strip()
    phone = input("Enter your phone number: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    if not phone.isdigit() or len(phone) != 10:
        print("Please enter a valid 10-digit phone number.")
        return

    pin = input("Create a 4-digit PIN: ").strip()

    if not pin.isdigit() or len(pin) != 4:
        print("PIN must contain exactly 4 digits.")
        return

    confirm_pin = input("Confirm your PIN: ").strip()

    if pin != confirm_pin:
        print("PINs do not match.")
        return

    account_number = generate_account_number()

    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }

    print("\nAccount created successfully!")
    print("Your Account Number:", account_number)
    print("Please remember your account number and PIN.")


# -----------------------------
# Login
# -----------------------------

def login():
    print("\n========== LOGIN ==========")

    account_number = input("Enter Account Number: ").strip()
    pin = input("Enter PIN: ").strip()

    if account_number not in accounts:
        print("Account not found.")
        return

    if accounts[account_number]["pin"] != pin:
        print("Incorrect PIN.")
        return

    print("\nLogin successful!")
    print("Welcome,", accounts[account_number]["name"])

    account_menu(account_number)


# -----------------------------
# Check Balance
# -----------------------------

def check_balance(account_number):
    balance = accounts[account_number]["balance"]

    print("\n========== ACCOUNT BALANCE ==========")
    print(f"Current Balance: ₹{balance:.2f}")


# -----------------------------
# Deposit
# -----------------------------

def deposit(account_number):
    print("\n========== DEPOSIT MONEY ==========")

    amount_input = input("Enter amount to deposit: ").strip()

    try:
        amount = float(amount_input)
    except ValueError:
        print("Please enter a valid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    accounts[account_number]["balance"] += amount

    add_transaction(
        account_number,
        "Deposit",
        amount
    )

    print(f"₹{amount:.2f} deposited successfully.")
    print(f"New Balance: ₹{accounts[account_number]['balance']:.2f}")


# -----------------------------
# Withdraw
# -----------------------------

def withdraw(account_number):
    print("\n========== WITHDRAW MONEY ==========")

    amount_input = input("Enter amount to withdraw: ").strip()

    try:
        amount = float(amount_input)
    except ValueError:
        print("Please enter a valid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    balance = accounts[account_number]["balance"]

    if amount > balance:
        print("Insufficient balance.")
        return

    accounts[account_number]["balance"] -= amount

    add_transaction(
        account_number,
        "Withdrawal",
        amount
    )

    print(f"₹{amount:.2f} withdrawn successfully.")
    print(f"Remaining Balance: ₹{accounts[account_number]['balance']:.2f}")


# -----------------------------
# Transfer Money
# -----------------------------

def transfer_money(account_number):
    print("\n========== TRANSFER MONEY ==========")

    receiver = input("Enter receiver Account Number: ").strip()

    if receiver not in accounts:
        print("Receiver account not found.")
        return

    if receiver == account_number:
        print("You cannot transfer money to your own account.")
        return

    amount_input = input("Enter amount to transfer: ").strip()

    try:
        amount = float(amount_input)
    except ValueError:
        print("Please enter a valid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if amount > accounts[account_number]["balance"]:
        print("Insufficient balance.")
        return

    # Deduct from sender
    accounts[account_number]["balance"] -= amount

    # Add to receiver
    accounts[receiver]["balance"] += amount

    # Sender transaction
    add_transaction(
        account_number,
        "Transfer Sent",
        amount,
        f"To Account: {receiver}"
    )

    # Receiver transaction
    add_transaction(
        receiver,
        "Transfer Received",
        amount,
        f"From Account: {account_number}"
    )

    print("\nTransfer successful!")
    print(f"₹{amount:.2f} transferred to Account {receiver}.")
    print(f"Your new balance: ₹{accounts[account_number]['balance']:.2f}")


# -----------------------------
# Transaction History
# -----------------------------

def transaction_history(account_number):
    print("\n========== TRANSACTION HISTORY ==========")

    transactions = accounts[account_number]["transactions"]

    if not transactions:
        print("No transactions found.")
        return

    for index, transaction in enumerate(transactions, start=1):
        print(f"\nTransaction {index}")
        print("Type   :", transaction["type"])
        print("Amount : ₹{:.2f}".format(transaction["amount"]))
        print("Date   :", transaction["date"])

        if transaction["details"]:
            print("Details:", transaction["details"])


# -----------------------------
# Change PIN
# -----------------------------

def change_pin(account_number):
    print("\n========== CHANGE PIN ==========")

    old_pin = input("Enter old PIN: ").strip()

    if old_pin != accounts[account_number]["pin"]:
        print("Incorrect old PIN.")
        return

    new_pin = input("Enter new 4-digit PIN: ").strip()

    if not new_pin.isdigit() or len(new_pin) != 4:
        print("PIN must contain exactly 4 digits.")
        return

    confirm_pin = input("Confirm new PIN: ").strip()

    if new_pin != confirm_pin:
        print("PINs do not match.")
        return

    if new_pin == old_pin:
        print("New PIN must be different from the old PIN.")
        return

    accounts[account_number]["pin"] = new_pin

    print("PIN changed successfully.")


# -----------------------------
# Account Menu
# -----------------------------

def account_menu(account_number):

    while True:
        print("\n")
        print("====================================")
        print("          ACCOUNT MENU")
        print("====================================")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")
        print("====================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            check_balance(account_number)

        elif choice == "2":
            deposit(account_number)

        elif choice == "3":
            withdraw(account_number)

        elif choice == "4":
            transfer_money(account_number)

        elif choice == "5":
            transaction_history(account_number)

        elif choice == "6":
            change_pin(account_number)

        elif choice == "7":
            print("\nLogged out successfully.")
            break

        else:
            print("Invalid choice. Please try again.")


# -----------------------------
# Main Menu
# -----------------------------

def main():

    while True:
        print("\n")
        print("====================================")
        print("         BANKING SYSTEM")
        print("====================================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("====================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account()

        elif choice == "2":
            login()

        elif choice == "3":
            print("\nThank you for using the Banking System.")
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


# -----------------------------
# Program Start
# -----------------------------

if __name__ == "__main__":
    main()
