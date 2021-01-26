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

df = data_pull(5, "2020-11-26")
count = 1
training_data = []
while (count < df.shape[0]):
    training_data = training_data + [df.loc[count, "open_value"],]
    count = count + 1

model = ARIMA(training_data, order=(4, 1, 1))
fitted_model = model.fit()
print(fitted_model.forecast())