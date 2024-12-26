import json
import hashlib
from termcolor import colored
import crud_users
import products
import validation

DATA_FILE = "users.json"

current_user = None     

def initialize_data_file():
    try:
        with open(DATA_FILE, "r") as file:
            json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(DATA_FILE, "w") as file:
            json.dump([], file)

def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    return encrypt_password(password) == hashed_password

def generate_user_id(users):
    if users:
        return len(users) + 1
    return 1



def register():
    global current_user
    users = crud_users.read_users()

    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()
    age = input("Enter your age: ").strip()
    password = input("Enter your password: ").strip()
    role = input("Enter your role (admin/user): ").strip().lower()

    if not name or not email or not password:
        print(colored("All fields are required.", "red"))
        return
    
    if not validation.is_valid_name(name):
        print(colored("Invalid name format.", "red"))
        return
    if not validation.is_valid_email(email):
        print(colored("Invalid email format.", "red"))
        return
    if not validation.is_valid_age(age):
        print(colored("Invalid age. Age must be a positive number.", "red"))
        return
    if not validation.is_valid_password(password):
            print(colored("Invalid password format. password must be with length > 5.", "red"))
            return
    if not validation.is_valid_role(role):
            print(colored("Invalid role format.", "red"))
            return

    if any(user["email"] == email for user in users):
        print(colored("This email is already in use.", "red"))
        return

    user_id = generate_user_id(users)
    hashed_password = encrypt_password(password)

    new_user = {
        "id": user_id,
        "name": name,
        "email": email,
        "age":age,
        "password": hashed_password,
        "role": role
    }

    users.append(new_user)
    crud_users.write_users(users)
    current_user = new_user
    print(colored("Registration successful!", "green"))
    post_login_menu(new_user)



def login():
    global current_user
    users = crud_users.read_users()

    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    user = next((user for user in users if user["email"] == email), None)

    if not user:
        print(colored("No user found with this email.", "red"))
        return

    if not verify_password(password, user["password"]):
        print(colored("Incorrect password.", "red"))
        return

    current_user = user
    print(colored(f"Welcome {user['name']}! You are logged in as {user['role']}.", "light_green"))

    post_login_menu(user)


def post_login_menu(user):
    if is_admin():
        print(colored("\n====================== Admin Post-Login Menu ======================", "cyan"))
        print("1. CRUD Users")
        print("2. CRUD Products")
        print("3. Logout")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            crud_users.main()
        elif choice == "2":
            products.main()
        elif choice == "3":
            logout()
        else:
            print(colored("Invalid choice. Returning to main menu.", "red"))

    elif not is_admin():
        print(colored("\n=== User Post-Login Menu ===", "cyan"))
        print("1. CRUD Products")
        print("2. Logout")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            products.main()
        elif choice == "2":
            logout()
        else:
            print(colored("Invalid choice. Returning to main menu.", "red"))
def is_logged_in():
    return current_user is not None

def get_current_user():
    if is_logged_in():
        return current_user
    print(colored("No user is logged in.", "yellow"))
    return None

def logout():
    global current_user
    if is_logged_in():
        print(colored(f"Goodbye {current_user['name']}!", "green"))
        current_user = None
        return
    else:
        print(colored("No user is currently logged in.", "red"))

def is_admin():
    user = get_current_user()
    return user and user["role"] == "admin"

def main():
    initialize_data_file()

    while True:
        print(colored("\n====================== Login/Register System ======================", "magenta"))

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
                print(colored(f"Logged in as {user['name']} ({user['role']}).",'magenta'))
        elif choice == "4":
            logout()
        elif choice == "5":
            print("Exiting the system. Goodbye!")
            break
        else:
            print(colored("Invalid choice. Please try again.", "red"))

if __name__ == "__main__":
    main()