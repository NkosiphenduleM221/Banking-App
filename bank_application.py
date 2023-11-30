import os
import re
import sqlite3
import random
import string

class BankApplication:
    def __init__(self):
        self.db_file = "bank_database.db"
        self.logged_in = False
        self.current_user = None
        self.connection = None
        self.create_tables()

    def create_tables(self):
        self.connection = sqlite3.connect(self.db_file)
        cursor = self.connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                            id INTEGER PRIMARY KEY,
                            full_name TEXT UNIQUE,
                            username TEXT UNIQUE,
                            gender TEXT,
                            date_of_birth TEXT,
                            employment_status TEXT,
                            cellphone_number TEXT,
                            password TEXT,
                            balance REAL DEFAULT 0 )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    transaction_time TEXT DEFAULT CURRENT_TIMESTAMP, -- Change to TEXT
                    transaction_type TEXT,
                    amount REAL,
                    FOREIGN KEY(user_id) REFERENCES accounts(id))''')

        self.connection.commit()
        cursor.close()

    def create_account(self, full_name, username, gender, date_of_birth, employment_status, cellphone_number, password):
        
        if not self.validate_full_name(full_name):
            return
        
        if not self.validate_username(username):
            return
        
        if not re.match("^[a-zA-Z0-9]+$", username):
            print("Username must contain only letters and numbers.")
            return  # Exit the function if the username contains invalid characters
        
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO accounts (full_name, username, gender, date_of_birth, employment_status, cellphone_number, password)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', (full_name, username, gender, date_of_birth, employment_status, cellphone_number, password))
        self.connection.commit()
        cursor.close()

    def login(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT username, password FROM accounts WHERE username = ?''', (username,))
        user = cursor.fetchone()

        if user and user[1] == password:
            self.logged_in = True
            self.current_user = username
            return True
        else:
            return False

    def deposit(self, amount):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE accounts SET balance = balance + ? WHERE username = ?''', (amount, self.current_user))
        cursor.execute('''INSERT INTO transactions (user_id, transaction_type, amount) VALUES ((SELECT id FROM accounts WHERE username = ?), ?, ?)''', (self.current_user, "Deposit", amount))
        self.connection.commit()
        cursor.close()

    def withdraw(self, amount):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT balance FROM accounts WHERE username = ?''', (self.current_user,))
        balance = cursor.fetchone()

        if balance and balance[0] >= amount:
            cursor.execute('''UPDATE accounts SET balance = balance - ? WHERE username = ?''', (amount, self.current_user))
            cursor.execute('''INSERT INTO transactions (user_id, transaction_type, amount) VALUES ((SELECT id FROM accounts WHERE username = ?), ?, ?)''', (self.current_user, "Withdrawal", amount))
            self.connection.commit()
            cursor.close()
            return True  # Successful withdrawal
        else:
            cursor.close()
            return False  # Insufficient balance or account not found
        
    def get_transaction_history(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT transaction_time, transaction_type, amount FROM transactions
                        INNER JOIN accounts ON transactions.user_id = accounts.id
                        WHERE accounts.username = ?''', (self.current_user,))
        transactions = cursor.fetchall()
        cursor.close()
        return transactions
    
    def display_balance(self):
        if self.logged_in and self.current_user:
            cursor = self.connection.cursor()
            cursor.execute('''SELECT balance FROM accounts WHERE username = ?''', (self.current_user,))
            balance = cursor.fetchone()
            cursor.close()

            if balance is not None:  # Check if balance is found and not empty
                return balance[0]  # Return the balance value
            else:
                return 0  # Default balance if account not found
        else:
            return 0  # Default balance if no user is logged in
    
    def get_full_name(self, username):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT full_name FROM accounts WHERE username = ?''', (username,))
        full_name = cursor.fetchone()
        cursor.close()

        if full_name:
            return full_name[0]
        else:
            return None
        
    def validate_password(self, password,confirm_password):
        # Check if the password matches the specified criteria
        if (re.match("^[a-zA-Z0-9@#$%^&+=]{8,12}$", password) and confirm_password):
            return True  # Password meets criteria
        else:
            return False  # Password does not meet criteria
        
    def update_password(self, username, new_password):
        if not re.match("^[a-zA-Z0-9@#$%^&+=]{8,12}$", new_password):
            return False  # Password does not meet criteria
        
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE accounts SET password = ? WHERE username = ?''', (new_password, username))
        self.connection.commit()
        cursor.close()
        return True  # Password updated successfully
    
    def validate_full_name(self, full_name):
        # Validate full name: Ensure it contains only letters and spaces
        if re.match("^[a-zA-Z ]+$", full_name):
            return True
        else:
            print("Full name must contain only letters and spaces.")
            return False

    def validate_username(self, username):
        # Validate username: Ensure it contains only letters and numbers
        if re.match("^[a-zA-Z0-9]+$", username):
            return True
        else:
            print("Username must contain only letters and numbers.")
            return False
        
    def validate_cellphone_number(self, cellphone_number):
        # Remove any spaces or special characters from the number
        cellphone_number = ''.join(filter(str.isdigit, cellphone_number))

        # Validate cellphone number: Ensure it starts with '0' and has 10 digits
        if len(cellphone_number) == 10 and cellphone_number.startswith('0'):
            return True
        else:
            print("Cellphone number must start with '0' and have 10 digits.")
            return False


    def generate_password(self):
        password_length = random.randint(8, 12)
        characters = string.ascii_letters + string.digits + "@#$%^&+="  # Allowable characters
        generated_password = ''.join(random.choice(characters) for _ in range(password_length))
        return generated_password