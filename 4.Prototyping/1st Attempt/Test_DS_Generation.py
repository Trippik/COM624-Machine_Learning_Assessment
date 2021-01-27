import mysql.connector
import pandas as pd

#Function to read data from database
def query_db(query):
    db = mysql.connector.connect(
        host="192.168.40.20",
        user="test",
        password="test",
        database="financial_data"
    )
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return(result)

def random_product_selection(no_products):
    query = "SELECT id FROM product ORDER BY RAND() LIMIT {}"
    query = query.format(str(no_products))
    results = query_db(query)
    return(results)

def generate_dataset(products, early_date):
    query = """SELECT
product_values.id,
product.product_name,
product.product_type,
product_values.open_value,
product_values.close_value,
product_values.high_value,
product_values.low_value,
currency.currency_name,
ROUND((product_values.close_value - product_values.open_value), 2) AS "Daily Return",
ROUND((product_values.high_value - product_values.low_value), 2) AS "Daily Range",
ROUND((((product_values.close_value - product_values.open_value) / product_values.open_value) * 100),2) AS "Percentage Daily Return"
FROM product_values
LEFT JOIN product ON product_values.product = product.id
LEFT JOIN currency ON product.currency = currency.id
WHERE (product_values.record_date > '{}')
AND 
(product.id = {})"""
    product_clause = ""
    for item in products:
        for product in item:
            product_clause = product_clause + str(product) + " OR "
    product_clause = product_clause[:-4]
    query = query.format(early_date, product_clause)
    print(query)

print("Please input desired number of products")
target_products = int(input())
print("Please input earliest date for product record (YYYY-MM-DD)")
date = input()
products = random_product_selection(target_products)
generate_dataset(products, date)