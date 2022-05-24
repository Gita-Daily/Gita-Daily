import pandas as pd
user_data = pd.read_csv('data.csv')

user_index = user_data.index[user_data["Phone Number"] == 919108006252].to_list()
print(user_index)
user_data[user_index[0], 'Subscribe'] = [False]
#user_data.loc[user_index,['Subscribe']] = [False]
user_data.to_csv('data.csv') 