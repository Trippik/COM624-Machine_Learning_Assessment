#Import neccessary libraries
import matplotlib.pyplot as plt
import pandas as pd 

#Load in raw data
raw = pd.read_csv("raw_data.csv")
total_raw_rows = raw.shape[0]

#Extract/calculate necessary data
count = 4
three_day_avg = ()
daily_return = ()
while(count < total_raw_rows):
    summ = ((raw.loc[(count - 3), "daily_return"]) + (raw.loc[(count - 2), "daily_return"]) + (raw.loc[(count - 1), "daily_return"]))
    avg = summ / 3
    three_day_avg = three_day_avg + (avg,)
    daily_return = daily_return + (raw.loc[count, "daily_return"],)
    count = count + 1

plt.scatter(three_day_avg, daily_return, color="red")
plt.title("3 Day Avg Return Vs Daily Return")
plt.xlabel("3 Day Avg Return")
plt.ylabel("Daily Return")
plt.grid(True)
plt.show()