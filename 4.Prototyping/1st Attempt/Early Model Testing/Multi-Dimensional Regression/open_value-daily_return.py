#Import neccessary libraries
import matplotlib.pyplot as plt
import pandas as pd 

#Load in raw data
raw = pd.read_csv("raw_data.csv")
plt.scatter(raw["open_value"], raw["daily_return"], color="red")
plt.title("Opening Value Vs Daily Return")
plt.xlabel("Opening Value")
plt.ylabel("Daily Return")
plt.grid(True)
plt.show()