#Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn
import sklearn
from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn import datasets, linear_model
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error
ohe = OneHotEncoder(sparse=False)

#Import train data
train = pd.read_csv("new_dataset_train.csv")
y_train = train.pop("Daily Return").values
X_train = train.pop("Avg return 3 day").values
X_train = X_train.reshape(-1, 1)

#Map train data to nearest neighbor regression model
regr = KNeighborsRegressor(n_neighbors = 100)
regr.fit(X_train, y_train)

#Import test data
test = pd.read_csv("new_dataset_test.csv")
y_test = test.pop("Daily Return").values
X_test = test.pop("Avg return 3 day").values
X_test = X_test.reshape(-1, 1)

#Make y predictions using X_test data
y_predict = regr.predict(X_test)

#Score
print("Testing r^2 rates: {:.2f}".format(regr.score(X_test, y_test)))