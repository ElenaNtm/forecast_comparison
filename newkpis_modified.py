# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 11:06:28 2024

@author: Eleni
"""

"""
lIBRARIES
"""
#pip install pandas
import pandas as pd
#import numpy as np

"""
SA_N Import already working data
"""

path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\met\SA_N\!met_e6_data.xlsx"
path = path.replace('\\', '/')
data = pd.read_excel(path)
data = data.rename({"Valid Date":"DateTime"}, axis = 1)

data['DateTime'] = pd.to_datetime(data['DateTime'])
data.set_index('DateTime', inplace = True)
data = data.drop(['MET Power (MW)', 'Power E6 (MW)', 'W+1 IP'], axis = 1)

#keep data from 27/11
data = data[data.index>='2023-11-27']

#path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\ip.xlsx"
#path = path.replace('\\', '/')
#ip = pd.read_excel(path)
#ip['DateTime'] = pd.to_datetime(ip['DateTime'])
#ip.set_index('DateTime', inplace = True)
#ip.info()
#data = pd.concat([data,ip], axis = 1)
#data.info()

"""
BALANCING COSTS

Calculate the hourly average average of IP and sum the hourly (MQ-E6)*IP, (MQ-MET)*IP
balance.xlsx has hourly data corresponding to sheet Balancing Costs
"""
#data.columns
data['(MQ-E6)*IP'] = (data['MQ (MWh)'] - data['Energy E6 (MWh)'])*data['Imbalance Prices']
data['(MQ-MET)*IP'] = (data['MQ (MWh)'] - data['MET Energy (MWh)'])*data['Imbalance Prices']
#Find the added value of the dynamic forecast doing the same procedure for the MS
data['(MQ-MS)*IP'] = (data['MQ (MWh)'] - data['MS (ΜWh)'])*data['Imbalance Prices']
#this is the new KPI1
data['ABS((MQ-E6)*IP)'] = data['(MQ-E6)*IP'].abs()
data['ABS((MQ-MET)*IP)'] = data['(MQ-MET)*IP'].abs()
data['ABS((MQ-MS)*IP)'] = data['(MQ-MS)*IP'].abs()
#data.info()
"""
SAVE THE FILE QUARTERLY DATA
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\SA_N\data(2).xlsx"
path = path.replace('\\', '/')
data.to_excel(path)

sum_by_hour = data['Imbalance Prices'].resample('H').sum()/4
# Create a new DataFrame with the sum values and corresponding hours
df = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'Average IP': sum_by_hour})

sum_by_hour = data['ABS((MQ-E6)*IP)'].resample('H').sum()

df1 = pd.DataFrame({'ABS((MQ-E6)*IP)': sum_by_hour})
df['ABS((MQ-E6)*IP)'] = df1['ABS((MQ-E6)*IP)']

sum_by_hour = data['ABS((MQ-MET)*IP)'].resample('H').sum()

df1 = pd.DataFrame({'ABS((MQ-MET)*IP)': sum_by_hour})
df['ABS((MQ-MET)*IP)'] = df1['ABS((MQ-MET)*IP)']

sum_by_hour = data['ABS((MQ-MS)*IP)'].resample('H').sum()

df1 = pd.DataFrame({'ABS((MQ-MS)*IP)': sum_by_hour})
df['ABS((MQ-MS)*IP)'] = df1['ABS((MQ-MS)*IP)']


df = df.drop(['Hour','Average IP'], axis=1)

"""
SAVE THE HOURLY DATA
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\SA_N\balance.xlsx"
path = path.replace('\\', '/')
df.to_excel(path)

"""
HOURLY DATA
kpis.xlsx has hourly data corresponding to sheet Hourly Data
"""

data['DEV E6'] = data['MQ (MWh)'] - data['Energy E6 (MWh)']
data['DEV MET'] = data['MQ (MWh)'] - data['MET Energy (MWh)']
data['DEV MS'] = data['MQ (MWh)'] - data['MS (ΜWh)']

data['ABS DEV E6'] = data['DEV E6'].abs()
data['ABS DEV MET'] = data['DEV MET'].abs()
data['ABS DEV MS'] = data['DEV MS'].abs()


data['(MQ-E6)^2'] = pow(data['DEV E6'], 2) 
data['(MQ-MET)^2'] = pow(data['DEV MET'], 2) 
data['(MQ-MS)^2'] = pow(data['DEV MS'], 2) 

data['RMSDEV E6'] = pow(data['(MQ-E6)^2'],0.5)
data['RMSDEV MET'] = pow(data['(MQ-MET)^2'],0.5)
data['RMSDEV MS'] = pow(data['(MQ-MS)^2'],0.5)

#Convert to hour
new = pd.DataFrame()

#MQ
sum_by_hour = data['MQ (MWh)'].resample('H').sum()
df = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MQ (MWh)':sum_by_hour})
new['MQ (MWh)'] = df['MQ (MWh)']

#E6
sum_by_hour = data['Energy E6 (MWh)'].resample('H').sum()
df = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'Energy E6 (MWh)':sum_by_hour})
new['E6 Energy (MWh)'] = df['Energy E6 (MWh)']

#MET
sum_by_hour = data['MET Energy (MWh)'].resample('H').sum()
df = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MET Energy (MWh)':sum_by_hour})
new['MET Energy (MWh)'] = df['MET Energy (MWh)']

#MS
sum_by_hour = data['MS (ΜWh)'].resample('H').sum()
df = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MS (ΜWh)':sum_by_hour})
new['MS (MWh)'] = df['MS (ΜWh)']

#DEV E6
sum_by_hour = data['DEV E6'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'DEV E6':sum_by_hour})
new['DEV E6'] = df1['DEV E6']

#DEV MET
sum_by_hour = data['DEV MET'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'DEV MET':sum_by_hour})
new['DEV MET'] = df1['DEV MET']

#DEV MS
sum_by_hour = data['DEV MS'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'DEV MS':sum_by_hour})
new['DEV MS'] = df1['DEV MS']

#ABS DEV E6
sum_by_hour = data['ABS DEV E6'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV E6':sum_by_hour})
new['ABS DEV E6'] = df1['ABS DEV E6']

#ABS DEV MET
sum_by_hour = data['ABS DEV MET'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV MET':sum_by_hour})
new['ABS DEV MET'] = df1['ABS DEV MET']

#ABS DEV MS
sum_by_hour = data['ABS DEV MS'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV MS':sum_by_hour})
new['ABS DEV MS'] = df1['ABS DEV MS']

#(MQ-E6)^2
sum_by_hour = data['(MQ-E6)^2'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, '(MQ-E6)^2':sum_by_hour})
new['(MQ-E6)^2'] = df1['(MQ-E6)^2']

#(MQ-MET)^2
sum_by_hour = data['(MQ-MET)^2'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, '(MQ-MET)^2':sum_by_hour})
new['(MQ-MET)^2'] = df1['(MQ-MET)^2']

#(MQ-MS)^2
sum_by_hour = data['(MQ-MS)^2'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, '(MQ-MS)^2':sum_by_hour})
new['(MQ-MS)^2'] = df1['(MQ-MS)^2']

#NEW KPI2
#RMSDEV E6
sum_by_hour = data['RMSDEV E6'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV E6':sum_by_hour})
new['RMSDEV E6'] = df1['RMSDEV E6']

#RMSDEV MET
sum_by_hour = data['RMSDEV MET'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV MET':sum_by_hour})
new['RMSDEV MET'] = df1['RMSDEV MET']

#RMSDEV MS
sum_by_hour = data['RMSDEV MS'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV MS':sum_by_hour})
new['RMSDEV MS'] = df1['RMSDEV MS']

"""
SAVE THE DATA
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\SA_N\kpis.xlsx"
path = path.replace('\\', '/')
new.to_excel(path)

"""
POINT SYSTEM
"""

result_df = pd.DataFrame()
# Compare values and assign points
result_df['ABS DEV E6 POINT'] = new['ABS DEV E6']
result_df['ABS DEV MET POINT'] = new['ABS DEV MET']

result_df['RMSDEV E6 POINT'] = new['RMSDEV E6']
result_df['RMSDEV MET POINT'] = new['RMSDEV MET']

result_df['Balances E6 POINT'] = data['ABS((MQ-E6)*IP)'] 
result_df['Balances MET POINT'] = data['ABS((MQ-MET)*IP)']

"""
SAVE THE DATA
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\SA_N\points.xlsx"
path = path.replace('\\', '/')
result_df.to_excel(path)

"""
OUTCOME 
we use the points file
"""
#Extract the day and hour from the index and add it as a new column to the dataframe
df2 = pd.DataFrame({'Day': result_df.index.day, 'Month':result_df.index.month, 'Year':result_df.index.year, 'Hour':result_df.index.hour, 'DateTime':result_df.index})
df2.set_index('DateTime', inplace=True)
points = pd.concat([result_df,df2], axis = 1)
points['DateTime'] = points.index
#points.info()
"""
SQL
"""
#Group by Hour
grouped = points.groupby(['Hour'])
#new df with last 21 rows for each group to include the last 21 days to calculate the cumulative points
#21 and not 30, as to take the last month. We do not have data of the last week of the month so we take into account only the 3 weeks
last_21 = grouped.apply(lambda x: x.tail(21)).reset_index(drop=True)
last_21.set_index('DateTime', inplace =True)

outcome = pd.DataFrame()

new = last_21.groupby(['Hour'])['ABS DEV E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['ABS DEV MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)
#make them into percent values as to sum them later
outcome['w_E6_ABS (DEV)'] = (outcome['ABS DEV E6 POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100
outcome['w_MET_ABS (DEV)'] = (outcome['ABS DEV MET POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['RMSDEV E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['RMSDEV MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_RMSDEV'] = (outcome['RMSDEV E6 POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100
outcome['w_MET_RMSDEV'] = (outcome['RMSDEV MET POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['Balances E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['Balances MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_Balances'] = (outcome['Balances E6 POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100
outcome['w_MET_Balances'] = (outcome['Balances MET POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100

#outcome.info()
"""
Find the weighted factor
"""
outcome['E6 WEIGHT'] = outcome["w_E6_ABS (DEV)"]*0.25 + outcome["w_E6_RMSDEV"]*0.25 + outcome['w_E6_Balances']*0.5
#outcome['MET WEIGHT'] = outcome["w_MET_ABS (DEV)"]*0.25 + outcome["w_MET_RMSDEV"]*0.25 + outcome['w_MET_Balances']*0.5


#outcome['FINAL KPI MET'] = outcome["ABS DEV MET POINT"]*0.25 + outcome["ABS RMSDEV MET POINT"]*0.25 + outcome['Balances MET POINT']*0.5

#outcome["ABS DEV MET POINT"] = outcome["ABS DEV MET POINT"].astype(float)
#outcome["ABS RMSDEV MET POINT"] = outcome["ABS RMSDEV MET POINT"].astype(float)
#outcome['Balances MET POINT'] = outcome['Balances MET POINT'].astype(float)
#outcome.tail()

#nan_values = outcome.isnull().sum()

#print(nan_values)


#print(outcome.dtypes)
#outcome['TOTAL'] = outcome['FINAL KPI E6'] + outcome['FINAL KPI MET']

"""
Keep 2 decimal points for the weights
"""
outcome['E6 WEIGHT'] = outcome['E6 WEIGHT'].apply(lambda x: round(x, 2))
outcome['MET WEIGHT'] = 1 - outcome['E6 WEIGHT']
new['Day'] = points.index[-1]
outcome['Day'] = new['Day']

"""
SAVE THE FILE
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\SA_N\outcome.xlsx"
path = path.replace('\\', '/')
outcome.to_excel(path)

"""
Roling Points for each day of the week from the last 30 days
"""

outcome = pd.DataFrame()
for i in range(1,8):
    outcome1 = pd.DataFrame()
    
    grouped = points.groupby([points['Hour'], points['DateTime'].dt.dayofweek])
    #grouped
    last_21 = grouped.apply(lambda x: x.tail(21)).reset_index(drop=True)
    last_21.set_index('DateTime', inplace=True)
    
    new = last_21.groupby(['Hour'])['ABS DEV E6 POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)

    new = last_21.groupby(['Hour'])['ABS DEV MET POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)
    #make them into percent values as to sum them later
    outcome1['w_E6_ABS (DEV)'] = (outcome1['ABS DEV E6 POINT']/ (outcome1['ABS DEV E6 POINT'] + outcome1['ABS DEV MET POINT']))#*100
    outcome1['w_MET_ABS (DEV)'] = (outcome1['ABS DEV MET POINT']/ (outcome1['ABS DEV E6 POINT'] + outcome1['ABS DEV MET POINT']))#*100

    new = last_21.groupby(['Hour'])['RMSDEV E6 POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)

    new = last_21.groupby(['Hour'])['RMSDEV MET POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)

    outcome1['w_E6_RMSDEV'] = (outcome1['RMSDEV E6 POINT']/ (outcome1['RMSDEV E6 POINT'] + outcome1['RMSDEV MET POINT']))#*100
    outcome1['w_MET_RMSDEV'] = (outcome1['RMSDEV MET POINT']/ (outcome1['RMSDEV E6 POINT'] + outcome1['RMSDEV MET POINT']))#*100

    new = last_21.groupby(['Hour'])['Balances E6 POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)

    new = last_21.groupby(['Hour'])['Balances MET POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)

    outcome1['w_E6_Balances'] = (outcome1['Balances E6 POINT']/ (outcome1['Balances E6 POINT'] + outcome1['Balances MET POINT']))#*100
    outcome1['w_MET_Balances'] = (outcome1['Balances MET POINT']/ (outcome1['Balances E6 POINT'] + outcome1['Balances MET POINT']))#*100
    
    outcome1['E6 WEIGHT'] = outcome1["w_E6_ABS (DEV)"]*0.25 + outcome1["w_E6_RMSDEV"]*0.25 + outcome1['w_E6_Balances']*0.5
    outcome1['E6 WEIGHT'] = outcome1['E6 WEIGHT'].apply(lambda x: round(x, 2))
    outcome1['MET WEIGHT'] = 1 - outcome1['E6 WEIGHT']
    
    new = points.iloc[-1,-1]
    outcome1['Day'] = new
    
    outcome = pd.concat([outcome1,outcome], axis = 0)
    points.drop(points.tail(24).index, inplace = True)

path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\SA_N\rolling outcome.xlsx"
outcome.to_excel(path, index = True)
"""
OUTCOME FOR W+6
"""
data.dropna(inplace = True)
"""
POINT SYSTEM W+6
"""

result_df = pd.DataFrame()
# Compare values and assign points
result_df['ABS DEV E6 POINT'] = data['ABS DEV E6']
result_df['ABS DEV MET POINT'] = data['ABS DEV MET']

result_df['RMSDEV E6 POINT'] = data['RMSDEV E6']
result_df['RMSDEV MET POINT'] = data['RMSDEV MET']

result_df['Balances E6 POINT'] = data['ABS((MQ-E6)*IP)'] 
result_df['Balances MET POINT'] = data['ABS((MQ-MET)*IP)']

"""
OUTCOME  W+6
we use the points file
"""
#Extract the day and hour from the index and add it as a new column to the dataframe
df2 = pd.DataFrame({'Day': result_df.index.day, 'Month':result_df.index.month, 'Year':result_df.index.year, 'Hour':result_df.index.hour, 'DateTime':result_df.index})
df2.set_index('DateTime', inplace=True)
points = pd.concat([result_df,df2], axis = 1)
points['DateTime'] = points.index
#points.info()
"""
SQL
"""
#Group by Hour
grouped = points.groupby(['Hour'])
#new df with last 21 rows for each group to include the last 21 days to calculate the cumulative points
#21 and not 30, as to take the last month. We do not have data of the last week of the month so we take into account only the 3 weeks
last_21 = grouped.apply(lambda x: x.tail(21)).reset_index(drop=True)
last_21.set_index('DateTime', inplace =True)

outcome = pd.DataFrame()

new = last_21.groupby(['Hour'])['ABS DEV E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['ABS DEV MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)
#make them into percent values as to sum them later
outcome['w_E6_ABS (DEV)'] = (outcome['ABS DEV E6 POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100
outcome['w_MET_ABS (DEV)'] = (outcome['ABS DEV MET POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['RMSDEV E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['RMSDEV MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_RMSDEV'] = (outcome['RMSDEV E6 POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100
outcome['w_MET_RMSDEV'] = (outcome['RMSDEV MET POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['Balances E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['Balances MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_Balances'] = (outcome['Balances E6 POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100
outcome['w_MET_Balances'] = (outcome['Balances MET POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100

#outcome.info()
"""
Find the weighted factor
"""
outcome['E6 WEIGHT'] = outcome["w_E6_ABS (DEV)"]*0.25 + outcome["w_E6_RMSDEV"]*0.25 + outcome['w_E6_Balances']*0.5

"""
Keep 2 decimal points for the weights
"""
outcome['E6 WEIGHT'] = outcome['E6 WEIGHT'].apply(lambda x: round(x, 2))
outcome['MET WEIGHT'] = 1 - outcome['E6 WEIGHT']
new['Day'] = points.index[-1]
outcome['Day'] = new['Day']

"""
SAVE THE FILE
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\SA_N\w+6 outcome.xlsx"
path = path.replace('\\', '/')
outcome.to_excel(path)


#################################################################################################################################
"""
NA_N Import already working data
"""

path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\met\NA_N\na_n met_e6_data.xlsx"
path = path.replace('\\', '/')
data = pd.read_excel(path)
data = data.rename({"Valid Date":"DateTime"}, axis = 1)
data.set_index('DateTime', inplace = True)
data = data.drop(['MET Power (MW)', 'Power E6 (MW)'], axis = 1)
data.info()

"""
BALANCING COSTS

Calculate the hourly average average of IP and sum the hourly (MQ-E6)*IP, (MQ-MET)*IP
balance.xlsx has hourly data corresponding to sheet Balancing Costs
"""

data['(MQ-E6)*IP'] = (data['MQ (MWh)'] - data['Energy E6 (MWh)'])*data['Imbalance Prices']
data['(MQ-MET)*IP'] = (data['MQ (MWh)'] - data['MET Energy (MWh)'])*data['Imbalance Prices']
data['(MQ-MS)*IP'] = (data['MQ (MWh)'] - data["MS (ΜWh)"])*data['Imbalance Prices']
data['ABS((MQ-E6)*IP)'] = data['(MQ-E6)*IP'].abs()
data['ABS((MQ-MET)*IP)'] = data['(MQ-MET)*IP'].abs()
data['ABS((MQ-MS)*IP)'] = data['(MQ-MS)*IP'].abs()
"""
SAVE THE FILE QUARTERLY DATA
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\NA_N\data(2).xlsx"
path = path.replace('\\', '/')
data.to_excel(path)

sum_by_hour = data['Imbalance Prices'].resample('H').sum()/4
#sum_by_hour
# Create a new DataFrame with the sum values and corresponding hours
df = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'Average IP': sum_by_hour})

sum_by_hour = data['ABS((MQ-E6)*IP)'].resample('H').sum()

df1 = pd.DataFrame({'ABS((MQ-E6)*IP)': sum_by_hour})
df['ABS((MQ-E6)*IP)'] = df1['ABS((MQ-E6)*IP)']

sum_by_hour = data['ABS((MQ-MET)*IP)'].resample('H').sum()

df1 = pd.DataFrame({'ABS((MQ-MET)*IP)': sum_by_hour})
df['ABS((MQ-MET)*IP)'] = df1['ABS((MQ-MET)*IP)']

sum_by_hour = data['ABS((MQ-MS)*IP)'].resample('H').sum()

df1 = pd.DataFrame({'ABS((MQ-MS)*IP)': sum_by_hour})
df['ABS((MQ-MS)*IP)'] = df1['ABS((MQ-MS)*IP)']
df = df.drop(['Hour','Average IP'], axis=1)

"""
SAVE THE HOURLY DATA
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\NA_N\balance.xlsx"
path = path.replace('\\', '/')
df.to_excel(path)

"""
HOURLY DATA
kpis.xlsx has hourly data corresponding to sheet Hourly Data
"""
data['DEV E6'] = data['MQ (MWh)'] - data['Energy E6 (MWh)']
data['DEV MET'] = data['MQ (MWh)'] - data['MET Energy (MWh)']
data['DEV MS'] = data['MQ (MWh)'] - data["MS (ΜWh)"]

data['ABS DEV E6'] = data['DEV E6'].abs()
data['ABS DEV MET'] = data['DEV MET'].abs()
data['ABS DEV MS'] = data['DEV MS'].abs()

data['(MQ-E6)^2'] = pow(data['DEV E6'], 2) 
data['(MQ-MET)^2'] = pow(data['DEV MET'], 2) 
data['(MQ-MS)^2'] = pow(data['DEV MS'], 2) 

data['RMSDEV E6'] = pow(data['(MQ-E6)^2'],0.5)
data['RMSDEV MET'] = pow(data['(MQ-MET)^2'],0.5)
data['RMSDEV MS'] = pow(data['(MQ-MS)^2'],0.5)

#Convert to hour
new = pd.DataFrame()

#MQ
sum_by_hour = data['MQ (MWh)'].resample('H').sum()
df = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MQ (MWh)':sum_by_hour})
new['MQ (MWh)'] = df['MQ (MWh)']

#E6
sum_by_hour = data['Energy E6 (MWh)'].resample('H').sum()
df = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'Energy E6 (MWh)':sum_by_hour})
new['E6 Energy (MWh)'] = df['Energy E6 (MWh)']

#MET
sum_by_hour = data['MET Energy (MWh)'].resample('H').sum()
df = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MET Energy (MWh)':sum_by_hour})
new['MET Energy (MWh)'] = df['MET Energy (MWh)']

#MS
sum_by_hour = data['MS (ΜWh)'].resample('H').sum()
df = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MS (ΜWh)':sum_by_hour})
new['MS (ΜWh)'] = df['MS (ΜWh)']

#DEV E6
sum_by_hour = data['DEV E6'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'DEV E6':sum_by_hour})
new['DEV E6'] = df1['DEV E6']

#DEV MET
sum_by_hour = data['DEV MET'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'DEV MET':sum_by_hour})
new['DEV MET'] = df1['DEV MET']

#DEV MS
sum_by_hour = data['DEV MS'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'DEV MS':sum_by_hour})
new['DEV MS'] = df1['DEV MS']

#ABS DEV E6
sum_by_hour = data['ABS DEV E6'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV E6':sum_by_hour})
new['ABS DEV E6'] = df1['ABS DEV E6']

#ABS DEV MET
sum_by_hour = data['ABS DEV MET'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV MET':sum_by_hour})
new['ABS DEV MET'] = df1['ABS DEV MET']

#ABS DEV MS
sum_by_hour = data['ABS DEV MS'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV MS':sum_by_hour})
new['ABS DEV MS'] = df1['ABS DEV MS']

#(MQ-E6)^2
sum_by_hour = data['(MQ-E6)^2'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, '(MQ-E6)^2':sum_by_hour})
new['(MQ-E6)^2'] = df1['(MQ-E6)^2']

#(MQ-MET)^2
sum_by_hour = data['(MQ-MET)^2'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, '(MQ-MET)^2':sum_by_hour})
new['(MQ-MET)^2'] = df1['(MQ-MET)^2']

#(MQ-MS)^2
sum_by_hour = data['(MQ-MS)^2'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, '(MQ-MS)^2':sum_by_hour})
new['(MQ-MS)^2'] = df1['(MQ-MS)^2']

#NEW KPI2
#RMSDEV E6
sum_by_hour = data['RMSDEV E6'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV E6':sum_by_hour})
new['RMSDEV E6'] = df1['RMSDEV E6']

#RMSDEV MET
sum_by_hour = data['RMSDEV MET'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV MET':sum_by_hour})
new['RMSDEV MET'] = df1['RMSDEV MET']

#RMSDEV MS
sum_by_hour = data['RMSDEV MS'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV MS':sum_by_hour})
new['RMSDEV MS'] = df1['RMSDEV MS']
"""
SAVE THE DATA
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\NA_N\kpis.xlsx"
path = path.replace('\\', '/')
new.to_excel(path)

"""
POINT SYSTEM
"""

result_df = pd.DataFrame()
# Compare values and assign points
result_df['ABS DEV E6 POINT'] = new['ABS DEV E6']
result_df['ABS DEV MET POINT'] = new['ABS DEV MET']

result_df['RMSDEV E6 POINT'] = new['RMSDEV E6']
result_df['RMSDEV MET POINT'] = new['RMSDEV MET']

result_df['Balances E6 POINT'] = data['ABS((MQ-E6)*IP)'] 
result_df['Balances MET POINT'] = data['ABS((MQ-MET)*IP)']

"""
SAVE THE DATA
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\NA_N\points.xlsx"
path = path.replace('\\', '/')
result_df.to_excel(path)

"""
OUTCOME 
we use the points file
"""
#Extract the day and hour from the index and add it as a new column to the dataframe
df2 = pd.DataFrame({'Day': result_df.index.day, 'Month':result_df.index.month, 'Year':result_df.index.year, 'Hour':result_df.index.hour, 'DateTime':result_df.index})
df2.set_index('DateTime', inplace=True)
points = pd.concat([result_df,df2], axis = 1)
points['DateTime'] = points.index
#points.info()

"""
SQL
"""
#Group by Hour
grouped = points.groupby(['Hour'])
#new df with last 21 rows for each group to include the last 21 days to calculate the cumulative points
#21 and not 30, as to take the last month. We do not have data of the last week of the month so we take into account only the 3 weeks
last_21 = grouped.apply(lambda x: x.tail(21)).reset_index(drop=True)
last_21.set_index('DateTime', inplace =True)

outcome = pd.DataFrame()

new = last_21.groupby(['Hour'])['ABS DEV E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['ABS DEV MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)
#make them into percent values as to sum them later
outcome['w_E6_ABS (DEV)'] = (outcome['ABS DEV E6 POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100
outcome['w_MET_ABS (DEV)'] = (outcome['ABS DEV MET POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['RMSDEV E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['RMSDEV MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_RMSDEV'] = (outcome['RMSDEV E6 POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100
outcome['w_MET_RMSDEV'] = (outcome['RMSDEV MET POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['Balances E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['Balances MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_Balances'] = (outcome['Balances E6 POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100
outcome['w_MET_Balances'] = (outcome['Balances MET POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100

#outcome.info()
"""
Find the weighted factor
"""
outcome['E6 WEIGHT'] = outcome["w_E6_ABS (DEV)"]*0.25 + outcome["w_E6_RMSDEV"]*0.25 + outcome['w_E6_Balances']*0.5

"""
Keep 2 decimal points for the weights
"""
outcome['E6 WEIGHT'] = outcome['E6 WEIGHT'].apply(lambda x: round(x, 2))
outcome['MET WEIGHT'] = 1 - outcome['E6 WEIGHT']
new['Day'] = points.index[-1]
outcome['Day'] = new['Day']

"""
SAVE THE FILE
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\NA_N\outcome.xlsx"
path = path.replace('\\', '/')
outcome.to_excel(path)

"""
Roling Points for each day of the week from the last 30 days
"""
outcome = pd.DataFrame()
for i in range(1,8):
    outcome1 = pd.DataFrame()
    
    grouped = points.groupby([points['Hour'], points['DateTime'].dt.dayofweek])
    #grouped
    last_21 = grouped.apply(lambda x: x.tail(21)).reset_index(drop=True)
    last_21.set_index('DateTime', inplace=True)
    
    new = last_21.groupby(['Hour'])['ABS DEV E6 POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)

    new = last_21.groupby(['Hour'])['ABS DEV MET POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)
    #make them into percent values as to sum them later
    outcome1['w_E6_ABS (DEV)'] = (outcome1['ABS DEV E6 POINT']/ (outcome1['ABS DEV E6 POINT'] + outcome1['ABS DEV MET POINT']))#*100
    outcome1['w_MET_ABS (DEV)'] = (outcome1['ABS DEV MET POINT']/ (outcome1['ABS DEV E6 POINT'] + outcome1['ABS DEV MET POINT']))#*100

    new = last_21.groupby(['Hour'])['RMSDEV E6 POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)

    new = last_21.groupby(['Hour'])['RMSDEV MET POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)

    outcome1['w_E6_RMSDEV'] = (outcome1['RMSDEV E6 POINT']/ (outcome1['RMSDEV E6 POINT'] + outcome1['RMSDEV MET POINT']))#*100
    outcome1['w_MET_RMSDEV'] = (outcome1['RMSDEV MET POINT']/ (outcome1['RMSDEV E6 POINT'] + outcome1['RMSDEV MET POINT']))#*100

    new = last_21.groupby(['Hour'])['Balances E6 POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)

    new = last_21.groupby(['Hour'])['Balances MET POINT'].sum().to_frame()
    outcome1 = pd.concat([outcome1, new], axis = 1)

    outcome1['w_E6_Balances'] = (outcome1['Balances MET POINT']/ (outcome1['Balances E6 POINT'] + outcome1['Balances MET POINT']))#*100
    outcome1['w_MET_Balances'] = (outcome1['Balances E6 POINT']/ (outcome1['Balances E6 POINT'] + outcome1['Balances MET POINT']))#*100

    outcome1['E6 WEIGHT'] = outcome1["w_E6_ABS (DEV)"]*0.25 + outcome1["w_E6_RMSDEV"]*0.25 + outcome1['w_E6_Balances']*0.5
    outcome1['E6 WEIGHT'] = outcome1['E6 WEIGHT'].apply(lambda x: round(x, 2))
    outcome1['MET WEIGHT'] = 1 - outcome1['E6 WEIGHT']
    
    new = points.iloc[-1,-1]
    outcome1['Day'] = new
    
    outcome = pd.concat([outcome1,outcome], axis = 0)
    points.drop(points.tail(24).index, inplace = True)

path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\NA_N\rolling outcome.xlsx"
outcome.to_excel(path, index = True)
"""
OUTCOME FOR W+6
"""
data.dropna(inplace = True)
"""
POINT SYSTEM W+6
"""

result_df = pd.DataFrame()
# Compare values and assign points
result_df['ABS DEV E6 POINT'] = data['ABS DEV E6']
result_df['ABS DEV MET POINT'] = data['ABS DEV MET']

result_df['RMSDEV E6 POINT'] = data['RMSDEV E6']
result_df['RMSDEV MET POINT'] = data['RMSDEV MET']

result_df['Balances E6 POINT'] = data['ABS((MQ-E6)*IP)'] 
result_df['Balances MET POINT'] = data['ABS((MQ-MET)*IP)']

"""
OUTCOME  W+6
we use the points file
"""
#Extract the day and hour from the index and add it as a new column to the dataframe
df2 = pd.DataFrame({'Day': result_df.index.day, 'Month':result_df.index.month, 'Year':result_df.index.year, 'Hour':result_df.index.hour, 'DateTime':result_df.index})
df2.set_index('DateTime', inplace=True)
points = pd.concat([result_df,df2], axis = 1)
points['DateTime'] = points.index
#points.info()
"""
SQL
"""
#Group by Hour
grouped = points.groupby(['Hour'])
#new df with last 21 rows for each group to include the last 21 days to calculate the cumulative points
#21 and not 30, as to take the last month. We do not have data of the last week of the month so we take into account only the 3 weeks
last_21 = grouped.apply(lambda x: x.tail(21)).reset_index(drop=True)
last_21.set_index('DateTime', inplace =True)

outcome = pd.DataFrame()

new = last_21.groupby(['Hour'])['ABS DEV E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['ABS DEV MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)
#make them into percent values as to sum them later
outcome['w_E6_ABS (DEV)'] = (outcome['ABS DEV E6 POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100
outcome['w_MET_ABS (DEV)'] = (outcome['ABS DEV MET POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['RMSDEV E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['RMSDEV MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_RMSDEV'] = (outcome['RMSDEV E6 POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100
outcome['w_MET_RMSDEV'] = (outcome['RMSDEV MET POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['Balances E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['Balances MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_Balances'] = (outcome['Balances E6 POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100
outcome['w_MET_Balances'] = (outcome['Balances MET POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100

#outcome.info()
"""
Find the weighted factor
"""
outcome['E6 WEIGHT'] = outcome["w_E6_ABS (DEV)"]*0.25 + outcome["w_E6_RMSDEV"]*0.25 + outcome['w_E6_Balances']*0.5

"""
Keep 2 decimal points for the weights
"""
outcome['E6 WEIGHT'] = outcome['E6 WEIGHT'].apply(lambda x: round(x, 2))
outcome['MET WEIGHT'] = 1 - outcome['E6 WEIGHT']
new['Day'] = points.index[-1]
outcome['Day'] = new['Day']

"""
SAVE THE FILE
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\NA_N\w+6 outcome.xlsx"
path = path.replace('\\', '/')
outcome.to_excel(path)
