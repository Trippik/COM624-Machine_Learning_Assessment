#Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn
import sklearn
from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model, preprocessing
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error

#Load in raw data
raw = pd.read_csv("raw_data.csv")
lab_enc = preprocessing.LabelEncoder()
X = raw[["date_rate", lab_enc."close_value", "high_value", "low_value", "open_value", "volume", "adj_close", "adj_low", "adj_volume", "div_cash", "split_factor"]]
y = raw["daily_return"]

#Split into train and test sets
lab_enc = preprocessing.LabelEncoder()
X_train = X[:-750]
X_test = X[-750:]
y_train = y[:-750]
y_test = y[-750:]

#Create and train model
model = linear_model.LogisticRegression()
model.fit(X_train, y_train)

#Test model
y_pred = model.predict(X_test)

#Plot outputs
print(model.summary())
print(sklearn.metrics(y_test, y_pred))