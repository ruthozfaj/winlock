import os
import ctypes
from ctypes import wintypes
import sys
from getpass import getpass
import hashlib

# Constants
APP_TITLE = "WinLock"
PASSWORD_FILE = "winlock_password.txt"

# WinAPI functions
user32 = ctypes.WinDLL('user32', use_last_error=True)

def block_input():
    user32.BlockInput(True)

def unblock_input():
    user32.BlockInput(False)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_password(hash_pass):
    with open(PASSWORD_FILE, 'w') as file:
        file.write(hash_pass)

def verify_password(input_password):
    try:
        with open(PASSWORD_FILE, 'r') as file:
            saved_password = file.read()
            return saved_password == hash_password(input_password)
    except FileNotFoundError:
        print("No password set. Please set a new password.")
        return False

def set_password():
    password = getpass("Set a new password: ")
    confirm_password = getpass("Confirm password: ")
    if password == confirm_password:
        save_password(hash_password(password))
        print("Password set successfully.")
    else:
        print("Passwords do not match. Try again.")

def lock_application():
    app_path = input("Enter the full path of the application to lock: ")
    if os.path.isfile(app_path):
        print(f"Locking {app_path}...")
        block_input()
        input(f"{app_path} is now locked. Press Enter to unlock...")  # Simulate locking
        unblock_input()
        print(f"{app_path} is now unlocked.")
    else:
        print("Invalid application path. Please try again.")

def main():
    if not is_admin():
        print("This program requires administrative privileges. Please run as administrator.")
        sys.exit(1)

    while True:
        print("\nWinLock Menu:")
        print("1. Set/Change Password")
        print("2. Lock Application")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            set_password()
        elif choice == '2':
            if verify_password(getpass("Enter your password to unlock: ")):
                lock_application()
            else:
                print("Invalid password.")
        elif choice == '3':
            print("Exiting WinLock.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()