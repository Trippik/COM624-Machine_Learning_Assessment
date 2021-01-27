import os
import pandas_datareader as pdr
import pandas as pd

symbols = pd.read_csv("data_dump/symbols.csv")
final_df = pd.DataFrame()
max_value = symbols.shape[0]
counter = 0
while(counter < max_value):
    try:
        symbol = symbols.iloc[counter, 0]
        print(symbol)
        df = pdr.get_data_tiingo(symbol, api_key="e23ef15ab483c90d5c8dd03d66a64dbaa1c67f4b")
        final_df = pd.concat([final_df, df])
        df.to_csv(("data_dump/raw_data/" + symbol + ".csv"))
        counter = counter + 1
    except:
        "general error"
        counter = counter + 1
final_df.to_csv(("data_dump/final_data.csv"))