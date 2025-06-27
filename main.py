import sqlite3
connection = sqlite3.connect('inventory.db')
connection.execute("PRAGMA foreign_keys = ON;")
cursor = connection.cursor()

# Creates the table and its rows for suppliers, products, and product stock.
cursor.execute('''
CREATE TABLE IF NOT EXISTS suppliers (
supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
supplier_name TEXT NOT NULL, 
supplier_contact TEXT 
);
''')

connection.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products(
product_id INTEGER PRIMARY KEY AUTOINCREMENT,
products_name TEXT NOT NULL,
product_price REAL,
supplier_id INTEGER,
FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) ON DELETE CASCADE
)
''')
connection.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS product_stock(
stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
product_id INTEGER,
quantity INTEGER,
FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
)
''')

# Assigns all the tables unknown values that can later be added.
def add_supplier(supplier_name, supplier_contact):
    cursor.execute('''
    INSERT INTO suppliers (supplier_name, supplier_contact)
    Values(?, ?)
    ''', (supplier_name, supplier_contact))
    connection.commit()

def add_product(products_name, product_price, supplier_id):
    cursor.execute('''
    INSERT INTO products(products_name, product_price, supplier_id)
    VALUES(?, ?, ?)    
    ''', (products_name, product_price, supplier_id))
    connection.commit()

def add_product_stock(product_id, quantity):
    cursor.execute('''
    INSERT INTO product_stock(product_id, quantity)
    VALUES(?, ?)
    ''', (product_id, quantity))
    connection.commit()

# Lets the user input the unknown values into the tables.
add_supplier(
    supplier_name=input("What is the name of the supplier?"),
    supplier_contact=input("What is the contact of the supplier?")
)
supplier_id=cursor.lastrowid
add_product(
    products_name=input("What is the name of the product?"),
    product_price=float(input("How much does the product cost?")),
    supplier_id=supplier_id
)
product_id=cursor.lastrowid
add_product_stock(
    product_id=product_id,
    quantity=int(input("How much product is in stock?"))
)
# A function allowing the user to receive all the current table data.
def receive_inventory():
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.execute("SELECT * FROM product_stock")
    product_stock = cursor.fetchall()
    return suppliers, products, product_stock

def remove_item():
    table_to_remove = input("What table do you want to remove an item from?").lower()
    if table_to_remove == "suppliers":
        cursor.execute("SELECT * FROM suppliers")
        suppliers = cursor.fetchall()
        for supplier in suppliers:
            print(supplier)
        supplier_id_to_remove = input("What supplier_id do you want to remove?")
        cursor.execute("DELETE FROM suppliers WHERE supplier_id = ?", (supplier_id_to_remove,))
        connection.commit()
    if table_to_remove == "products":
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        for product in products:
            print(product)
        product_id_to_remove = input("What product_id do you want to remove?")
        cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id_to_remove,))
        connection.commit()
    if table_to_remove == "product_stock":
        cursor.execute("SELECT * FROM product_stock")
        product_stock = cursor.fetchall()
        for product_stock1 in product_stock:
            print(product_stock1)
        product_stock_id_to_remove = input("What stock_id do you want to remove?")
        cursor.execute("DELETE FROM product_stock WHERE stock_id = ?", (product_stock_id_to_remove,))
        connection.commit()




print(receive_inventory())

# Allows the user to update the data when they want to.
def update_inventory(suppliers, products, product_stock):
    update_question = input("Do you want to update your inventory? Yes or No").capitalize()
    if update_question == "Yes":
        update_part = input("What table do you want to update").lower()
        if update_part == 'suppliers':
            for supplier_data in suppliers:
                print(supplier_data)
                print(add_supplier)
                print(receive_inventory())
                print("This is your new updates table")
        elif update_part == 'products':
            for product_data in products:
                print(product_data)
                print(add_product)
                print(receive_inventory())
                print("This is your new updates table")
        elif update_part == 'product_stock':
            for product_stock_data in product_stock:
                print(product_stock_data)
                print(add_product_stock)
                print(receive_inventory())
                print("This is your new updates table")


read_table = input("Do you want to see your new list of suppliers, products, and product stock? Yes or No").capitalize()
if read_table == "Yes":
    suppliers, products, product_stock = receive_inventory()


