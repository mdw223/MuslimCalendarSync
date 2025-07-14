
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO

def invoke(template:pd.DataFrame,data:pd.DataFrame) -> pd.DataFrame:
    # Prepare dataframes with month and year information
    df_data = data.copy()
    df_data['Year'] = 2025
    df_data['Month'] = 7

    # Clean 'Day' column: convert to numeric, coerce errors to NaN, then drop rows with NaN
    df_data['Day'] = pd.to_numeric(df_data['Day'], errors='coerce')
    df_data_cleaned = df_data.dropna(subset=['Day']).copy()
    df_data['Day'] = df_data_cleaned['Day'].astype(int) # Convert Day to integer after cleaning


    # Define the prayer time columns to iterate over
    prayer_cols = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']

    # List to store the generated event records
    event_records = []

    # Iterate through each row of the combined dataset to create calendar events
    for index, row in df_data_cleaned.iterrows():
        year = row['Year']
        month = row['Month']
        day = row['Day']

        for prayer_name in prayer_cols:
            prayer_time_str = str(row[prayer_name]).strip()

            # Skip if the prayer time string is empty, a header, or 'nan' (from NaN conversion)
            if not prayer_time_str or prayer_time_str in prayer_cols or prayer_time_str == 'nan':
                continue

            # Replace the narrow no-break space character with a regular space for parsing
            prayer_time_str = prayer_time_str.replace('\u202f', ' ')

            try:
                # Construct the full datetime string
                full_datetime_str = f"{year}-{month:02d}-{day:02d} {prayer_time_str}"

                # Parse the start datetime
                start_datetime = pd.to_datetime(full_datetime_str, format='%Y-%m-%d %I:%M %p')

                # Calculate the end datetime by adding 10 minutes
                end_datetime = start_datetime + pd.Timedelta(minutes=10)

                # Determine the event description
                if prayer_name == 'Sunrise':
                    description = 'Sunrise Description'
                else:
                    description = f"{prayer_name} Salah Description"

                # Append the new event record to the list
                event_records.append({
                    'Subject': prayer_name,
                    'Start Date': start_datetime.strftime('%Y-%m-%d'),
                    'Start Time': start_datetime.strftime('%I:%M %p'),
                    'End Date': end_datetime.strftime('%Y-%m-%d'),
                    'End Time': end_datetime.strftime('%I:%M %p'),
                    'All Day Event': False,
                    'Description': description,
                    'Private': True
                })
            except ValueError:
                # Skip rows where time parsing fails (e.g., malformed time strings)
                continue

    # Create the final output DataFrame from the list of event records
    output = pd.DataFrame(event_records)

    return output

# FINISH!
# Sample data as a string (you would typically read this from a CSV file)
data = """Athan Calendar
July 2025
Day, Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha
1,4:36 AM,6:02 AM,1:19 PM,5:07 PM,8:34 PM,10:01 PM
2,4:36 AM,6:03 AM,1:20 PM,5:07 PM,8:34 PM,10:01 PM
3,4:37 AM,6:03 AM,1:20 PM,5:08 PM,8:34 PM,10:00 PM
...
31,5:02 AM,6:22 AM,1:22 PM,5:07 PM,8:19 PM,9:39 PM
August 2025
Day, Fajr, Sunrise, Dhuhr, Asr, Maghrib, Isha
1,5:03 AM,6:23 AM,1:22 PM,5:07 PM,8:18 PM,9:38 PM
2,5:04 AM,6:23 AM,1:22 PM,5:07 PM,8:17 PM,9:37 PM
...
31,5:33 AM,6:46 AM,1:16 PM,4:52 PM,7:43 PM,8:55 PM
"""

# Use StringIO to simulate reading from a CSV file
data_io = StringIO(data)

# Read the data into a DataFrame, skipping the first row
lines = data_io.readlines()
months_data = {}
current_month = None

for line in lines:
    line = line.strip()
    if line and not line.startswith("Athan Calendar"):
        if not line[0].isdigit():  # Check if the line starts with a digit (indicating a day)
            current_month = line  # This is the month name
            continue

        # Read the data into a DataFrame
        if current_month not in months_data:
            months_data[current_month] = []

        # Split the line by commas and append to the current month's data
        months_data[current_month].append(line)

# Convert each month's data into a DataFrame
month_dfs = {}
for month, rows in months_data.items():
    # Create a DataFrame for the month, using the first row as the header
    month_df = pd.DataFrame([row.split(',') for row in rows[1:]], columns=rows[0].split(','))
    month_dfs[month] = month_df

# Now you can access each month's DataFrame
july_df = month_dfs['July 2025']
august_df = month_dfs['August 2025']

# Display the DataFrames
print("July 2025 DataFrame:")
print(july_df)
print("\nAugust 2025 DataFrame:")
print(august_df)

data = pd.read_csv('athan-calendar.csv')
#Google_Cal_Prayer_Times = invoke(template,data)
print(data)