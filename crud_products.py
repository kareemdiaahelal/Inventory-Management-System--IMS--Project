import json
from termcolor import colored
import auth
import Report
from tabulate import tabulate

DATA_FILE = "products.json"

def main():
    while True:
        try:
            print("Enter the operation you want to do in IMS:")
            print("(1) View Products")
            print("(2) Add Product")
            print("(3) Remove Product")
            print("(4) Search for a product")
            print("(5) Edit (Update) Product")
            print("(6) sell product") # for a single product
            print("(7) Make an Inventory Report")
            print("(8) Exit")
            choice = input("Enter your choice: ")
            if choice not in ["1","2","3","4","5","6","7","8"]:
                raise ValueError
            user_choice(choice)
        except ValueError:
            print(colored("Invalid choice. Please select a number between 1 and 8.","red"))

def user_choice(choice):
    if choice == "1":
        try:
            products = role_product_view()
            if products:
                headers = ["ID", "Name", "Price", "Quantity", "Created By"]
                data = [[
                    product.get("id"), 
                    product.get("name"), 
                    product.get("price"), 
                    product.get("quantity"), 
                    product.get("createdBy")
                ] for product in products]
                print(tabulate(data, headers=headers, tablefmt="rounded_outline"))
            else:
                print(colored("No products found.", "yellow"))
        except Exception as e:
                print(colored(f"An error happened: {e}", "red"))

    elif choice == "2":
        try:
            name = input("Enter product name: ").strip()

            price = float(input("Enter product price: "))
            if price < 0:
                raise ValueError("Price cannot be negative.")

            quantity = int(input("Enter product quantity: "))
            if quantity < 0:
                raise ValueError("Quantity cannot be negative.")

            add_product(name, price, quantity)

        except ValueError as e:
            print(colored(f"Invalid input: {e}. Please try again.","light_red"))

    elif choice == "3":
        delete_product()

    elif choice == "4":
        product_search()

    elif choice == "5":
        view_products()
        product_id = int(input("Enter product ID to edit: "))
        new_name = input("Enter new name: ").strip()
        new_price =  float(input("Enter new price: "))
        new_quantity = int(input("Enter new quantity: "))
        update_product(product_id, new_name, new_price, new_quantity)

    elif choice == "6":
        sell_item()

    elif choice == "7":
        file_name = "products.html"
        products_data=view_products("r")
        Report.create_report(products_data,file_name,"products")

    elif choice == "8":
        print("Exiting program. Goodbye!")
        auth.main()

def view_products(mode='r'):
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        if mode == 'r':
            print(colored(f"Error: {DATA_FILE} not found.", "red"))
        return []
    except json.JSONDecodeError:
        print(colored(f"Error: {DATA_FILE} is not valid JSON.", "red"))
        return []

def role_product_view(): #returns all products if it's admin & returns products created by the user if it's user
    products = view_products()
    if auth.is_admin():
        return products
    else:
        return list(filter(lambda product: product.get('createdBy') == auth.current_user['email'], products))

def save_products(products):
    try:
        with open(DATA_FILE, "w") as file: 
            json.dump(products, file, indent=4)
    except Exception as e:
        print(colored(f"Error writing to {DATA_FILE}: {str(e)}", "red"))

def add_product(name, price, quantity):
    products = view_products('w')
    product = {
        'id': len(products) + 1,
        "name": name,
        "price": price,
        "quantity": quantity
    }
    if auth.current_user:
        product['createdBy'] = auth.current_user.get('email')
    else:
        print(colored("Error: No authenticated user found. Cannot add product.", "red"))
        return
    products.append(product)
    save_products(products)
    print(colored("Product added successfully!", 'green'))

def delete_product():
    products = view_products('r')
    try:
        delete_by = input("Do you want to delete by name or by ID?(Please choose 1 or 2)\n1.Delete by Name.\n2.Delete by ID.\nAnswer: ")
        if delete_by not in ["1","2"]:
            raise ValueError
    except ValueError:
        print(colored("Invalid choice! Please choose 1 or 2.","red"))
    if delete_by == "1":
        try:
            product_name = input("Enter the name of the product: ")
            product =next((product for product in products if product["name"] == product_name), None)
            if product:
                products.remove(product)
                print(colored("Product deleted successfully.","green"))
            else:
                print(colored("Product not found.","red"))
                return

        except ValueError as e:
            print(colored(f"Invalid Name : error ( {e} )","light_red"))
            return
    elif delete_by == "2":
        try:
            product_id = int(input("Enter the ID of the product: "))
            product =next((product for product in products if product["id"] == product_id), None)
            if product:
                products.remove(product)
                print(colored("Product deleted successfully.","green"))
            else:
                print(colored("Product not found.","red"))
                return

        except ValueError as e:
            print(colored(f"Invalid ID : error ( {e} )","light_red"))
            return
    
    save_products(products)

def product_search():
    try:
        search_by = input("Do you want to search by Name or by ID?(Please choose 1 or 2)\n1.Search by Name.\n2.Search by ID.\nAnswer: ").strip()
        if search_by not in ["1","2"]:
            raise ValueError
    except ValueError:
        print(colored("Invalid choice! Please choose 1 or 2.","red"))
    if search_by == "1":
        product_name = input("Enter the name of the product: ").strip()
        return search_by_name(product_name)
    elif search_by == "2":
        product_id = int(input("Enter the ID of the product: "))
        return search_by_id(product_id)

def search_by_name(name):
    products = view_products()
    for product in products:
        if product['name'].lower() == name.lower():
            headers = ["ID", "Name", "Price", "Quantity", "Created By"]
            data = [[
                    product.get("id"), 
                    product.get("name"), 
                    product.get("price"), 
                    product.get("quantity"), 
                    product.get("createdBy")
                ]]
            print(tabulate(data, headers=headers, tablefmt="rounded_outline"))   # Make search case-insensitive
            return product
    print(colored("No products found with that name","red"))
    return None

def search_by_id(id):
    products = view_products()
    for product in products:
        if product['id'] == id:
            headers = ["ID", "Name", "Price", "Quantity", "Created By"]
            data = [[
                    product.get("id"), 
                    product.get("name"), 
                    product.get("price"), 
                    product.get("quantity"), 
                    product.get("createdBy")
                ]]
            print(tabulate(data, headers=headers, tablefmt="rounded_outline"))   # Make search case-insensitive
            return product
    print(colored("No products found with that id","red"))
    return None

def update_product(product_id, new_name=None, new_price=None, new_quantity=None):
    products = view_products('r')

    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        print(colored("Product not found.", 'red'))
        return

    if new_name is not None:
        product['name'] = new_name
    if new_price is not None:
        product['price'] = new_price
    if new_quantity is not None:
        product['quantity'] = new_quantity

    index = products.index(product)
    products[index] = product

    save_products(products)
    print(colored("Product updated successfully.", 'green'))

def sell_item():
    products = view_products()
    user_product = product_search()  

    if user_product:  
        try:
            quantity = int(input("Enter the quantity you want to sell: "))

            if quantity > user_product['quantity']:
                print(colored("You cannot sell this product with this quantity.", 'yellow'))
                return

            remaining_quantity = user_product['quantity'] - quantity

            if remaining_quantity <= 5:
                choice = input(
                    colored(
                        f"You're going to reach the threshold (5). The product quantity will be {remaining_quantity} if you proceed.\n"
                        f"Choose 1 : to proceed.\nChoose 2 : to exit.\nYour choice : ",
                        'light_yellow'
                    )
                ).strip()

                if choice == "2":
                    print(colored("Transaction cancelled.", 'light_green'))
                    return
                elif choice != "1":
                    print(colored("Invalid choice. Transaction cancelled.", 'light_red'))
                    return

            index = products.index(user_product)
            products[index]['quantity'] = remaining_quantity
            save_products(products)

            print(colored(f"Product sold successfully with quantity: {quantity}.", 'green'))

        except ValueError:
            print(colored("Invalid input. Please enter a valid number for the quantity.", 'red'))
    else:
        print(colored("Product not found.", 'red'))




if __name__ == "__main__":
    main()

