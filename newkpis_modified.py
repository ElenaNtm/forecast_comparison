# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 09:30:48 2024

@author: Eleni
"""
"""
Libraries
"""
import pandas as pd
"""
MS Import already working data
"""
path = R"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\met\MS\met_e6_data.xlsx"
path = path.replace('\\', '/')
data = pd.read_excel(path)
data = data.rename({"Valid Date":"DateTime"}, axis = 1)

data['DateTime'] = pd.to_datetime(data['DateTime'])
data.set_index('DateTime', inplace = True)
data = data.drop(['MET Power (MW)', 'Power E6 (MW)', 'W+1 IP'], axis = 1)

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
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\MS\data(2).xlsx"
path = path.replace('\\', '/')
data.to_excel(path)

sum_by_hour = data['Imbalance Prices'].resample('H').sum()/4
# Create a new DataFrame with the sum values and corresponding hours
df = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'Average IP': sum_by_hour})

sum_by_hour = data['(MQ-E6)*IP'].resample('H').sum()

df1 = pd.DataFrame({'(MQ-E6)*IP': sum_by_hour})
df['(MQ-E6)*IP'] = df1['(MQ-E6)*IP']
df['ABS(MQ-E6)*IP'] = df['(MQ-E6)*IP'].abs()

sum_by_hour = data['(MQ-MET)*IP'].resample('H').sum()

df1 = pd.DataFrame({'(MQ-MET)*IP': sum_by_hour})
df['(MQ-MET)*IP'] = df1['(MQ-MET)*IP']
df['ABS(MQ-MET)*IP'] = df['(MQ-MET)*IP'].abs()


sum_by_hour = data['(MQ-MS)*IP'].resample('H').sum()

df1 = pd.DataFrame({'(MQ-MS)*IP': sum_by_hour})
df['(MQ-MS)*IP'] = df1['(MQ-MS)*IP']
df['ABS(MQ-MS)*IP'] = df['(MQ-MS)*IP'].abs()

df = df.drop(['Hour','Average IP','(MQ-MS)*IP', '(MQ-MET)*IP', '(MQ-E6)*IP'], axis=1)

"""
SAVE THE HOURLY DATA
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\MS\balance.xlsx"
path = path.replace('\\', '/')
df.to_excel(path)

"""
HOURLY DATA
kpis.xlsx has hourly data corresponding to sheet Hourly Data
"""

data['DEV E6'] = data['MQ (MWh)'] - data['Energy E6 (MWh)']
data['DEV MET'] = data['MQ (MWh)'] - data['MET Energy (MWh)']
data['DEV MS'] = data['MQ (MWh)'] - data['MS (ΜWh)']

#data['ABS DEV E6'] = data['DEV E6'].abs()
#data['ABS DEV MET'] = data['DEV MET'].abs()
#data['ABS DEV MS'] = data['DEV MS'].abs()


data['(MQ-E6)^2'] = pow(data['DEV E6'], 2) 
data['(MQ-MET)^2'] = pow(data['DEV MET'], 2) 
data['(MQ-MS)^2'] = pow(data['DEV MS'], 2) 


#Convert to hour
new = pd.DataFrame()

#MQ
sum_by_hour = data['MQ (MWh)'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MQ (MWh)':sum_by_hour})
new['MQ (MWh)'] = df1['MQ (MWh)']

#E6
sum_by_hour = data['Energy E6 (MWh)'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'Energy E6 (MWh)':sum_by_hour})
new['E6 Energy (MWh)'] = df1['Energy E6 (MWh)']

#MET
sum_by_hour = data['MET Energy (MWh)'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MET Energy (MWh)':sum_by_hour})
new['MET Energy (MWh)'] = df1['MET Energy (MWh)']

#MS
sum_by_hour = data['MS (ΜWh)'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MS (ΜWh)':sum_by_hour})
new['MS (MWh)'] = df1['MS (ΜWh)']

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
#sum_by_hour = data['ABS DEV E6'].resample('H').sum()
#df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV E6':sum_by_hour})
new['ABS DEV E6'] = new['DEV E6'].abs()

#ABS DEV MET
#sum_by_hour = data['ABS DEV MET'].resample('H').sum()
#df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV MET':sum_by_hour})
new['ABS DEV MET'] = new['DEV MET'].abs()

#ABS DEV MS
#sum_by_hour = data['ABS DEV MS'].resample('H').sum()
#df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV MS':sum_by_hour})
new['ABS DEV MS'] = new['DEV MS'].abs()

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
sum_by_hour = pow(data['(MQ-E6)^2'].resample('H').sum(),0.5)
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV E6':sum_by_hour})
new['RMSDEV E6'] = df1['RMSDEV E6']

#RMSDEV MET
sum_by_hour = pow(data['(MQ-MET)^2'].resample('H').sum(),0.5)
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV MET':sum_by_hour})
new['RMSDEV MET'] = df1['RMSDEV MET']

#RMSDEV MS
sum_by_hour = pow(data['(MQ-MS)^2'].resample('H').sum(),0.5)
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV MS':sum_by_hour})
new['RMSDEV MS'] = df1['RMSDEV MS']

"""
SAVE THE DATA
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\MS\kpis.xlsx"
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

result_df['Balances E6 POINT'] = df['ABS(MQ-E6)*IP'] 
result_df['Balances MET POINT'] = df['ABS(MQ-MET)*IP']

"""
SAVE THE DATA
"""
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\MS\points.xlsx"
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
outcome['w_E6_ABS (DEV)'] = (outcome['ABS DEV MET POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100
outcome['w_MET_ABS (DEV)'] = (outcome['ABS DEV E6 POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['RMSDEV E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['RMSDEV MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_RMSDEV'] = (outcome['RMSDEV MET POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100
outcome['w_MET_RMSDEV'] = (outcome['RMSDEV E6 POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['Balances E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['Balances MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_Balances'] = (outcome['Balances MET POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100
outcome['w_MET_Balances'] = (outcome['Balances E6 POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100

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
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\MS\outcome.xlsx"
path = path.replace('\\', '/')
outcome.to_excel(path)

"""
OUTCOME FOR W+6
"""
data.dropna(inplace = True)
new = pd.DataFrame()

#MQ
sum_by_hour = data['MQ (MWh)'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MQ (MWh)':sum_by_hour})
new['MQ (MWh)'] = df1['MQ (MWh)']

#E6
sum_by_hour = data['Energy E6 (MWh)'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'Energy E6 (MWh)':sum_by_hour})
new['E6 Energy (MWh)'] = df1['Energy E6 (MWh)']

#MET
sum_by_hour = data['MET Energy (MWh)'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MET Energy (MWh)':sum_by_hour})
new['MET Energy (MWh)'] = df1['MET Energy (MWh)']

#MS
sum_by_hour = data['MS (ΜWh)'].resample('H').sum()
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'MS (ΜWh)':sum_by_hour})
new['MS (MWh)'] = df1['MS (ΜWh)']

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
#sum_by_hour = data['ABS DEV E6'].resample('H').sum()
#df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV E6':sum_by_hour})
new['ABS DEV E6'] = new['DEV E6'].abs()

#ABS DEV MET
#sum_by_hour = data['ABS DEV MET'].resample('H').sum()
#df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV MET':sum_by_hour})
new['ABS DEV MET'] = new['DEV MET'].abs()

#ABS DEV MS
#sum_by_hour = data['ABS DEV MS'].resample('H').sum()
#df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'ABS DEV MS':sum_by_hour})
new['ABS DEV MS'] = new['DEV MS'].abs()

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
sum_by_hour = pow(data['(MQ-E6)^2'].resample('H').sum(),0.5)
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV E6':sum_by_hour})
new['RMSDEV E6'] = df1['RMSDEV E6']

#RMSDEV MET
sum_by_hour = pow(data['(MQ-MET)^2'].resample('H').sum(),0.5)
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV MET':sum_by_hour})
new['RMSDEV MET'] = df1['RMSDEV MET']

#RMSDEV MS
sum_by_hour = pow(data['(MQ-MS)^2'].resample('H').sum(),0.5)
df1 = pd.DataFrame({'Hour': sum_by_hour.index.hour, 'RMSDEV MS':sum_by_hour})
new['RMSDEV MS'] = df1['RMSDEV MS']

"""
POINT SYSTEM
"""

result_df = pd.DataFrame()
# Compare values and assign points
result_df['ABS DEV E6 POINT'] = new['ABS DEV E6']
result_df['ABS DEV MET POINT'] = new['ABS DEV MET']

result_df['RMSDEV E6 POINT'] = new['RMSDEV E6']
result_df['RMSDEV MET POINT'] = new['RMSDEV MET']
l = new.index[-1]

df = df[df.index<=l]
result_df['Balances E6 POINT'] = df['ABS(MQ-E6)*IP'] 
result_df['Balances MET POINT'] = df['ABS(MQ-MET)*IP']

"""
OUTCOME 
we use the points file
"""
df2 = pd.DataFrame({'Day': result_df.index.day, 'Month':result_df.index.month, 'Year':result_df.index.year, 'Hour':result_df.index.hour, 'DateTime':result_df.index})
df2.set_index('DateTime', inplace=True)
points = pd.concat([result_df,df2], axis = 1)
points['DateTime'] = points.index

"""
SQL
"""
#Group by Hour
grouped = points.groupby(['Hour'])
last_21 = grouped.apply(lambda x: x.tail(21)).reset_index(drop=True)
last_21.set_index('DateTime', inplace =True)

outcome = pd.DataFrame()

new = last_21.groupby(['Hour'])['ABS DEV E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['ABS DEV MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)
#make them into percent values as to sum them later
outcome['w_E6_ABS (DEV)'] = (outcome['ABS DEV MET POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100
outcome['w_MET_ABS (DEV)'] = (outcome['ABS DEV E6 POINT']/ (outcome['ABS DEV E6 POINT'] + outcome['ABS DEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['RMSDEV E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['RMSDEV MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_RMSDEV'] = (outcome['RMSDEV MET POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100
outcome['w_MET_RMSDEV'] = (outcome['RMSDEV E6 POINT']/ (outcome['RMSDEV E6 POINT'] + outcome['RMSDEV MET POINT']))#*100

new = last_21.groupby(['Hour'])['Balances E6 POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

new = last_21.groupby(['Hour'])['Balances MET POINT'].sum().to_frame()
outcome = pd.concat([outcome, new], axis = 1)

outcome['w_E6_Balances'] = (outcome['Balances MET POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100
outcome['w_MET_Balances'] = (outcome['Balances E6 POINT']/ (outcome['Balances E6 POINT'] + outcome['Balances MET POINT']))#*100

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
path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\Επιφάνεια εργασίας\NEW KPIs\MS\w+6 outcome.xlsx"
path = path.replace('\\', '/')
outcome.to_excel(path)
