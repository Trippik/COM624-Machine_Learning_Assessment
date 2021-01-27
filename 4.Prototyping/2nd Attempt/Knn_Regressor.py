#Import necessary libraries
import random
import sys
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from scipy.spatial import KDTree
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt 
import mysql.connector 

#Query SQL db for data
def query_db(query):
    print("Querying DB")
    db = mysql.connector.connect(
        host="192.168.40.20",
        user="root",
        password="root_password",
        database="financial_data",
        port=3306
    )
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return(result)

def pull_data(no_values, direction):
    query = """SELECT
DATEDIFF(product_values.record_date, (SELECT MIN(record_date) FROM product_values)) AS date_rate,
product.product_type,
product.financial_exchange,
currency.id AS "currency", 
product_values.open_value,
product_values.volume,
ROUND((product_values.close_value - product_values.open_value), 2) AS "daily_return"
FROM product_values
LEFT JOIN product ON product_values.product = product.id
LEFT JOIN currency ON product.currency = currency.id
ORDER BY (product_values.record_date) {}
LIMIT {}"""
    query = query.format(direction, str(no_values))
    results = query_db(query)
    print("DB Query Complete")
    return(results)

def build_dataset(no_values, direction):
    raw_results = pull_data(no_values, direction)
    df = pd.DataFrame(columns=["date_rate", "product_type", "financial_exchange", "currency", "open_value", "volume", "daily_return"])
    for row in raw_results:
        df = df.append(pd.Series([row[0], row[1], row[2], row[3], row[4], row[5], row[6]], index = df.columns), ignore_index = True)
    return(df)

#Create training data
train_data = build_dataset(1000, "ASC")
target_train = train_data["daily_return"]
values_train = train_data[["date_rate", "product_type", "financial_exchange", "currency", "open_value", "volume"]]
print(train_data.dtypes)
input()
print("Training data generated")

#Create testing data
test_data = build_dataset(300, "DESC")
target_test = test_data["daily_return"]
values_test = test_data[["date_rate", "product_type", "financial_exchange", "currency", "open_value", "volume"]]
print("Testing data generated")

#Create model 
poly_model = SVR(kernel="poly", epsilon=.1, coef0=1)
poly_model.fit(values_train, target_train)
target_predict = poly_model.predict(values_test)
print('Coefficient of determination: %.2f'
      % r2_score(target_test, target_predict))

