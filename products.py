import json

def main():
    while True:
        print("Enter the operation you want to do in IMS:")
        print("1. View Products")
        print("2. Add Product")
        print("3. Remove Product")
        print("4. Search for a product")
        print("5. Edit Product")
        print("6. Check Low Stock")
        print("7. Make an Inventory Report")
        print("8. Exit")
        choice = int(input("Enter your choice: "))
        user_choice(choice)

def user_choice(choice):
    if choice == 1:
        view_products()           

    elif choice == 2:
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))
        add_product(name, price, quantity)

    elif choice == 3:
        view_products()
        delete_product()

    elif choice == 4:
        product_search()

    elif choice == 5:
        view_products()
        product_id = int(input("Enter product ID to edit: "))
        new_name = input("Enter new name (press Enter to not edit name): ")
        new_price = float(input("Enter new price (press Enter to not edit price): "))
        new_quantity = int(input("Enter new quantity (press Enter to not edit quantity): "))
        update_product(product_id, new_name, new_price, new_quantity)

    elif choice == 6:
        check_low_stock()

    elif choice == 8:
        print("Exiting program. Goodbye!")
    
    else:
        print("Please choose an appropriate option from the above list")
        main()

def view_products():
    f = open("products.json", "r")
    products = json.load(f)
    print("ID\tName\tPrice\tQuantity")
    for product in products:
        print(f"{product['id']}\t{product['name']}\t{product['price']}\t{product['quantity']}")

def add_product(name, price, quantity):
    product = {
        "name": name,
        "price": price,
        "quantity": quantity
    }
    f = open("products.json", "r")
    products = json.load(f)
    products.append(product)
    f = open("products.json", "w")
    json.dump(products, f, indent = 4)
    f.close()
    print("Product added successfully!")

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
                print("Product deleted successfully!")
                break
            else:
                print("Product not found!")
                break
    else:
        print("Please choose 1 or 2")
    f = open("products.json", "w")
    json.dump(products, f, indent = 4) 
    f.close()

def product_search():
    search_by = int(input("Do you want to search by Name or by ID?(Please choose 1 or 2)\n1.Search by Name.\n2.Search by ID.\nAnswer: "))
    if search_by == 1:
        product_name = input("Enter the name of the product: ")
        search_by_name(product_name)
    elif search_by == 2:
        product_id = int(input("Enter the ID of the product: "))
        search_by_id(product_id)
    else:
        print("Please choose 1 or 2")
        user_choice()

def search_by_name(name):
    f = open("products.json", "r")
    products = json.load(f)
    for product in products:
        if product['name'] == name:
            print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}, Quantity: {product['quantity']}")
            break
        else:
            print("No products found with that name")
            break
    f.close()

def search_by_id(id):
    f = open("products.json", "r")
    products = json.load(f)
    for product in products:
        if product['id'] == id:
            print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}, Quantity: {product['quantity']}")
            break
        else:
            print("No products found with that id")
            break
    f.close()

def update_product(product_id, new_name=None, new_price=None, new_quantity=None):
    f = open("products.json","r")
    products = json.load(f)
    for product in products:
        if product['id'] == product_id:
            if new_name is not None:
                product['name'] = new_name
            if new_price is not None:
                product['price'] = new_price
            if new_quantity is not None:
                product['quantity'] = new_quantity
            break
        else:
            print("No product with that ID was found")

    f = open("products.json", "w")
    json.dump(products, f, indent = 4)
    f.close()

def check_low_stock():
    f = open("products.json", "r")
    products = json.load(f)
    low_stock_products = []
    print("\n--- Low Stock Products ---")
    for product in products:
        if product['quantity'] < 5:
            low_stock_products.append(product)
    if low_stock_products:
        print(f"ID\tName\tQuantity")
        for product in low_stock_products:
            print(f"{product['id']}\t{product['name']}\t{product['quantity']}")
    else:
        print("   No low stock products   ")

def notify_low_stock(threshold=5):
    f = open("products.json", "r")
    products = json.load(f)

    low_stock_products = []

    for product in products:
        if product['quantity'] < threshold:
            low_stock_products.append(product)

    if low_stock_products:
        print(f"Products with stock below {threshold}:")
        print("ID\tName\tPrice\tQuantity")
        for product in low_stock_products:
            print(f"{product['id']}\t{product['name']}\t{product['price']}\t{product['quantity']}")
    else:
        print(f"All products have stock above the threshold of {threshold}.")


def sell_item():
    user_sell = input("Do you want to search for a specific product or to view all products?(Choose 1 or 2)\n1.Search for a specific product\n2.View all products\n3.Exit\nAnswer: ")
    if user_sell == 1:
        product_search()
    elif user_sell == 2:
        view_products()


    elif user_sell == 3:
        print("Exiting program. Goodbye!")
        exit()

    else:
        print("Please choose 1 or 2, or 3 for exiting")
        sell_item()

    # do u want to search for an item or view all products?
    # if found item
    # choose quantity
    # quantity - 1










main()
# notify_low_stock(7)






# elif choice == 7:
    #     make_inventory_report()
    #     print("Inventory report has been generated.")
    



# def make_inventory_report():

