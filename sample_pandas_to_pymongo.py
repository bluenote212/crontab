import pandas as pd

data_csv = pd.read_csv('C:/Users/B180093/Desktop/test.csv',encoding='utf-8')

project_data = []
for i in range(0, len(data_csv)):
    temp = []
    temp = {'key':str(data_csv.iloc[i]['Key']), 'date':str(data_csv.iloc[i]['date']),'total':str(data_csv.iloc[i]['total']),'2weeks':str(data_csv.iloc[i]['2weeks']),'pending':str(data_csv.iloc[i]['pending'])}
    project_data.append(temp)





