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
from openpyxl import load_workbook

#Load the data
path = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/met_e6_data.xlsx"
df = pd.read_excel(path)
df = df.set_index('Valid Date UTC+2')

#Check for nan data
# Check for NaN values
nan_check = df.isna()

any_nan_values = nan_check.any().any()
print(f"Any NaN values: {any_nan_values}")

#DAILY
#Create the KPIs for each day

"""
Split by day by day

DEV = ABS(SUM(MQ-FORECAST)) per every 15 minutes by day sum                             MWh
ADEV = SUM(ABS(MQ - FORECAST))                                                          MWh
NADEV = ADEV/(SUM(MQ))                                                                  percentage %
RMSDEV = SQRT(SUM((MQ - FORECAST)^2))                                                   MWh
ANDEV = SUM(DEV)/SUM(MQ) = SUM(ABS(SUM(MQ-FORECAST)))                                   percentage %
NRMSDEV = RMSDEV/SQRT(SUM(MQ^2)) = SQRT(SUM((MQ - FORECAST)^2))/SQRT(SUM(MQ^2))         percentage %           

"""

"""
DEV for MQ
"""
df['MQ - E6'] = df['MQ (MWh)'] - df['Energy E6 (MWh)']
daily_sum = df['MQ - E6'].resample('D').transform('sum')
df['dummy'] = daily_sum
df['E6 DEV'] = np.where(df['dummy'] < 0, -df['dummy'], df['dummy'])

df['MQ - MET'] = df['MQ (MWh)'] - df['MET Energy (MWh)']
daily_sum = df['MQ - MET'].resample('D').transform('sum')
df['dummy'] = daily_sum
df['MET DEV'] = np.where(df['dummy'] < 0, -df['dummy'], df['dummy'])

df['MQ - MS'] = df['MQ (MWh)'] - df['MS (ΜWh)']
daily_sum = df['MQ - MS'].resample('D').transform('sum')
df['dummy'] = daily_sum
df['MS DEV'] = np.where(df['dummy'] < 0, -df['dummy'], df['dummy'])

"""
ADEV
"""
df['MQ - E6'] = np.where(df['MQ - E6'] < 0, -df['MQ - E6'], df['MQ - E6'])
daily_sum = df['MQ - E6'].resample('D').transform('sum')
df['E6 ADEV'] = daily_sum

df['MQ - MET'] = np.where(df['MQ - MET'] < 0, -df['MQ - MET'], df['MQ - MET'])
daily_sum = df['MQ - MET'].resample('D').transform('sum')
df['MET ADEV'] = daily_sum

df['MQ - MS'] = np.where(df['MQ - MS'] < 0, -df['MQ - MS'], df['MQ - MS'])
daily_sum = df['MQ - MS'].resample('D').transform('sum')
df['MS ADEV'] = daily_sum

"""
NADEV
"""
daily_sum = df['MQ (MWh)'].resample('D').transform('sum')
df['DAILY SUM MQ'] = daily_sum

df['E6 NADEV'] = (df['E6 ADEV']/df['DAILY SUM MQ'])*100
df['MET NADEV'] = (df['MET ADEV']/df['DAILY SUM MQ'])*100
df['MS NADEV'] = (df['MS ADEV']/df['DAILY SUM MQ'])*100

"""
RMSDEV
"""
daily_sum = ((df['MQ - E6'])**2).resample('D').transform('sum')
df['E6 RMSDEV'] = (daily_sum)**(1/2)

daily_sum = ((df['MQ - MET'])**2).resample('D').transform('sum')
df['MET RMSDEV'] = (daily_sum)**(1/2)

daily_sum = ((df['MQ - MS'])**2).resample('D').transform('sum')
df['MS RMSDEV'] = (daily_sum)**(1/2)

"""
ANDEV
"""
df['E6 ANDEV'] = (df['E6 DEV']/df['DAILY SUM MQ'])*100
df['MET ANDEV'] = (df['MET DEV']/df['DAILY SUM MQ'])*100
df['MS ANDEV'] = (df['MS DEV']/df['DAILY SUM MQ'])*100

"""
NRMSDEV
"""
daily_sum = ((df['MQ (MWh)'])**2).resample('D').transform('sum')
df['dummy'] = (daily_sum)**(1/2)

df['E6 NRMSDEV'] = (df['E6 RMSDEV']/df['dummy'])*100
df['MET NRMSDEV'] = (df['MET RMSDEV']/df['dummy'])*100
df['MS NRMSDEV'] = (df['MS RMSDEV']/df['dummy'])*100

#Rename some columns
mapping = {'E6 DEV': 'E6 DEV (MWh)',
'MET DEV': 'MET DEV (MWh)',
'MS DEV': 'MS DEV (MWh)',
'E6 ADEV': 'E6 ADEV (MWh)',
'MET ADEV': 'MET ADEV (MWh)',
'MS ADEV': 'MS ADEV (MWh)',
'E6 NADEV': 'E6 NADEV (%)',
'MET NADEV': 'MET NADEV (%)',
'MS NADEV': 'MS NADEV (%)',
'E6 RMSDEV': 'E6 RMSDEV (MWh)',
'MET RMSDEV': 'MET RMSDEV (MWh)',
'MS RMSDEV': 'MS RMSDEV (MWh)',
'E6 NRMSDEV': 'E6 NRMSDEV (%)',
'MS NRMSDEV': 'MS NRMSDEV (%)',
'E6 ANDEV': "E6 ANDEV (%)",
'MS ANDEV': "MS ANDEV (%)",
'MET ANDEV': 'MET ANDEV (%)',
'MET NRMSDEV': 'MET NRMSDEV (%)'}
df.rename(columns = mapping, inplace=True)

#Save to new dataframe the KPIs
mask = df.index.time == pd.to_datetime('00:00:00').time() #this action is performed because we have the same values for each row that is refered to the same day - we keep only the first value
columns_to_select = ['E6 DEV (MWh)', 'MET DEV (MWh)', 'MS DEV (MWh)',
       'E6 ADEV (MWh)', 'MET ADEV (MWh)', 'MS ADEV (MWh)',
       'DAILY SUM MQ', 'E6 NADEV (%)', 'MET NADEV (%)',
       'MS NADEV (%)', 'E6 RMSDEV (MWh)', 'MET RMSDEV (MWh)',
       'MS RMSDEV (MWh)', 'E6 ANDEV (%)', 'MET ANDEV (%)',
       'MS ANDEV (%)', 'E6 NRMSDEV (%)', 'MET NRMSDEV (%)',
       'MS NRMSDEV (%)']
new_df = df[mask][columns_to_select]

#Save the data to an excel file with different sheets
path = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/weekly_KPIs.xlsx"
# Sort the DataFrame by the datetime index (if it's not already sorted)
new_df = new_df.sort_index()

# Group the DataFrame by week
weekly_groups = new_df.groupby(pd.Grouper(freq='W'))

# Create an Excel writer with the xlsxwriter engine
excel_writer = pd.ExcelWriter('path', engine='xlsxwriter')

# Iterate through the groups and save each week as a separate sheet
for week, week_data in weekly_groups:
    sheet_name = f'Week_{week.strftime("%Y-%m-%d")}'
    week_data.to_excel(excel_writer, sheet_name=sheet_name)

# Save the Excel file
excel_writer.close()

#WEEKLY
#Create the KPIs for each week
df_new = pd.DataFrame()

"""
MQ
"""
weekly_sum = (df['MQ (MWh)']).resample('W').transform('sum')
df_new['weekly MQ'] = weekly_sum

"""
ADEV
"""
#df['MQ - E6'] = np.where(df['MQ - E6'] < 0, -df['MQ - E6'], df['MQ - E6'])
weekly_sum = df['MQ - E6'].resample('W').transform('sum')
df_new['weekly E6 ADEV'] = weekly_sum

weekly_sum = df['MQ - MET'].resample('W').transform('sum')
df_new['weekly MET ADEV'] = weekly_sum

weekly_sum = df['MQ - MS'].resample('W').transform('sum')
df_new['weekly MS ADEV'] = weekly_sum

"""
NADEV
"""
df_new['weekly E6 NADEV'] = (df_new['weekly E6 ADEV']/df_new['weekly MQ'])*100
df_new['weekly MET NADEV'] = (df_new['weekly MET ADEV']/df_new['weekly MQ'])*100
df_new['weekly MS NADEV'] = (df_new['weekly MS ADEV']/df_new['weekly MQ'])*100

"""
RMSDEV
"""
weekly_sum = ((df['MQ - E6'])**2).resample('W').transform('sum')
df_new['weekly E6 RMSDEV'] = (weekly_sum)**(1/2)
weekly_sum = ((df['MQ - MET'])**2).resample('W').transform('sum')
df_new['weekly MET RMSDEV'] = (weekly_sum)**(1/2)
weekly_sum = ((df['MQ - MS'])**2).resample('W').transform('sum')
df_new['weekly MS RMSDEV'] = (weekly_sum)**(1/2)

"""
NRMSDEV
"""
weekly_sum = ((df['MQ (MWh)'])**2).resample('W').transform('sum')
df['dummy'] = (weekly_sum)**(1/2)
df_new['weekly E6 NRMSDEV'] = (df_new['weekly E6 RMSDEV']/df['dummy'])*100
df_new['weekly MET NRMSDEV'] = (df_new['weekly MET RMSDEV']/df['dummy'])*100
df_new['weekly MS NRMSDEV'] = (df_new['weekly MS RMSDEV']/df['dummy'])*100

#Filter and keep only Monday and the first entry for the same reason we kept the first row for each day above
df_new = df_new[(df_new.index.time == pd.to_datetime('00:00:00').time()) & (df_new.index.day_name() == 'Monday')]

#Save to different file
path = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/KPIs_for_ther_week.xlsx"
data = pd.read_excel(path)
data.set_index('Valid Date UTC+2', inplace = True)
df_new = pd.concat([df_new, data], axis = 0)
df_new.to_excel(path,index=True)

"""
TOLLERANCE

NCBALR_C1p,m=0 only if both A & B ≤ 0, otherwise =MAX(A,B) 
NCBALR_C2p,m=0 only if ANDEV < 𝑻𝑶𝑳𝒓,𝑫𝑬𝑽_NORM 
NADEV < 𝑻𝑶𝑳𝒓,𝑨𝑫𝑬𝑽 (%) 
NRMSDEV < 𝑻𝑶𝑳𝒓, 𝑹𝑴𝑺𝑫𝑬𝑽 (%) 

Α = (𝑈𝑁𝐶𝐵𝐴𝐿𝑅𝐴𝐷𝐸𝑉 ∗ 𝐴𝐷𝐸𝑉𝑝,𝑚) ∗ (𝑁𝐴𝐷𝐸𝑉𝑝,𝑚 − 𝑇𝑂𝐿𝑟,𝐴𝐷𝐸𝑉) (€)
Β = (𝑈𝑁𝐶𝐵𝐴𝐿𝑅𝑅𝑀𝑆𝐷𝐸𝑉 ∗ 𝑅𝑀𝑆𝐷𝐸𝑉𝑝,𝑚) ∗ (𝑁𝑅𝑀𝑆𝐷𝐸𝑉𝑝,𝑚 − 𝑇𝑂𝐿𝑟,𝑅𝑀𝑆𝐷𝐸𝑉) (€)

These constants can change, they depend from IPTO 
α2ADEV = -0.009 
α2RMSDEV = -0.009
α3ADEV = 0.28 
α3RMSDEV = 0.28 
α1ADEV = 0.35 
α1RMSDEV = 0.4
UNCBALR, ADEV  €/MWh = 10 
UNCBALR, RMSDEV €/MWh = 210 
minTOLADEV =20% 
minTOLRMSDEV = 20% 
maxTOLADEV = 100% 
maxTOLRMSDEV = 100% 
maxTOL_DEV_NORM = 0.27
minTOL_DEV_NORM = 0.0109
a1DEV_NORM = 0.27
a2DEV_NORM = 0.0109
a3DEV_NORM = 0.28
"""
df_tol = pd.DataFrame()

#Set the constants
a1ADEV = 0.35
a1RMSDEV = 0.4
a2ADEV = -0.009
a2RMSDEV = a2ADEV
a3ADEV = 0.28
a3RMSDEV = a3ADEV
UNCBALR_ADEV = 10 #EURO/MWh
UNCBALR_RMSDEV = 210 #EURO/MWh
min_TOLADEV = 0.20 #20%
minTOLRMSDEV = 0.20#20%
maxTOLADEV = 1#100%
maxTOLRMSDEV = 1#100%
maxTOL_DEV_NORM = 1#100%
minTOL_DEV_NORM = 0.0005#0.05%
a1DEV_NORM = 0.27
a2DEV_NORM = -0.0109
a3DEV_NORM = 0.28

"""
TOL_ADEV
𝑻𝑶𝑳𝒓,𝑨𝑫𝑬𝑽 (%) = MAX(minTOLADEV,MIN(maxTOLADEV, α1ADEV+ α2ADEV*MQ^ α3ADEV))
"""
def calculate_TOL_ADEV(x):
    return max(min_TOLADEV, min(maxTOLADEV, (a1ADEV + (a2ADEV * (x ** a3ADEV)))))

# Apply the function to each element of the 'MQ weekly' column
df_tol['TOL_ADEV'] = df_new['weekly MQ'].apply(calculate_TOL_ADEV)

"""
TOL_DEV_NORM
𝑻𝑶𝑳𝒓,𝑫𝑬𝑽_NORM (%) = MAX(minTOL DEV_NORM, MIN(maxTOL DEV_NORM, α1DEV_NORM+ α2DEV_NORM *MQ^ α3DEV_NORM)
"""
def calculate_TOL_DEV_NORM(x):
    return max(minTOL_DEV_NORM, min(maxTOL_DEV_NORM, a1DEV_NORM + a2DEV_NORM * (x ** a3DEV_NORM)))

# Apply the function to each element of the 'MQ weekly' column
df_tol['TOL_DEV_NORM'] = df_new['weekly MQ'].apply(calculate_TOL_DEV_NORM)

"""
TOL_RMSDEV
𝑻𝑶𝑳𝒓,𝑹𝑴𝑺𝑫𝑬𝑽 (%) = MAX(minTOLRMSDEV,MIN(maxTOLRMSDEV, α1RMSDEV+ α2RMSDEV*MQ^ α3RMSDEV))
"""
def calculate_TOL_RMSDEV(x):
    return max(minTOLRMSDEV, min(maxTOLRMSDEV, a1RMSDEV + a2RMSDEV * (x ** a3RMSDEV)))

# Apply the function to each element of the 'MQ weekly' column
df_tol['TOL_RMSDEV'] = df_new['weekly MQ'].apply(calculate_TOL_RMSDEV)

"""
Α = (UNCBALR, ADEV  €/MWh * ADEV) * (NADEV - 𝑻𝑶𝑳𝒓,𝑨𝑫𝑬𝑽 (%)) (€)
"""
df_tol['E6 A'] = (UNCBALR_ADEV*df_new['weekly E6 ADEV'])*(df_new['weekly E6 NADEV']/100-df_tol['TOL_ADEV'])
df_tol['MET A'] = (UNCBALR_ADEV* df_new['weekly MET ADEV'])*(df_new['weekly MET NADEV']/100-df_tol['TOL_ADEV'])
df_tol['MS A'] = UNCBALR_ADEV* df_new['weekly MS ADEV']*(df_new['weekly MS NADEV']/100-df_tol['TOL_ADEV'])

"""
B = (UNCBALR, RMSDEV €/MWh * RMSDEV) * (NRMSDEV - 𝑻𝑶𝑳𝒓,𝑹𝑴𝑺𝑫𝑬𝑽 (%))(€)
"""
df_tol['E6 B'] = UNCBALR_RMSDEV* df_new['weekly E6 RMSDEV']*(df_new['weekly E6 NRMSDEV']/100-df_tol['TOL_RMSDEV'])
df_tol['MET B'] = UNCBALR_RMSDEV* df_new['weekly MET RMSDEV']*(df_new['weekly MET NRMSDEV']/100-df_tol['TOL_RMSDEV'])
df_tol['MS B'] = UNCBALR_RMSDEV* df_new['weekly MS RMSDEV']*(df_new['weekly MS NRMSDEV']/100-df_tol['TOL_RMSDEV'])

#Check for nan values
nan_values = df_new.isna()
# Printing the positions of True values
true_positions = nan_values.stack().loc[lambda x: x].index
print("\nPositions of True values:")
print(true_positions)

"""
NCBALR_C1 = 0 <-> A & B <=0
ELSE|    NCBALR_C1 = MAX(A,B)
"""
if (df_tol['E6 A'] <= 0).all() and (df_tol['E6 B'] <= 0).all():
    df_tol['NCBALR_C1 E6'] = 0
else:
     df_tol['NCBALR_C1 E6'] = df_tol[['E6 A', 'E6 B']].max(axis=1)
  
if (df_tol['MET A'] <= 0).all() and (df_tol['MET B'] <= 0).all():
    df_tol['NCBALR_C1 MET'] = 0
else:
     df_tol['NCBALR_C1 MET'] = df_tol[['MET A', 'MET B']].max(axis=1)

if (df_tol['MS A'] <= 0).all() and (df_tol['MS B'] <= 0).all():
    df_tol['NCBALR_C1 MS'] = 0
else:
     df_tol['NCBALR_C1 MS'] = df_tol[['MS A', 'MS B']].max(axis=1)

"""
NCBALR_C2 = 0 <-> ANDEV < 𝑻𝑶𝑳𝒓,𝑫𝑬𝑽_NORM (%)
"""
if (df_new['weekly E6 ADEV'] < df_tol['TOL_DEV_NORM']).all():
    df_tol['NCBALR_C2 E6'] = 0
else:
    df_tol['NCBALR_C2 E6'] = -1

if (df_new['weekly MET ADEV'] < df_tol['TOL_DEV_NORM']).all():
    df_tol['NCBALR_C2 MET'] = 0
else:
    df_tol['NCBALR_C2 MET'] = -1

if (df_new['weekly MS ADEV'] < df_tol['TOL_DEV_NORM']).all():
    df_tol['NCBALR_C2 MS'] = 0
else:
    df_tol['NCBALR_C2 MS'] = -1

#Save the data
path = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/tolerance.xlsx"
# Create an ExcelWriter object
writer = pd.ExcelWriter(path, engine='xlsxwriter')
# Iterate over each week (Monday to Sunday) and write to a separate sheet
for start_date, groups in df_tol.groupby(pd.Grouper(freq='W-Mon', closed='left', label='left')):
    end_date = start_date + pd.DateOffset(days=6)
    
    sheet_name = f'{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}'
    
    groups.to_excel(writer, header= True, sheet_name=sheet_name)

# Close the ExcelWriter, and the file will be saved automatically
writer.close()



























