# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 10:55:48 2024

@author: Eleni
"""

#Libraries
import requests
from datetime import datetime, timedelta
#import csv
import pandas as pd
import os

#Preliminaries
url = "https://www.meteogen.com/api/"

username = "your username"
password = "your password"

auth_response = requests.post(url + "Authenticate/Login", json={"username": username, "password": password})
token = auth_response.json()["token"]

headers = {"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"}

# fetch all the assets
assets = requests.get(url + "Assets", headers=headers).json()

df = "%Y-%m-%dT%H:%M:%SZ"
interval = "FifteenMinutes"  # other valid values: "TenMinutes", "Hour"

#Dates to be added, manually set them
start = datetime(year=2023, month=12, day=20)
end = datetime(year=2023, month=12, day=25)
current_date = start

#Set the directory
output_excel_path = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/ENPOWER/Tasks/METEOGEN Analysis/historical_forecast_data.xlsx"

data = []

while current_date < end:
    # fetch forecasts for 1 day
    request_start = current_date
    request_end = current_date + timedelta(hours=24)
    for a in assets:
        forecast_json_body = {"from": start.strftime(df), "to": end.strftime(df), "interval": interval}
        forecast_response = requests.post(url + "Assets/{}/Forecast".format(a["id"]), headers=headers, json=forecast_json_body)

        if forecast_response.status_code != 200:
            print("Error fetching forecasts with status code {}".format(forecast_response.status_code))
            exit()

        forecasts = forecast_response.json()
        for f in forecasts:
            data.append([a["name"], a["type"], datetime.strptime(f["validDate"], df), f["energy"], f["power"], f["radiation"]])

    #print(current_date)
    #advance by a day
    current_date = current_date + timedelta(hours=24)

df = pd.DataFrame(data, columns=["Asset", "Type", "Valid Date UTC", "Energy KWh", "Power KW", "Radiation"])

#Convert to UTC+2 for winter time and UTC+3 for summer time 
df["Valid Date UTC+2"] = df["Valid Date UTC"] + pd.Timedelta(hours=2)
df.drop(['Valid Date UTC'], axis = 1)
df = df.set_index('Valid Date UTC+2')
df = df.drop(['Type', 'Radiation'], axis = 1)
#df.tail()
#Bring the data to a suitable format|Creating separate DataFrames for each group and saving them to a local drive
grouped = df.groupby('Asset')
#We have a separate directory for the new data, only after checking it we will concat them with the old files
output_directory = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/Επιφάνεια εργασίας/met"

# Iterate over the groups
for asset, group_df in grouped:
    # Reset the index to make "Valid Date UTC+2" and 'Asset' columns again
    group_df.reset_index(inplace=True)
    
    # Create the full path for saving
    filename = os.path.join(output_directory, f"{asset}_data.csv")
    
    # Save the DataFrame to a CSV file
    group_df.to_csv(filename, index=False)
"""
#Concat the dataframesby name and save them to the initial directory where the old files are
# Specify the directories
dir_path1 = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/Επιφάνεια εργασίας/meteogen"#old data directory
dir_path2 = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/Επιφάνεια εργασίας/meteogen/met"#new data directory

# Function to merge CSV files with the same name from two directories
def merge_and_save_csv_files(dir_path1, dir_path2):
    all_files_dir1 = [f for f in os.listdir(dir_path1) if f.endswith('.csv')]
    all_files_dir2 = [f for f in os.listdir(dir_path2) if f.endswith('.csv')]
    common_files = set(all_files_dir1) & set(all_files_dir2)

    for file in common_files:
        file_path_dir1 = os.path.join(dir_path1, file)
        file_path_dir2 = os.path.join(dir_path2, file)

        df1 = pd.read_csv(file_path_dir1)
        df2 = pd.read_csv(file_path_dir2)

        # Assuming you want to merge based on a common column, adjust the 'on' parameter accordingly
        merged_df = pd.merge(df1, df2, on=df1.columns.tolist(), how='outer')

        # Save the merged DataFrame to the first directory, replacing the old file
        merged_file_path = os.path.join(dir_path1, file)
        merged_df.to_csv(merged_file_path, index=False)

# Merge CSV files with the same name from both directories and save them back to the first directory
merge_and_save_csv_files(dir_path1,dir_path2)
"""
"""
csv_directory = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/Επιφάνεια εργασίας/met"

# List all files in the directory
csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]

# Create an empty list to store DataFrames
dfs = []

# Loop through each CSV file and read it into a DataFrame
for file in csv_files:
    # Construct the full path to the CSV file
    file_path = os.path.join(csv_directory, file)
    
    # Read the CSV file into a DataFrame and set 'Valid Date UTC+2' as the index
    df = pd.read_csv(file_path, parse_dates=['Valid Date UTC+2'], index_col='Valid Date UTC+2')
    
    # Extract the value from the second row of the 'asset' column
    new_column_name = df['Asset'][1] + 'Energy KWh'
    df.rename(columns={'Energy KWh': new_column_name}, inplace=True)
    
    new_column_name = df['Asset'][1] + 'Power KW'
    df.rename(columns={'Power KW': new_column_name}, inplace=True)
    
    #new_column_name = df['Radiation'][1] + 'Radiation'
    #df.rename(columns={'Radiation': new_column_name}, inplace=True)
    
    # Append the DataFrame to the list
    df = df.drop(['Asset', 'Valid Date UTC'], axis = 1)
    dfs.append(df)
"""
# Specify the directory containing the CSV files
directory_path = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/Επιφάνεια εργασίας/met"

# Get a list of all CSV files in the directory
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

# Initialize an empty DataFrame
concatenated_df = pd.DataFrame()

# Read each CSV file and concatenate into the DataFrame
for file in csv_files:
    file_path = os.path.join(directory_path, file)
    
    # Read the CSV file into a DataFrame with "Valid Date UTC+2" as the index
    df = pd.read_csv(file_path, parse_dates=['Valid Date UTC+2'])
    
    # Rename columns
    # If needed, you can customize the column renaming based on your CSV files
    
    # Drop specified columns
    columns_to_drop = ['Valid Date UTC','Asset']
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    # Extract file name without extension
    file_name = os.path.splitext(file)[0]
    df = df.set_index('Valid Date UTC+2', inplace = False)
    # Reset the index and then use it as a regular column
    df.reset_index(inplace=True)
    
    # Set the name of the index explicitly
    #df.index.name = 'Valid Date UTC+2'
    
    # Assign each set of columns to the concatenated DataFrame with the modified column names
    for col in df.columns:
        concatenated_df[f"{file_name}_{col}"] = df[col]


# Set "Valid Date UTC+2" as the index again
#concatenated_df.set_index('Valid Date UTC+2', inplace=True)
concatenated_df.set_index("AGR 26 KYPSELI (PARGA)_data_Valid Date UTC+2", inplace=True)
concatenated_df = concatenated_df.rename_axis('Valid Date UTC+2')
concatenated_df = concatenated_df[~concatenated_df.index.duplicated(keep='first')]
concatenated_df.columns = concatenated_df.columns.str.replace('_data', '')
columns_to_drop = concatenated_df.filter(like='Valid Date UTC+2').columns
concatenated_df = concatenated_df.drop(columns=columns_to_drop)

#Split to two different dataframes and later to two different sheets
mask_power = concatenated_df.columns.str.contains("Power", case=False)
mask_energy = concatenated_df.columns.str.contains("Energy", case=False)
df_power = concatenated_df.loc[:, mask_power]
df_energy = concatenated_df.loc[:, mask_energy]

output_directory = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/temp_forecast_data_split.xlsx"
with pd.ExcelWriter(output_directory) as writer:
    df_power.to_excel(writer, sheet_name='PowerSheet', index=True)
    df_energy.to_excel(writer, sheet_name='EnergySheet', index=True)
    
df1 = pd.read_excel(output_directory,sheet_name='EnergySheet')
df2 = pd.read_excel(output_directory,sheet_name='PowerSheet')
df1.set_index('Valid Date UTC+2', inplace = True)
df2.set_index('Valid Date UTC+2', inplace = True)

output_directory = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/historical_forecast_data_split.xlsx"
df = pd.read_excel(output_directory,sheet_name='EnergySheet')
df_ = pd.read_excel(output_directory,sheet_name='PowerSheet')
df.set_index('Valid Date UTC+2', inplace = True)
df_.set_index('Valid Date UTC+2', inplace = True)

"""
# Drop rows where the index is greater than December 18th, 2023
cutoff_date = pd.to_datetime('2023-12-10 02:00:00')
df = df[df.index < cutoff_date]
df_ = df_[df_.index < cutoff_date]
"""

result = pd.concat([df,df1], axis = 0 )
result_ = pd.concat([df_,df2],axis = 0)

#Save to the initial file the appended version
output_directory = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/historical_forecast_data_split.xlsx"
with pd.ExcelWriter(output_directory) as writer:
    result.to_excel(writer, sheet_name='EnergySheet', index=True)
    result_.to_excel(writer, sheet_name='PowerSheet', index=True)
