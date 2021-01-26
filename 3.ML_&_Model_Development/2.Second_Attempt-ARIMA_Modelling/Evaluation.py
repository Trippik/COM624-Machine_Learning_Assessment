import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import mysql.connector
import warnings
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARMA',
                        FutureWarning)
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARIMA',
                        FutureWarning)
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

#-----DATA PULL-----
def data_pull(product_id, date):
    query = "SELECT product, record_date , close_value, open_value FROM product_values WHERE product = {} AND record_date < '{}' ORDER BY record_date ASC"
    query = query.format(str(product_id), date)
    raw_results = query_db(query)
    df = pd.DataFrame(columns = ["product", "record_date", "close_value", "open_value"])
    for row in raw_results:
        df = df.append(pd.Series([row[0], row[1], row[2], row[3]], index = df.columns), ignore_index = True)
    return(df)

#Predict next day value
def predict(product):
    df = data_pull(product, "2020-11-26")
    count = 1
    training_data = []
    while (count < df.shape[0]):
        training_data = training_data + [df.loc[count, "open_value"],]
        count = count + 1
    model = ARIMA(training_data, order=(4, 1, 1))
    fitted_model = model.fit()
    return(fitted_model.forecast()[0][0])

def pull_test_products():
    query = "SELECT product FROM product_values WHERE record_date > '2020-11-25' AND record_date > '2020-11-26' LIMIT 1000"
    raw_results = query_db(query)
    products = []
    for row in raw_results:
        products = products + [row[0],]
    return(products)

def test_product(product):
    try:
        prediction = predict(product)
    except:
        pass
    query_1 = "SELECT open_value FROM product_values WHERE product = {} AND record_date = '2020-11-26'"
    query_2 = "SELECT open_value FROM product_values WHERE product = {} AND record_date = '2020-11-27'"
    query_1 = query_1.format(str(product))
    query_2 = query_2.format(str(product))
    raw_results_1 = query_db(query_1)
    raw_results_2 = query_db(query_2)
    score = 0
    for row in raw_results_1:
        early_value = row[0]
    for row in raw_results_2:
        next_value = float(row[0])
    try:
        dif = (prediction - next_value)/next_value
        score = score + (dif)
    except:
        pass
    return(score)

products_to_test = pull_test_products()
score_tup = ()
for product in products_to_test:
    score = test_product(product)
    print("------------------------------------------------------------")
    print("Product:" + str(product))
    print("Score: " + str(score))
    print("------------------------------------------------------------")
    score_tup = score_tup + (score,)
percentage_major_error = (score_tup.count(1) / len(score_tup)) * 100
sum_of_score = 0
for item in score_tup:
    sum_of_score = sum_of_score + item
avg_score = sum_of_score / len(score_tup)
print("Percentage major error: " + str(percentage_major_error))
print("Avg Score: " + str(avg_score))