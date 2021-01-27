#Import necessary libraries
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv("data_3.csv")

def trend_detector(date_rate, value):
    result = np.polyfit(date_rate, value, 1)
    slope = result[-2]
    return(slope)

raw_data = df["no_days"]
print(raw_data)
counter = 1
values_tup = ()
max_value = raw_data.max()
print(max_value)
while(counter < (max_value + 1)):
    sub_counter = 0
    for row in raw_data:
        if(row == counter):
            sub_counter = sub_counter + 1
    print("Number of", counter, "occurences: " + str(sub_counter))
    values_tup = values_tup + (sub_counter,)
    counter = counter + 1            

print()
print(values_tup)
input()