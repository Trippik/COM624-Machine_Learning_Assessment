#-----IMPORT NECESSARY LIBRARIES-----
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import mysql.connector
from datetime import datetime
import datetime
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import time
from pathlib import Path
from joblib import dump, load

#-----CORE FUNCTIONS FOR SQL ACCESS-----
#Function to read data from database
def query_db(query):
    db = mysql.connector.connect(
        host="192.168.40.20",
        user="root",
        password="root_password",
        database="financial_data"
    )
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return(result)

#Function to write data to database
def update_db(query):
    db = mysql.connector.connect(
        host="192.168.40.20",
        user="root",
        password="root_password",
        database="financial_data"
    )
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()

#-----GENERAL FUNCTIONS-----
def to_seconds(date):
    return time.mktime(date.timetuple())

#-----RETURNING TARGET PRODUCTS-----
#Return tuple of targets that are active
def active_products(target_date):
    query = "SELECT product FROM product_values WHERE record_date = '{}'"
    query = query.format(target_date)
    results = query_db(query)
    return(results)

#Return tuple of products whose value has increased over n number of days
def increasing_products(year, month, day, day_delta):
    today = datetime.datetime(year, month, day)
    days = datetime.timedelta(day_delta)
    target_date = today - days
    target_tup = ()
    print(str(len(active_products(today.strftime("%Y-%m-%d")))) + " out of 48893 products active")
    for item in (active_products(today.strftime("%Y-%m-%d"))):
        query = """SELECT 
((SELECT open_value FROM product_values WHERE product = {} AND record_date = "{}") - (SELECT open_value FROM product_values WHERE product = {} AND record_date = "{}"))
FROM 
product_values
LIMIT 1"""
        query = query.format(item[0], (today.strftime("%Y-%m-%d")), item[0], (target_date.strftime("%Y-%m-%d")))
        try:
            result = query_db(query)
            for row in result:
                if(row[0] > 0):
                    target_tup = target_tup + (item[0],)
        except:
            pass
    print(str(len(target_tup)) + " products highlighted out of " + str(len(active_products(today.strftime("%Y-%m-%d")))) + " active products")
    return(target_tup)

#-----VALUE PREDICTION FUNCTIONS-----
#Model and predict values of rising products
def return_calc(target_tup, target_date):
    final_tup = ()
    for item in target_tup:
        product = item
        input(product)
        values_query = "SELECT open_value, record_date FROM product_values WHERE product = {} ORDER BY record_date DESC LIMIT {}"
        values_query = values_query.format(product, 4)
        values_results = query_db(values_query)
        last_value = 0
        linear = True
        values_tup = ()
        raw_date_tup = ()
        date_tup = np.empty(0, dtype=float)
        model = None
        for value in values_results:
            values_tup = values_tup + (value[0],)
            raw_date_tup = raw_date_tup + (value[1],)
            if(value[0] < last_value):
                linear = False
                last_value = value[0]
            else:
                last_value = value[0]
        for item in raw_date_tup:
            raw_date = item
            value_date = to_seconds(raw_date)
            date_tup = np.append(date_tup, [value_date], axis=0)
        date_tup = date_tup.reshape(-1, 1)
        if(linear == True):
            model = LinearRegression().fit(date_tup, values_tup)
        elif(linear == False):
            print()
            polyreg = make_pipeline(PolynomialFeatures(2), LinearRegression())
            model = polyreg.fit(date_tup, values_tup)
        final_tup = final_tup + ((product, model),)
    return(final_tup)

#-----FUNCTIONS TO SAVE FINALISED MODELS-----
def save_to_db(final_tup, date, date_delta):
    working_directory = "/models/" + date + "/"
    Path(working_directory).mkdir(parents=True, exist_ok=True)
    query_1 = "INSERT INTO model_set (target_date, date_delta) VALUES('{}', {})"
    query_1a = "SELECT id FROM model_set WHERE target_date = '{}' AND date_delta = {}"
    query_2 = "INSERT INTO models (product, model_set, model_path) VALUES({}, {}, '{}')"
    query_1 = query_1.format(date, date_delta)
    update_db(query_1)
    query_1a = query_1a.format(date, date_delta)
    raw_model_set_id = query_db(query_1a)
    model_set_id = None
    for row in raw_model_set_id:
        model_set_id = row[0]
    for item in final_tup:
        product = item[0]
        model = item[1]
        directory = working_directory + str(product) + ".joblib"
        dump(model, directory)
        query_2 = query_2.format(product, model_set_id, directory)
        update_db(query_2)

target_products = increasing_products(2020, 11, 25, 2)
final_tup = return_calc(target_products, "2020-11-22")
save_to_db(final_tup, "2020-11-25", 2)
input("Finished!!")