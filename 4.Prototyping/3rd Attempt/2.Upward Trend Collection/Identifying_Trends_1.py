#Import necessary libraries
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv("Data_1.csv")

def trend_detector(date_rate, value):
    result = np.polyfit(date_rate, value, 1)
    slope = result[-2]
    return(slope)

int_value_tup = []
int_date_tup = []
values_tup = []
date_tup = []
last_value = 0
count = 1
print(df.shape[0])
while(count < df.shape[0]):
    date_point = df.loc[count, "record_date"]
    value_point = df.loc[count, "open_value"]
    if(value_point > last_value):
        int_value_tup = int_value_tup + [value_point,]
        int_date_tup = int_date_tup + [date_point,]
        last_value = value_point
    elif(value_point < last_value):
        values_tup = values_tup + [int_value_tup,]
        int_value_tup = []
        date_tup = date_tup + [int_date_tup,]
        int_date_tup = []
        last_value = value_point
    count = count + 1

new_df = pd.DataFrame(columns = ["no_days", "values"])
for item in values_tup:
    new_df = new_df.append(pd.Series([len(item), item], index = new_df.columns), ignore_index = True)
print(new_df)
new_df.to_csv("data_2.csv")