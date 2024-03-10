import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
file_path = '../ProcessedData/combined_15min.csv'
data = pd.read_csv(file_path)

# Extract the hour from the time
data['uhrzeit'] = pd.to_datetime(data['uhrzeit_start'], format='%H:%M:%S').dt.hour

# Convert 'datum' to datetime format to work with it
data['datum'] = pd.to_datetime(data['datum'])

# Define the seasons
winter_months = [12, 1, 2]
spring_months = [3, 4, 5]
summer_months = [6, 7, 8]
autumn_months = [9, 10, 11]

# Filter data for each season
winter_data = data[data['datum'].dt.month.isin(winter_months)]
spring_data = data[data['datum'].dt.month.isin(spring_months)]
summer_data = data[data['datum'].dt.month.isin(summer_months)]
autumn_data = data[data['datum'].dt.month.isin(autumn_months)]

# Group by 'uhrzeit' and sum 'gesamt' for each season
winter_rides_per_hour = winter_data.groupby('uhrzeit')['gesamt'].sum()
spring_rides_per_hour = spring_data.groupby('uhrzeit')['gesamt'].sum()
summer_rides_per_hour = summer_data.groupby('uhrzeit')['gesamt'].sum()
autumn_rides_per_hour = autumn_data.groupby('uhrzeit')['gesamt'].sum()

# Calculate total rides for each season
total_winter_rides = winter_rides_per_hour.sum()
total_spring_rides = spring_rides_per_hour.sum()
total_summer_rides = summer_rides_per_hour.sum()
total_autumn_rides = autumn_rides_per_hour.sum()

# Calculate proportional rides per hour for each season
proportional_winter_rides_per_hour = (winter_rides_per_hour)
proportional_spring_rides_per_hour = (spring_rides_per_hour)
proportional_autumn_rides_per_hour = (autumn_rides_per_hour)
proportional_summer_rides_per_hour = (summer_rides_per_hour)

# combine all the data into a single dataframe into separate columns and save to a csv file
#combined_data = pd.concat([proportional_winter_rides_per_hour, proportional_spring_rides_per_hour, proportional_autumn_rides_per_hour, proportional_summer_rides_per_hour], axis=1)
#combined_data.columns = ['Winter', 'Spring', 'Autumn', 'Summer']
#combined_data.to_csv('ProcessedData/seasonal_rides_per_hour.csv')


# Plotting
plt.figure(figsize=(12, 6))
spring_bars = plt.bar(spring_rides_per_hour.index - 0.2, spring_rides_per_hour.values, width=0.2, color='green', label='Spring')
summer_bars = plt.bar(autumn_rides_per_hour.index + 0.0, summer_rides_per_hour.values, width=0.2, color='orange', label='Summer')
autumn_bars = plt.bar(summer_rides_per_hour.index + 0.2, autumn_rides_per_hour.values, width=0.2, color='brown', label='Autumn')
winter_bars = plt.bar(winter_rides_per_hour.index + 0.4, winter_rides_per_hour.values, width=0.2, color='skyblue', label='Winter')

plt.title('Proportional Rides per Hour in Each Season')
plt.xlabel('Hour of the Day')
plt.ylabel('Percentage of Total Rides (%)')
plt.xticks(np.arange(24))
plt.legend()
plt.grid(axis='y', linestyle='--')
plt.show()
