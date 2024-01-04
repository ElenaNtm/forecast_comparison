#Libraries
import requests
from datetime import datetime, timedelta
import pandas as pd
import os

#Preliminaries
url = "https://www.meteogen.com/api/"
username = "Input username"
password = "Input password"
auth_response = requests.post(url + "Authenticate/Login", json={"username": username, "password": password})
token = auth_response.json()["token"]

headers = {"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"}

# fetch all the assets
assets = requests.get(url + "Assets", headers=headers).json()
df = "%Y-%m-%dT%H:%M:%SZ"
interval = "FifteenMinutes"  # other valid values: "TenMinutes", "Hour"

#Set the dates that you are interested in 
start = datetime(year=2023, month=11, day=20)
end = datetime(year=2023, month=12, day=17)
current_date = start

#Set the directory and file name where you will save the data
output_excel_path = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/ENPOWER/Tasks/METEOGEN Analysis/historical_forecast_data.xlsx"

#Download the data
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
#We are not interested in the radiation and type for the time being
df = df.drop(['Type', 'Radiation'], axis = 1)

#Bring the data to a suitable format|Creating separate DataFrames for each group and saving them to a local drive
grouped = df.groupby('Asset')
output_directory = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/Επιφάνεια εργασίας/meteogen"

# Iterate over the groups
for asset, group_df in grouped:
    # Reset the index to make "Valid Date UTC+2" and 'Asset' columns again
    group_df.reset_index(inplace=True)
    
    # Create the full path for saving
    filename = os.path.join(output_directory, f"{asset}_data.csv")
    
    # Save the DataFrame to a CSV file
    group_df.to_csv(filename, index=False)

#Before reuploading check the files for data that should not be there 
#Reupload the individual csv files, rename the columns and concat them to one
csv_directory = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/Επιφάνεια εργασίας/meteogen"

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
    
    # Append the DataFrame to the list
    df = df.drop(['Asset', 'Valid Date UTC'], axis = 1)
    dfs.append(df)

# Specify the directory containing the CSV files
directory_path = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/Επιφάνεια εργασίας/meteogen"

# Get a list of all CSV files in the directory
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

# Initialize an empty DataFrame
concatenated_df = pd.DataFrame()

# Read each CSV file and concatenate into the DataFrame
for file in csv_files:
    file_path = os.path.join(directory_path, file)
    
    # Read the CSV file into a DataFrame with "Valid Date UTC+2" as the index
    df = pd.read_csv(file_path, parse_dates=['Valid Date UTC+2'])
    
    # Drop specified columns
    columns_to_drop = ['Valid Date UTC','Asset']
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    # Extract file name without extension
    file_name = os.path.splitext(file)[0]
    df = df.set_index('Valid Date UTC+2', inplace = False)
    # Reset the index and then use it as a regular column
    df.reset_index(inplace=True)
    
    # Assign each set of columns to the concatenated DataFrame with the modified column names
    for col in df.columns:
        concatenated_df[f"{file_name}_{col}"] = df[col]

  #Visualise the dataframe if needed
  #concatenated_df.tail()

concatenated_df = concatenated_df.set_index('AGR 26 KYPSELI (PARGA)_data_Valid Date UTC+2')
concatenated_df = concatenated_df.rename_axis('Valid Date UTC+2')

# Create a list of columns to drop
columns_to_drop = concatenated_df.filter(like='Valid Date UTC+2').columns

# Drop the selected columns
concatenated_df = concatenated_df.drop(columns=columns_to_drop)
concatenated_df = concatenated_df[~concatenated_df.index.duplicated(keep='first')]
concatenated_df.columns = concatenated_df.columns.str.replace('_data', '')

#Split to 2 dataframes, one for energy and the other for power 
mask_power = concatenated_df.columns.str.contains("Power", case=False)
mask_energy = concatenated_df.columns.str.contains("Energy", case=False)
df_power = concatenated_df.loc[:, mask_power]
df_energy = concatenated_df.loc[:, mask_energy]

output_directory = "C:/Users/Eleni/OneDrive - Hellenic Association for Energy Economics (1)/GEARS TASKS/Tasks/METEOGEN Analysis/historical_forecast_data_split.xlsx"
with pd.ExcelWriter(output_directory) as writer:
    df_power.to_excel(writer, sheet_name='PowerSheet', index=True)
    df_energy.to_excel(writer, sheet_name='EnergySheet', index=True)
