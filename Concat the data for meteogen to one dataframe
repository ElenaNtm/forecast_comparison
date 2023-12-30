#Libraries

#Reupload the individual csv files, rename the columns and concat them to one
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
