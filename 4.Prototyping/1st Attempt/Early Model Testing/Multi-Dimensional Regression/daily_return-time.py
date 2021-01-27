#Import neccessary libraries
import matplotlib.pyplot as plt
import pandas as pd 

#Load in raw data
raw = pd.read_csv("raw_data.csv")
plt.scatter(raw["date_rate"], raw["daily_return"], color="red")
plt.title("Time Vs Daily Return")
plt.xlabel("Time")
plt.ylabel("Daily Return")
plt.grid(True)
plt.show()