import json
from termcolor import colored
from tabulate import tabulate

DATA_FILE = "users.json"

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

def write_users(users):
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(users, file, indent=4)
    except Exception as e:
        print(colored(f"Error writing to {DATA_FILE}: {str(e)}", "red"))

def read_user_by_email(email):
    users = read_users()
    return next((user for user in users if user["email"] == email), None)

def update_user_by_email(email, new_data):
    users = read_users()
    user = next((user for user in users if user["email"] == email), None)

    if not user:
        print(colored("User not found.", "red"))
        return

    user.update(new_data)
    write_users(users)
    print(colored("User updated successfully.", "green"))

def update_user_by_id(user_id, new_data):
    users = read_users()
    user = next((user for user in users if user["id"] == user_id), None)

    if not user:
        print(colored("User not found.", "red"))
        return

    user.update(new_data)
    write_users(users)
    print(colored("User updated successfully.", "green"))

def delete_user_by_email(email):
    users = read_users()
    user = next((user for user in users if user["email"] == email), None)

    if not user:
        print(colored("User not found.", "red"))
        return

    users.remove(user)
    write_users(users)
    print(colored("User deleted successfully.", "green"))

def delete_user_by_id(user_id):
    users = read_users()
    user = next((user for user in users if user["id"] == user_id), None)

    if not user:
        print(colored("User not found.", "red"))
        return

    users.remove(user)
    write_users(users)
    print(colored("User deleted successfully.", "green"))

def main():
    while True:
        print(colored("\n ====================== User Management System ======================",'light_magenta'))
        print("1. View All Users")
        print("2. Find User by Email")
        print("3. Update User by Email")
        print("4. Update User by ID")
        print("5. Delete User by Email")
        print("6. Delete User by ID")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            users = read_users()
            if users:
                headers = ["ID", "Name", "Email", "Age"]
                data = [[user.get("id"), user.get("name"), user.get("email"), user.get("age")] for user in users]
                print(tabulate(data, headers=headers, tablefmt="rounded_outline"))
            else:
                print(colored("No users found.", "yellow"))

        elif choice == "2":
            email = input("Enter the user's email: ")
            user = read_user_by_email(email)
            if user:
                print(json.dumps(user, indent=4))
            else:
                print(colored("User not found.", "red"))

        elif choice == "3":
            email = input("Enter the user's email: ")
            new_data = {}
            print("Enter new data (leave blank to skip):")
            name = input("Name: ")
            if name:
                new_data["name"] = name
            age = input("Age: ")
            if age:
                new_data["age"] = age

            if new_data:
                update_user_by_email(email, new_data)
            else:
                print(colored("No updates provided.", "yellow"))

        elif choice == "4":
            user_id = input("Enter the user's ID: ")
            new_data = {}
            print("Enter new data (leave blank to skip):")
            name = input("Name: ")
            if name:
                new_data["name"] = name
            age = input("Age: ")
            if age:
                new_data["age"] = age

            if new_data:
                update_user_by_id(user_id, new_data)
            else:
                print(colored("No updates provided.", "yellow"))

        elif choice == "5":
            email = input("Enter the user's email: ")
            delete_user_by_email(email)

        elif choice == "6":
            user_id = input("Enter the user's ID: ")
            delete_user_by_id(user_id)

        elif choice == "7":
            print("Exiting User Management System.")
            break

        else:
            print(colored("Invalid choice. Please try again.", "red"))

if __name__ == "__main__":
    main()
