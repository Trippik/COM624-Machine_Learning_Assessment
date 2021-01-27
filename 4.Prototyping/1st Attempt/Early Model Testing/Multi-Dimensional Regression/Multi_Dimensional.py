#Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn
import sklearn
from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model
from sklearn.neighbors import KNeighborsRegressor
import sklearn.linear_model
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error

#Import raw data
data = pd.read_csv("TEST DATA 2.CSV")
X = data[["product_type", "open_value", "close_value", "high_value", "low_value", "daily_return", "daily_range"]]
y = data["percentage_daily_return"]
print(X)
print(y)

#Split into test and train data sets
X_train, y_train, X_test, y_test = train_test_split(X, y, test_size=0.33)

#Fit to linear regression model
regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)