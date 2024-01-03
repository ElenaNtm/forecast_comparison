#Libraries
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import numpy as np
from datetime import datetime
from matplotlib.dates import WeekdayLocator, DateFormatter
import matplotlib.dates as mdates

#Load the data from the downloads, the path must be changed every time you run this code
#And the dataframe with the already existing data

#This is the new data for E6 from the GEARS platform
path = "C:/Users/Eleni/Downloads/DataExport-12-22-2023.xlsx"
df = pd.read_excel(path)

df['DateTime'] = pd.to_datetime(df['DateTime'], format='%d/%m/%Y %H:%M')

#Brind the column names and data to the same format as with METEOGEN
#Manipulate the data so that we have MWh instead of KWh
#rename columns
df = df.rename(columns={'DateTime':'Valid Date UTC+2','Energy forecast - GEARS_BZ01_NDR_SA_N (KWh)':'Energy E6 (MWh)', "MQ - GEARS_BZ01_NDR_SA_N (ΜWh)":'MQ (MWh)','IPTO W+1 - GEARS_BZ01_NDR_SA_N (KWh)':'W+1 (MWh)','MS - GEARS_BZ01_NDR_SA_N (ΜWh)':"MS (ΜWh)"})
df['Energy E6 (MWh)'] = df['Energy E6 (MWh)']/1000
df['W+1 (MWh)'] = df['W+1 (MWh)']/1000
df["MS (ΜWh)"] = df["MS (ΜWh)"]/1000
df.set_index('Valid Date UTC+2', inplace=True)

#Load the old data to concatenate them with the new data
path = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/met_e6_data.xlsx"
data = pd.read_excel(path)
data = data.set_index('Valid Date UTC+2')

result = pd.concat([df, data])

#Load the meteogen data
path = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/historical_forecast_data_split.xlsx"
met = pd.read_excel(path, sheet_name='EnergySheet')
met['Valid Date UTC+2'] = pd.to_datetime(met['Valid Date UTC+2'])
met = met.set_index('Valid Date UTC+2')

#Sum the energy produced by 15 minutes
met['MET Energy (MWh)'] = met.sum(axis=1)
#met.head()
new = pd.DataFrame()
new['MET Energy (MWh)'] = met['MET Energy (MWh)']

#Keep only the last week, as we download the data weeek by week for this procedure
# Find the last week's start date
last_week_start = new.index[-1] - pd.DateOffset(weeks=1)

# Filter the DataFrame to keep only the last week
df_last_week = new.loc[last_week_start:]

"""
Check your data in the df_last_week to ensure that you have the right dates, if needed act accordingly

Drop the first row
df_last_week = df_last_week.iloc[1:]

Drop the last row
df_last_week = df_last_week.iloc[:-1]

Drop rows where the index is greater than December 18th, 2023
cutoff_date = pd.to_datetime('2023-12-11 00:00:00')
data = data[data.index <= cutoff_date]
result = result.drop(result.index[-1])
result.head()

Drop rows where the index is smaller than December 18th, 2023
cutoff_date = pd.to_datetime('2023-12-11 00:00:00')
data = data[data.index > cutoff_date]
result = result.drop(result.index[-1])
result.head()
"""

#Concat to one dataframe the sum
result = pd.concat([result, df_last_week])

#Some random columns was created so we drop it, check before performing this actions
#result = result.drop(0, axis = 1)

#Save the file
path = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/met_e6_data.xlsx"
result.to_excel(path, index = True)
