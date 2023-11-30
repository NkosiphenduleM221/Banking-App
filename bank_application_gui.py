from datetime import date, timedelta
import tkinter as tk
from tkinter import messagebox
from bank_application import BankApplication  # Assuming your BankApplication class is in a separate file named 'bank_application.py'
from tkcalendar import DateEntry
import sqlite3
import PIL
from PIL import Image, ImageTk

class BankApplicationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Application")
        self.bank_app = BankApplication()
        self.logged_in = False
        self.current_user = None
        self.create_main_screen()
        self.users = {}
        

    
    def create_main_screen(self):
        
        self.root.configure(bg="lightblue")  # Change "lightblue" to your desired color
        # Load the image and resize it
        welcome_image = Image.open("logo pic.png")
        welcome_image = welcome_image.resize((200, 200), PIL.Image.Resampling.LANCZOS)  # Resizing the image
        welcome_image = ImageTk.PhotoImage(welcome_image)

        # Create a label to display the image
        self.image_label = tk.Label(self.root, image=welcome_image)
        self.image_label.image = welcome_image  # Keep a reference to avoid garbage collection
        self.image_label.pack(pady=10)

        # Create the buttons below the image
        
        
        if not self.logged_in:
            self.button_create_account = tk.Button(self.root, text="Create Account", command=self.create_account,bg="lightblue")
            self.button_login = tk.Button(self.root, text="Login", command=self.create_login_screen,bg="lightblue")
            self.button_exit = tk.Button(self.root, text="Exit", command=self.destroy,bg="lightblue")

            self.button_create_account.pack()
            self.button_login.pack()
            self.button_exit.pack()
            
        else:
            self.create_main_menu()
    def create_account(self):
        genders = ["Select", "Male", "Female", "Non-binary"]
        status = ["Select", "Employed", "Unemployed", "Student"]
        self.clear_screen()
        self.label_fullname = tk.Label(self.root, text="Full Name:",bg="lightblue")
        self.entry_fullname = tk.Entry(self.root)
        self.label_username = tk.Label(self.root, text="Username:",bg="lightblue")
        self.entry_username = tk.Entry(self.root)
        self.label_gender = tk.Label(self.root, text="Gender:",bg="lightblue")
        self.gender_var = tk.StringVar(self.root)
        self.gender_var.set(genders[0])
        self.entry_gender = tk.OptionMenu(self.root, self.gender_var, *genders)

        self.label_dob = tk.Label(self.root, text="Date of Birth:",bg="lightblue")
        self.entry_dob = DateEntry(self.root, date_pattern="dd/mm/yyyy", validate="focusout", validatecommand=self.validate_date)

        self.label_employment = tk.Label(self.root, text="Employment Status:",bg="lightblue")
        self.employment_var = tk.StringVar(self.root)
        self.employment_var.set(status[0])
        self.entry_employment = tk.OptionMenu(self.root, self.employment_var, *status)
        self.label_cellphone = tk.Label(self.root, text="Cellphone Number:",bg="lightblue")
        self.entry_cellphone = tk.Entry(self.root)
        self.label_password = tk.Label(self.root, text="Password:",bg="lightblue")
        self.entry_password = tk.Entry(self.root, show="*")
        self.label_cpassword = tk.Label(self.root, text="Confirm Password:",bg="lightblue")
        self.entry_cpassword = tk.Entry(self.root, show="*")
        self.button_create = tk.Button(self.root, text="Create", command=self.process_create_account,bg="lightblue")
        self.button_back = tk.Button(self.root, text="Back", command=self.button_back,bg="lightblue")

        self.label_fullname.pack()
        self.entry_fullname.pack()
        self.label_username.pack()
        self.entry_username.pack()
        self.label_gender.pack()
        self.entry_gender.pack()
        self.label_dob.pack()
        self.entry_dob.pack()
        self.label_employment.pack()
        self.entry_employment.pack()
        self.label_cellphone.pack()
        self.entry_cellphone.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.label_cpassword.pack()
        self.entry_cpassword.pack()
        self.button_create.pack()
        self.button_back.pack()
    
    def validate_date(self):
        try:
            selected_date = self.entry_dob.get_date()
            today = date.today()
            min_birth_date = today - timedelta(days=(16 * 365))  # 16 years ago from today

            if selected_date <= min_birth_date:
                return True
            else:
                return False
        except ValueError:
            return False

    def process_create_account(self):
        full_name = self.entry_fullname.get().strip()
        username = self.entry_username.get().strip()
        gender = self.gender_var.get()
        date_of_birth = self.entry_dob.get()
        employment_status = self.employment_var.get()
        cellphone_number = self.entry_cellphone.get().strip()
        password = self.entry_password.get().strip()
        cpassword = self.entry_cpassword.get().strip()
        date_valid = self.validate_date()  # Validate date of birth

        if not all([full_name, username, gender != "Select", date_of_birth, employment_status != "Select", cellphone_number, password, cpassword]):
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        if password != cpassword:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if not self.bank_app.validate_password(password, cpassword):
            messagebox.showerror("Error", "Password does not meet criteria.Please enter 8 or 12 characters(letters,number and special characters).")
            return
        if not self.bank_app.validate_full_name(full_name):
            messagebox.showerror("Error", "Full name does not meet criteria. Please enter letters only")
            return
        if not self.bank_app.validate_username(username):
            messagebox.showerror("Error", "Username does not meet criteria. Please enter letters and numbers only")
            return
        if not self.bank_app.validate_cellphone_number(cellphone_number):
            messagebox.showerror("Error", "Cellphone number does not meet criteria. Please enter a valid cellphone number")
            return

        if not date_valid:
            messagebox.showerror("Error", "The user must be 16 years old or older.")
            return

        try:
            # Assuming your create_account method in BankApplication now expects a single password parameter
            self.bank_app.create_account(full_name, username, gender, date_of_birth, employment_status, cellphone_number, password)
            messagebox.showinfo("Account Created", "Account created successfully!")
            self.clear_screen()
            self.create_main_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")
            




    def forgot_password(self):
        username = self.entry_username.get()
        if not username:
            messagebox.showerror("Error", "Please enter your username.")
            return

        # Fetch the full name from the BankApplication instance
        full_name = self.bank_app.get_full_name(username)

        if not full_name:
            messagebox.showerror("Error", "User not found. Please enter a valid username.")
            return

        # Generate a new password
        new_password = self.bank_app.generate_password()

        # Call the update_password method of BankApplication
        if self.bank_app.update_password(username, new_password):
        # Inform the user about the new password
            messagebox.showinfo("Password Reset", f"Hello {full_name}, your new password is: {new_password}")
        else:
            # Handle the case where password update failed
            messagebox.showerror("Error", "Password reset failed. Please contact support or try again later")




    
    def create_change_password_screen(self):
        self.clear_screen()
        self.label_old_password = tk.Label(self.root, text="Old Password:",bg="lightblue")
        self.entry_old_password = tk.Entry(self.root, show="*")
        self.label_new_password = tk.Label(self.root, text="New Password:",bg="lightblue")
        self.entry_new_password = tk.Entry(self.root, show="*")
        self.label_confirm_new_password = tk.Label(self.root, text="Confirm New Password:",bg="lightblue")
        self.entry_confirm_new_password = tk.Entry(self.root, show="*")
        self.button_change_password = tk.Button(self.root, text="Change Password", command=self.process_change_password,bg="lightblue")
        self.button_back = tk.Button(self.root, text="Back", command=self.button_back,bg="lightblue")

        self.label_old_password.pack()
        self.entry_old_password.pack()
        self.label_new_password.pack()
        self.entry_new_password.pack()
        self.label_confirm_new_password.pack()
        self.entry_confirm_new_password.pack()
        self.button_change_password.pack()
        self.button_back.pack()



    def validate_user_password(self, username, password):
        # Connect to the SQLite database (replace 'your_database.db' with your actual database file)
        connection = sqlite3.connect('bank_database.db')
        cursor = connection.cursor()

        # Execute a query to fetch the stored password for the given username
        query = "SELECT password FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        stored_password = cursor.fetchone()

        # Close the database connection
        connection.close()

        # Compare the stored password with the provided password
        return stored_password and stored_password[0] == password

    def update_password(self, username, new_password):
        # Connect to the SQLite database (replace 'your_database.db' with your actual database file)
        connection = sqlite3.connect('bank_database.db')
        cursor = connection.cursor()

        # Execute a query to update the password for the given username
        query = "UPDATE users SET password = ? WHERE username = ?"
        cursor.execute(query, (new_password, username))
        connection.commit()

        # Close the database connection
        connection.close()

        return True


    


    
    def process_change_password(self):
        old_password = self.entry_old_password.get().strip()
        new_password = self.entry_new_password.get().strip()
        confirm_new_password = self.entry_confirm_new_password.get().strip()

        # Validate that old password matches the current user's password
        if not self.bank_app.validate_password(self.current_user, old_password):
            messagebox.showerror("Error", "Incorrect old password. Please try again.")
            return

        # Validate that new password and confirm new password match
        if new_password != confirm_new_password:
            messagebox.showerror("Error", "New password and confirm new password do not match.")
            return

        # Validate the new password
        if not self.bank_app.validate_password(new_password, confirm_new_password):
            messagebox.showerror("Error", "New password does not meet criteria.")
            return

        # Update the password in the BankApplication
        if self.bank_app.update_password(self.current_user, new_password):
            messagebox.showinfo("Password Changed", "Your password has been changed successfully!")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Failed to change the password. Please try again.")


    
    
    





    def create_login_screen(self):
        self.clear_screen()
        self.label_username = tk.Label(self.root, text="Username:",bg="lightblue")
        self.entry_username = tk.Entry(self.root)
        self.label_password = tk.Label(self.root, text="Password:",bg="lightblue")
        self.entry_password = tk.Entry(self.root, show="*")
        self.button_login = tk.Button(self.root, text="Login", command=self.login,bg="lightblue")
        self.button_forgot_password = tk.Button(self.root, text="Forgot Password", command=self.forgot_password,bg="lightblue")
        self.button_back = tk.Button(self.root, text="Back", command=self.button_back,bg="lightblue")
        
        
        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.button_login.pack()
        self.button_forgot_password.pack()
        self.button_back.pack()
        self.button_forgot_password = tk.Button(self.root, text="Forgot Password", command=self.forgot_password,bg="lightblue")


    def create_main_menu(self):
        self.clear_screen()
        full_name = self.bank_app.get_full_name(self.current_user)  # Fetch full name

        if full_name:
            self.label_welcome = tk.Label(self.root, text=f"Welcome, {full_name}!",bg="lightblue")  # Display full name
            self.label_welcome.pack()
            
            welcome_image = Image.open("logo pic.png")
            welcome_image = welcome_image.resize((200, 200), PIL.Image.Resampling.LANCZOS)  # Resizing the image
            welcome_image = ImageTk.PhotoImage(welcome_image)

            # Create a label to display the image
            self.image_label = tk.Label(self.root, image=welcome_image)
            self.image_label.image = welcome_image  # Keep a reference to avoid garbage collection
            self.image_label.pack(pady=10)

            self.button_deposit = tk.Button(self.root, text="Deposit", command=self.deposit,bg="lightblue")
            self.button_withdraw = tk.Button(self.root, text="Withdraw", command=self.withdraw,bg="lightblue")
            self.button_view_balance = tk.Button(self.root, text="View Balance", command=self.view_balance,bg="lightblue")
            self.button_view_statement = tk.Button(self.root, text="View Statement", command=self.view_statement,bg="lightblue")

            self.button_change_password = tk.Button(self.root, text="Change Password", command=self.create_change_password_screen,bg="lightblue")
            self.button_change_password.pack()

            self.button_logout = tk.Button(self.root, text="Logout", command=self.logout,bg="lightblue")
        
            self.button_deposit.pack()
            self.button_withdraw.pack()
            self.button_view_balance.pack()
            self.button_view_statement.pack()
            self.button_logout.pack()
        else:
            # Handle the case when full name is not found for the user
            messagebox.showerror("Error", "User details not found.")
            self.create_main_screen()

    def deposit(self):
        self.clear_screen()
        self.label_amount = tk.Label(self.root, text="Enter amount to deposit:",bg="lightblue")
        self.entry_amount = tk.Entry(self.root)
        self.button_deposit = tk.Button(self.root, text="Deposit", command=self.process_deposit,bg="lightblue")
        self.button_back = tk.Button(self.root, text="Back", command=self.button_back,bg="lightblue")
        
        self.label_amount.pack()
        self.entry_amount.pack()
        self.button_deposit.pack()
        self.button_back.pack()

    def withdraw(self):
        self.clear_screen()
        self.label_amount = tk.Label(self.root, text="Enter amount to withdraw:",bg="lightblue")
        self.entry_amount = tk.Entry(self.root)
        self.button_withdraw = tk.Button(self.root, text="Withdraw", command=self.process_withdrawal,bg="lightblue")
        self.button_back = tk.Button(self.root, text="Back", command=self.button_back,bg="lightblue")
        
        self.label_amount.pack()
        self.entry_amount.pack()
        self.button_withdraw.pack()
        self.button_back.pack()

    def view_statement(self):
        transactions = self.bank_app.get_transaction_history()
        if transactions:
            # Displaying transactions in a new window or dialog
            statement_window = tk.Toplevel(self.root)
            statement_window.title("Transaction History")
            statement_text = tk.Text(statement_window)
            statement_text.pack()

            for transaction in transactions:
                statement_text.insert(tk.END, f"Time: {transaction[0]}, Type: {transaction[1]}, Amount: R{transaction[2]:.2f}\n")

            statement_text.config(state=tk.DISABLED)  # Making the text read-only
        else:
            messagebox.showerror("Error", "No transactions found.")

    def view_balance(self):
        balance = self.bank_app.display_balance()
        if balance is not None:
            messagebox.showinfo("Balance", f"Current Balance for {self.current_user}: R{balance:.2f}")
        else:
            messagebox.showerror("Error", "Account not found or no user logged in.")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        login_successful = self.bank_app.login(username, password)
        if login_successful:
            self.logged_in = True
            self.current_user = username
            messagebox.showinfo("Login Successful", "You have successfully logged in!")
            self.clear_screen()
            self.create_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            
    def process_deposit(self):
        amount = float(self.entry_amount.get())
        if amount <= 0:
            messagebox.showerror("Error", "Invalid deposit amount")
        else:
            self.bank_app.deposit(amount)
            messagebox.showinfo("Success", f"Deposited: ${amount}")
            self.clear_screen()
            self.create_main_menu()

    def process_withdrawal(self):
        amount = float(self.entry_amount.get())
        if amount <= 0:
            messagebox.showerror("Error", "Invalid withdrawal amount")
        elif not self.bank_app.withdraw(amount):
            messagebox.showerror("Error", "Insufficient balance")
        else:
            messagebox.showinfo("Success", f"Withdrawn: ${amount}")
            self.clear_screen()
            self.create_main_menu()

    def logout(self):
        self.logged_in = False
        self.current_user = None
        self.clear_screen()
        self.create_main_screen()
        
    def button_back(self):
        self.clear_screen()
        self.create_main_screen()

    def destroy(self):
        self.root.destroy()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    bank_app_gui = BankApplicationGUI(root)
    bank_app_gui.start()