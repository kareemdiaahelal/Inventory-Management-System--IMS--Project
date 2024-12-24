
import json
from termcolor import colored
import auth
import Report
DATA_FILE = 'products.json'
def main():
    while True:
        print("Enter the operation you want to do in IMS:")
        print("1. View Products")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Search for a product")
        print("5. Edit Product")
        print("6. sell product") # for a single product
        print("7. Make an Inventory Report")
        print("8. Exit")
        choice = int(input("Enter your choice: "))
        user_choice(choice)

def user_choice(choice):
    if choice == 1:
        products = role_product_view() 
        print(products)         

    elif choice == 2:
        try:
            name = input("Enter product name: ")

            # Handling price input
            price = float(input("Enter product price: "))
            if price < 0:
                raise ValueError("Price cannot be negative.")

            # Handling quantity input
            quantity = int(input("Enter product quantity: "))
            if quantity < 0:
                raise ValueError("Quantity cannot be negative.")

            add_product(name, price, quantity)

        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

    elif choice == 3:
        view_products()
        delete_product()

    elif choice == 4:
        product_search()

    elif choice == 5:
        view_products()
        product_id = int(input("Enter product ID to edit: "))
        new_name = input("Enter new name (press Enter to not edit name): ")
        new_price =  float(input("Enter new price (press Enter to not edit price): "))
        new_quantity = int(input("Enter new quantity (press Enter to not edit quantity): "))
        update_product(product_id, new_name, new_price, new_quantity)

    elif choice == 6:
        sell_item()
    elif choice==7:
        file_name = "products.html"
        products_data=view_products("r")
        Report.create_report(products_data,file_name,"products")
    elif choice == 8:
        print("Exiting program. Goodbye!")
    
    else:
        print("Please choose an appropriate option from the above list")
        main()


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

def role_product_view():
    products = view_products()
    if auth.is_admin():
        return products
    else:
        return list(filter(lambda product: product.get('createdBy') == auth.current_user['email'], products))

def write_products(products):
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(products, file, indent=4)
    except Exception as e:
        print(colored(f"Error writing to {DATA_FILE}: {str(e)}", "red"))

def edit_product(new_product):
    print(new_product)
    products = view_products('r')
    for product in products:
        if product['id'] == new_product['id']:
            index=products.index(product)
            products[index]= new_product
        else:
            print(colored("product not updated .",'red'))
    write_products(products)
    print(colored("product updated successfully.",'green'))



def add_product(name, price, quantity):
    products = view_products('w')
    product = {
        "name": name,
        "price": price,
        "quantity": quantity
    }
    product['id'] = len(products) + 1
    product['createdBy'] = auth.current_user['email']
    products.append(product)
    write_products(products)
    print(colored("Product added successfully!",'green'))

def delete_product():
    f = open("products.json", "r")
    products = json.load(f)
    delete_by = int(input("Do you want to delete by name or by ID?(Please choose 1 or 2)\n1.Delete by Name.\n2.Delete by ID.\nAnswer: "))
    if delete_by == 1:
        product_name = input("Enter the name of the product: ")
        for product in products:
            if product['name'] == product_name:
                products.remove(product)
                print("Product deleted successfully!")
                break
            else:
                print("Product not found!")
                break
    elif delete_by == 2:
        product_id = int(input("Enter the ID of the product: "))
        for product in products:
            if product['id'] == product_id:
                products.remove(product)
                print(colored("Product deleted successfully!",'green'))
                break
            else:
                print(colored("Product not found!",'red'))
                break
    else:
        print(colored("Please choose 1 or 2",'yellow'))
    write_products(products)

def product_search():
    search_by = int(input("Do you want to search by Name or by ID?(Please choose 1 or 2)\n1.Search by Name.\n2.Search by ID.\nAnswer: "))
    if search_by == 1:
        product_name = input("Enter the name of the product: ").strip()
        return search_by_name(product_name)
    elif search_by == 2:
        product_id = int(input("Enter the ID of the product: "))
        return search_by_id(product_id)
    else:
        print("Please choose 1 or 2")
        user_choice()

def search_by_name(name):
    products = view_products()
    for product in products:
        if product['name'].lower() == name.lower():  # Make search case-insensitive
            print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}, Quantity: {product['quantity']}")
            return product
    print("No products found with that name")
    return None

def search_by_id(id):
    products = view_products('r')
    for product in products:
        if product['id'] == id:
            print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}, Quantity: {product['quantity']}")
            return product
        else:
            print("No products found with that id")
            break

def update_product(product_id, new_name=None, new_price=None, new_quantity=None):
    product= search_by_id(product_id)
    if not product:
            print("prouct is not found")
            return 
    if new_name is not None:
        product['name'] = new_name
    if new_price is not None:
        product['price'] = new_price
    if new_quantity is not None:
        product['quantity'] = new_quantity 

          
    edit_product(product)
         
def sell_item():
    products = view_products()
    user_product = product_search()  # Find the product to sell

    if user_product:  # If the product is found
        try:
            quantity = int(input("Enter the quantity you want to sell: "))

            if quantity > user_product['quantity']:
                print(colored("You cannot sell this product with this quantity.", 'yellow'))
                return

            # Calculate the remaining quantity
            remaining_quantity = user_product['quantity'] - quantity

            # Warn if the remaining quantity is at or below the threshold
            if remaining_quantity <= 5:
                choice = input(
                    colored(
                        f"You're going to reach the threshold. The product quantity will be {remaining_quantity} if you proceed.\n"
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

            # Update the product quantity and save to the file
            index = products.index(user_product)
            products[index]['quantity'] = remaining_quantity
            write_products(products)

            print(colored(f"Product sold successfully with quantity: {quantity}.", 'green'))

        except ValueError:
            print(colored("Invalid input. Please enter a valid number for the quantity.", 'red'))
    else:
        print(colored("Product not found.", 'red'))


if __name__ == "__main__":
    main()

