import json
import hashlib
from termcolor import colored
import crud_users
# File to store user data
DATA_FILE = "users.json"

# Global variable to store the logged-in user's session
current_user = None

# Initialize data file if it doesn't exist
def initialize_data_file():
    try:
        with open(DATA_FILE, "r") as file:
            json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(DATA_FILE, "w") as file:
            json.dump([], file)



# Encrypt the password (hashing with salt)
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify password by comparing hashes
def verify_password(password, hashed_password):
    return encrypt_password(password) == hashed_password

# Auto-increment ID generator
def generate_user_id(users):
    if users:
        return len(users) + 1
    return 1

# Validate email format
def is_valid_email(email):
    return "@" in email and "." in email.split("@")[-1]

# Register a new user
def register():
    users = crud_users.read_users()

    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()
    role = input("Enter your role (admin/user): ").strip().lower()

    if not name or not email or not password:
        print("All fields are required.")
        return

    if not is_valid_email(email):
        print("Invalid email format.")
        return

    if role not in ["admin", "user"]:
        print("Role must be either 'admin' or 'user'.")
        return

    if any(user["email"] == email for user in users):
        print(colored("This email already in use.", "red"))
        return

    user_id = generate_user_id(users)
    hashed_password = encrypt_password(password)

    new_user = {
        "id": user_id,
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role
    }

    users.append(new_user)
    crud_users.write_users(users)
    print(colored("Registration successful!","green"))

# Login existing user
def login():
    global current_user
    users = crud_users.read_users()

    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    user = next((user for user in users if user["email"] == email), None)

    if not user:
        print(colored("No user found with this email.","red"))
        return

    if not verify_password(password, user["password"]):
        print(colored("Incorrect password.",'red'))
        return

    current_user = user
    print(colored(f"Welcome {user['name']}! You are logged in as {user['role']}.",'light_green'))

# Check if a user is logged in
def is_logged_in():
    return current_user is not None

# Get the current user's data
def get_current_user():
    if is_logged_in():
        return current_user
    print(colored("No user is logged in.",'yellow'))
    return None

# Logout the current user
def logout():
    global current_user
    if is_logged_in():
        print(colored(f"Goodbye {current_user['name']}!",'green'))
        current_user = None
    else:
        print(colored("No user is currently logged in.",'red'))

# Main menu
def main():
    initialize_data_file()

    while True:
        print("\n=== Login/Register System ===")
        print("1. Register")
        print("2. Login")
        print("3. Check Login Status")
        print("4. Logout")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            user = get_current_user()
            if user:
                print(f"Logged in as {user['name']} ({user['role']}).")
        elif choice == "4":
            logout()
        elif choice == "5":
            print("Exiting the system. Goodbye!")
            break
        else:
            print(colored("Invalid choice. Please try again.",'red'))

if __name__ == "__main__":
    main()
