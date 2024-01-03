#Libraries
import requests
from datetime import datetime, timedelta
#import csv
import pandas as pd
import os

#Preliminaries
url = "https://www.meteogen.com/api/"

username = "your username"
password = "your pass"

auth_response = requests.post(url + "Authenticate/Login", json={"username": username, "password": password})
token = auth_response.json()["token"]

headers = {"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"}

# fetch all the assets
assets = requests.get(url + "Assets", headers=headers).json()

df = "%Y-%m-%dT%H:%M:%SZ"
interval = "FifteenMinutes"  # other valid values: "TenMinutes", "Hour"

#Dates to be added
start = datetime(year=2023, month=12, day=13)
end = datetime(year=2023, month=12, day=20)
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
