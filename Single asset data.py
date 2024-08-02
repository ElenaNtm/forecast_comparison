# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 17:17:50 2024

@author: Eleni
"""

import requests
from datetime import datetime, timedelta
import pandas as pd
#import os

path = r"C:\Users\Eleni\OneDrive - Hellenic Association for Energy Economics (1)\GEARS TASKS\ENPOWER Tasks\ChalkiOn\Forecasts\EN use\chalki forecast meteogen.xlsx"
forecast = pd.read_excel(path)
forecast.set_index('Valid Date', inplace = True) 
url = "https://www.meteogen.com/api/"
 
username = "georgitsioti@greenaggregator.com"
password = "c6V6TAG6XrFn"
 
auth_response = requests.post(url + "Authenticate/Login", json={"username": username, "password": password})
token = auth_response.json()["token"]
 
headers = {"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"}
 
# # This call fetches all the assets
# assets = requests.get(url + "Assets", headers=headers).json()
 
# if you only need one particular asset and you already know it's id, you can load it's details like this:
asset_id = 40766
asset = requests.get(url + f"Assets/{asset_id}", headers=headers).json()
 
# create an array with just the only asset we're dealing with:
assets = [asset]
 
df = "%Y-%m-%dT%H:%M:%SZ"
interval = "FifteenMinutes"  
 
start = datetime(year=2024, month=6, day=25)
end = datetime(year=2024, month=7, day=25)
 
current_date = start
 
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
 
#df.info()

#Convert to Greek summer time 
df["Valid Date"] = df["Valid Date UTC"] + pd.Timedelta(hours=3)
df.drop(['Valid Date UTC'], axis = 1)
df = df.set_index('Valid Date')

#Keep type and radiation
#df = df.drop(['Type', 'Radiation'], axis = 1)
df = df.drop(['Type'], axis = 1)

forecast = pd.concat([forecast,df], axis = 0)
#forecast.head()

#mask_power = df.columns.str.contains("Power", case=False)
#mask_energy = df.columns.str.contains("Energy", case=False)
#df_power = df.loc[:, mask_power]
#df_energy = df.loc[:, mask_energy]
#df_power.head()
forecast = forecast.sort_index()
duplicate_indexes = forecast.index.duplicated()

# Remove duplicate indexes
forecast = forecast[~duplicate_indexes]

forecast.to_excel(path, index=True)



