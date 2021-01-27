#Import necessary library
import pandas as pd
train = pd.read_csv("Single_Product_Test.csv")
print(train)
input()
new_df_train = pd.DataFrame(columns=["id", "date_rate", "Daily Return", "Avg return 3 day"])
new_df_test = pd.DataFrame(columns=["id", "date_rate", "Daily Return", "Avg return 3 day"])
total_rows = train.shape[0]
print(total_rows)
print(total_rows / 2)
count = 1
while(count < total_rows):
    if(count < (total_rows / 2)):
        if(count > 4):
            value_1 = float(train.loc[(count - 3), "Daily Return"])
            value_2 = float(train.loc[(count - 2), "Daily Return"])
            value_3 = float(train.loc[(count - 1), "Daily Return"])
            avg_return = ((value_1 + value_2 + value_3) / 3)
            new_df_train = new_df_train.append(pd.Series([train.loc[count,"id"], train.loc[count,"date_rate"], train.loc[count, "Daily Return"], avg_return], index = new_df_train.columns), ignore_index = True)
        else:
            pass
    if(count > (total_rows / 2)):
        value_1 = float(train.loc[(count - 3), "Daily Return"])
        value_2 = float(train.loc[(count - 2), "Daily Return"])
        value_3 = float(train.loc[(count - 1), "Daily Return"])
        avg_return = ((value_1 + value_2 + value_3) / 3)
        new_df_test = new_df_test.append(pd.Series([train.loc[count,"id"], train.loc[count,"date_rate"], train.loc[count, "Daily Return"], avg_return], index = new_df_test.columns), ignore_index = True)    
    count = count + 1
new_df_train.to_csv("new_dataset_train.csv", index=False)
new_df_test.to_csv("new_dataset_test.csv", index=False)