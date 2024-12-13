import json
from termcolor import colored

DATA_FILE = "users.json"

# Read users data from the file
def read_users():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(colored(f"Error: {DATA_FILE} not found.", "red"))
        return []
    except json.JSONDecodeError:
        print(colored(f"Error: {DATA_FILE} is not valid JSON.", "red"))
        return []

# Write users data to the file
def write_users(users):
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(users, file, indent=4)
    except Exception as e:
        print(colored(f"Error writing to {DATA_FILE}: {str(e)}", "red"))

# Read user by email
def read_user_by_email(email):
    users = read_users()
    return next((user for user in users if user["email"] == email), None)

# Update user by email
def update_user_by_email(email, new_data):
    users = read_users()
    user = next((user for user in users if user["email"] == email), None)

    if not user:
        print(colored("User not found.", "red"))
        return

    user.update(new_data)
    write_users(users)
    print(colored("User updated successfully.", "green"))

# Delete user by email
def delete_user_by_email(email):
    users = read_users()
    user = next((user for user in users if user["email"] == email), None)

    if not user:
        print(colored("User not found.", "red"))
        return

    users.remove(user)
    write_users(users)
    print(colored("User deleted successfully.", "green"))
