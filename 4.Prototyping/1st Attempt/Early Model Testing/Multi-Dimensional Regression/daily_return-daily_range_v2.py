#Import neccessary libraries
import matplotlib.pyplot as plt
import pandas as pd 

#Load in raw data
raw = pd.read_csv("raw_data_v2.csv")
plt.scatter(raw["daily_range"], raw["daily_return"], color="red")
plt.title("Daily Range Vs Daily Return")
plt.xlabel("Daily Range")
plt.ylabel("Daily Return")
plt.grid(True)
plt.show()