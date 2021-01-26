#-----LIBRARIES-----
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
import logging
#-------------------------------------------------
#LOG FILE
#-------------------------------------------------
logging.basicConfig(filename="predictor.log", level=logging.DEBUG)

#-------------------------------------------------
#UNDERLYING FUNCTIONS
#-------------------------------------------------
#-----CORE FUNCTIONS FOR SQL ACCESS-----
#Function to read data from database
def query_db(query):
    db = mysql.connector.connect(
        host="INSERT IP",
        user="INSERT USER",
        password="INSERT PASSWORD",
        database="financial_data"
    )
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return(result)

#Function to write data to database
def update_db(query):
    db = mysql.connector.connect(
        host="INSERT IP",
        user="INSERT USER",
        password="INSERT PASSWORD",
        database="financial_data"
    )
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()

#-------------------------------------------------
#STAGE 1 - FIND AVERAGE LENGTH OF UPWARD TREND
#-------------------------------------------------
#-----SHARED FUNCTIONS-----
def trend_detector(date_rate, value):
    result = np.polyfit(date_rate, value, 1)
    slope = result[-2]
    return(slope)

#-----COLLATE UPWARD TRENDS-----
def collate_upward_trends(df):
    int_value_tup = []
    int_date_tup = []
    values_tup = []
    date_tup = []
    last_value = 0
    count = 1
    last_product = 0
    while(count < df.shape[0]):
        date_point = df.loc[count, "record_date"]
        value_point = df.loc[count, "open_value"]
        product = df.loc[count, "product"]
        if((value_point > last_value) and (product == last_product)):
            int_value_tup = int_value_tup + [value_point,]
            int_date_tup = int_date_tup + [date_point,]
            last_value = value_point
            last_product = product
        elif((value_point < last_value) or (product != last_product)):
            values_tup = values_tup + [int_value_tup,]
            int_value_tup = []
            date_tup = date_tup + [int_date_tup,]
            int_date_tup = []
            last_value = value_point
            last_product = product
        count = count + 1

    new_df = pd.DataFrame(columns = ["no_days", "values"])
    for item in values_tup:
        if(len(item) != 0):
            new_df = new_df.append(pd.Series([len(item), item], index = new_df.columns), ignore_index = True)
    logging.debug("\n" + str(datetime.datetime.now()) + "-Collated Updward Trends: \n" + new_df.to_string())
    return(new_df)

#-----COUNT FREQUENCY OF UPWARD TREND LENGTH-----
def find_frequency(df):
    raw_data = df["no_days"]
    counter = 1
    values_tup = ()
    max_value = raw_data.max()
    while(counter < (max_value + 1)):
        sub_counter = 0
        for row in raw_data:
            if(row == counter):
                sub_counter = sub_counter + 1
        print("Number of", counter, "occurences: " + str(sub_counter))
        values_tup = values_tup + (sub_counter,)
        counter = counter + 1  
    logging.debug("\n" + str(datetime.datetime.now()) + "-Frenquency of values:\n" + str(values_tup))          
    return(values_tup)

#-----DETERMINE MOST FREQUENT TREND LENGTH-----
def frequency_determine(values_tup):
    count = 1
    highest_value = 0
    highest_value_count = 0
    for item in values_tup:
        if(item > highest_value) and (count != 1):
            highest_value = item 
            highest_value_count = count
        count = count + 1
    logging.debug("\n" + str(datetime.datetime.now()) + "-Frequency Determined:\n" + str((highest_value_count, highest_value)))
    return((highest_value_count, highest_value))

#-----CONTROL FUNCTION-----
def frequency_control():
    query = """SELECT
product_values.product,
product_values.record_date,
product_values.open_value 
FROM product_values
WHERE product_values.record_date > "{}"
ORDER BY product, product_values.record_date 
LIMIT {}"""
    query = query.format("2020-01-01", str(10000))
    raw_results = query_db(query)
    df = pd.DataFrame(columns=['product', 'record_date', 'open_value'])
    for row in raw_results:
        df = df.append(pd.Series([row[0], row[1], row[2]], index = df.columns), ignore_index = True)
    return(frequency_determine(find_frequency(collate_upward_trends(df))))

#-------------------------------------------------
#STAGE 2 - IDENTIFY KEY PRODUCTS
#-------------------------------------------------
#-----RETURNING TARGET PRODUCTS-----
#Return tuple of targets that are active
def active_products(target_date):
    query = "SELECT product FROM product_values WHERE record_date = '{}'"
    query = query.format(target_date)
    results = query_db(query)
    return(results)

#Return tuple of products whose value has increased over n number of days
def increasing_products(year, month, day):
    today = datetime.datetime(year, month, day)
    day_delta = ((frequency_control())[0]) - 1
    print(day_delta)
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
    logging.debug("\n" + str(datetime.datetime.now()) + " -" + str(len(target_tup)) + " products highlighted out of " + str(len(active_products(today.strftime("%Y-%m-%d")))) + " active products \n")
    logging.debug("\n" + str(datetime.datetime.now()) + " " + str(target_tup) + "\n")
    return(target_tup)

#-------------------------------------------------
#STAGE 3 - PREDICT VALUES OF HIGHLIGHTED PRODUCTS
#-------------------------------------------------
#-----SHARED FUNCTIONS-----
def to_seconds(date):
    return time.mktime(date.timetuple())

#-----VALUE PREDICTION FUNCTIONS-----
#Model and predict values of rising products
def return_calc(target_tup):
    final_tup = ()
    number = (frequency_control()[0]) * 2
    for item in target_tup:
        product = item
        logging.debug("\n" + str(datetime.datetime.now()) + " -" + str(product) + "\n")
        values_query = "SELECT open_value, record_date FROM product_values WHERE product = {} ORDER BY record_date DESC LIMIT {}"
        values_query = values_query.format(product, str(number))
        values_results = query_db(values_query)
        last_value = 0
        linear = True
        values_tup = ()
        raw_date_tup = ()
        date_tup = np.empty(0, dtype=float)
        model = None
        for value in values_results:
            values_tup = values_tup + (value[0],)
            logging.debug("Value: " + str(value[0]) + "\n")
            raw_date_tup = raw_date_tup + (value[1],)
            logging.debug("Date: " + str(value[1]) + "\n")
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
            polyreg = make_pipeline(PolynomialFeatures(2), LinearRegression())
            model = polyreg.fit(date_tup, values_tup)
            logging.debug(str(model) + "\n")
        final_tup = final_tup + ((product, model),)
    return(final_tup)

target_tup = increasing_products(2020, 11, 25)
final_tup = return_calc(target_tup)
print(final_tup)