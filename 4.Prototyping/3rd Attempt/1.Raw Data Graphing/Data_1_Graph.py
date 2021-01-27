import pandas as pd 
import matplotlib.pyplot as plt 
df = pd.read_csv("Data_1.csv")
plt.scatter(df['record_date'], df['open_value'], color='red')
plt.plot(df['record_date'], df['open_value'])
plt.title('Stock Opening Value over Time', fontsize=14)
plt.xlabel('Time', fontsize=14)
plt.ylabel('Opening Value', fontsize=14)
plt.grid(True)
plt.show()