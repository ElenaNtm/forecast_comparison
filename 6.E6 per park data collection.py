#Libraries
import pandas as pd
import os
import numpy as np
from datetime import datetime
from matplotlib.dates import WeekdayLocator, DateFormatter
import matplotlib.dates as mdates
from openpyxl import load_workbook

#Load the data manually from the download (GEARS platform)
path = "C:/Users/Eleni/Downloads/DataExport-1-3-2024 (2).xlsx"
df1 = pd.read_excel(path)
path = "C:/Users/Eleni/Downloads/DataExport-1-3-2024 (3).xlsx"
df2 = pd.read_excel(path)
path = "C:/Users/Eleni/Downloads/DataExport-1-3-2024 (3).xlsx"
df2 = pd.read_excel(path)
path = "C:/Users/Eleni/Downloads/DataExport-1-3-2024 (4).xlsx"
df3 = pd.read_excel(path)
path = "C:/Users/Eleni/Downloads/DataExport-1-3-2024 (5).xlsx"
df4 = pd.read_excel(path)
path = "C:/Users/Eleni/Downloads/DataExport-1-3-2024 (6).xlsx"
df5 = pd.read_excel(path)
path = "C:/Users/Eleni/Downloads/DataExport-1-3-2024 (7).xlsx"
df6 = pd.read_excel(path)

#Change the format of the date column
df1['DateTime'] = pd.to_datetime(df1['DateTime'], format='%d/%m/%Y %H:%M')
df2['DateTime'] = pd.to_datetime(df2['DateTime'], format='%d/%m/%Y %H:%M')
df3['DateTime'] = pd.to_datetime(df3['DateTime'], format='%d/%m/%Y %H:%M')
df4['DateTime'] = pd.to_datetime(df4['DateTime'], format='%d/%m/%Y %H:%M')
df5['DateTime'] = pd.to_datetime(df5['DateTime'], format='%d/%m/%Y %H:%M')
df6['DateTime'] = pd.to_datetime(df6['DateTime'], format='%d/%m/%Y %H:%M')
#Set it as the index
df1.set_index('DateTime',inplace=True)
df2.set_index('DateTime',inplace=True)
df3.set_index('DateTime',inplace=True)
df4.set_index('DateTime',inplace=True)
df5.set_index('DateTime',inplace=True)
df6.set_index('DateTime',inplace=True)
#Connat all the data to one dataframe so that we have all the parks production in one file
df = pd.DataFrame()
df = pd.concat([df1,df2],axis=1)
df = pd.concat([df,df3],axis =1)
df = pd.concat([df,df4],axis =1)
df = pd.concat([df,df5],axis =1)
df = pd.concat([df,df6],axis =1)
df.columns = df.columns.str.replace('forecast', '')

# Create a list of columns to drop - these are the forecasts for the portfolio and not for each park
columns_to_drop = df.filter(like='GEARS_BZ01_NDR_SA_N').columns
# Drop the selected columns
df = df.drop(columns=columns_to_drop)

#Split the columns based on the Power or Energy to save them separetelly
mask_power = df.columns.str.contains("Power", case=False)
mask_energy = df.columns.str.contains("Energy", case=False)
df_power = df.loc[:, mask_power]
df_energy = df.loc[:, mask_energy]
output_directory = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/e6_forecast_data_split.xlsx"
with pd.ExcelWriter(output_directory) as writer:
    df_power.to_excel(writer, sheet_name='PowerSheet', index=True)
    df_energy.to_excel(writer, sheet_name='EnergySheet', index=True)
