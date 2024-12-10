import json

# Initialize the products list
products = []

# Load products from a file
def load_products():
    global products
    try:
        with open("products.json", "w") as file:
            products = json.load(file)
    except FileNotFoundError:
        products = []

# Save products to a file
def save_products():
    with open("products.json", "w") as file:
        json.dump(products, file, indent=4)

# Create (Add a new product)
def add_product(name, price, quantity):
    product = {
        'id': len(products) + 1,
        'name': name,
        'price': price,
        'quantity': quantity
    }
    products.append(product)
    save_products()
    print(f"Product '{name}' added successfully!")

# Read (View all products)
def view_products():
    if not products:
        print("No products found.")
    else:
        print("\n--- Product Inventory ---")
        for product in products:
            print(
                f"ID: {product['id']}, Name: {product['name']}, "
                f"Price: ${product['price']:.2f}, Quantity: {product['quantity']}"
            )

# Update (Edit product details by ID)
def edit_product(product_id, new_name=None, new_price=None, new_quantity=None):
    for product in products:
        if product['id'] == product_id:
            if new_name:
                product['name'] = new_name
            if new_price:
                product['price'] = new_price
            if new_quantity:
                product['quantity'] = new_quantity
            save_products()
            print(f"Product ID {product_id} updated successfully!")
            return
    print(f"Product ID {product_id} not found.")

# Delete (Remove product by ID)
def delete_product(product_id):
    global products
    products = [product for product in products if product['id'] != product_id]
    save_products()
    print(f"Product ID {product_id} deleted successfully!")

# Notify when stock is low
def check_low_stock(threshold=5):
    print("\n--- Low Stock Products ---")
    low_stock = [product for product in products if product['quantity'] < threshold]
    if low_stock:
        for product in low_stock:
            print(
                f"ID: {product['id']}, Name: {product['name']}, "
                f"Quantity: {product['quantity']} (Below Threshold)"
            )
    else:
        print("No products are below the threshold.")

# Load products when the script starts
load_products()

# Example usage
if __name__ == "__main__":
    while True:
        print("\n--- Product Inventory Management ---")
        print("1. Add Product")
        print("2. View Products")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. Check Low Stock")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            add_product(name, price, quantity)
        elif choice == "2":
            view_products()
        elif choice == "3":
            product_id = int(input("Enter product ID to edit: "))
            new_name = input("Enter new name (leave blank to skip): ")
            new_price = input("Enter new price (leave blank to skip): ")
            new_quantity = input("Enter new quantity (leave blank to skip): ")
            
            edit_product(
                product_id,
                new_name if new_name else None,
                float(new_price) if new_price else None,
                int(new_quantity) if new_quantity else None
            )
        elif choice == "4":
            product_id = int(input("Enter product ID to delete: "))
            delete_product(product_id)
        elif choice == "5":
            threshold = int(input("Enter low stock threshold (default is 5): "))
            check_low_stock(threshold)
        elif choice == "6":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")
