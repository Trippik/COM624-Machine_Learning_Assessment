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
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error
ohe = OneHotEncoder(sparse=False)

#Import train data
train = pd.read_csv("Single_Product_Test_Train.csv")
y_train = train.pop("Daily Return").values
x = train.pop("Daily Range").values
X_train = x.reshape(-1, 1)

#Map train data to linear regression model
regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)

#Import test data
test = pd.read_csv("Single_Product_Test_Test.csv")
y_test = test.pop("Daily Return").values
x = test.pop("Daily Range").values
X_test = x.reshape(-1, 1)

#Make y predictions using X_test data
y_predict = regr.predict(X_test)

#Calculate coefficients
print("Coefficients: \n", regr.coef_)
#The Mean Percentage error
print("Mean Percentage error: " + str(mean_absolute_percentage_error(y_test, y_predict)) + "%")
#The r2 score
print("The r2 Score: " + str(r2_score(y_test, y_predict)))
#The mean squared error
print("Mean squared error: " + str(mean_squared_error(y_test, y_predict)))
#Plot Outputs
plt.scatter(X_test, y_test, color="black")
plt.plot(X_test, y_predict, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.xlabel("Daily Range")
plt.ylabel("Daily Return")
plt.show()