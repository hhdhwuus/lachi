import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# Define the base directory where the CSV files are located
base_dir = './FahrradMuenchen'

# Function to read and filter 15min files
def process_15min_files():
    # Pattern to match 15min files
    pattern = os.path.join(base_dir, '*15min*.csv')
    files = glob.glob(pattern)
    
    # Combine files with appropriate filtering
    combined_df = pd.DataFrame()
    for file in files:
        df = pd.read_csv(file)
        # Filter out rows where 'richtung_1' or 'richtung_2' is NA
        df_filtered = df[(df['richtung_1'] != 'NA') & (df['richtung_2'] != 'NA')].fillna(0)
        combined_df = pd.concat([combined_df, df_filtered], ignore_index=True)
    
    return combined_df

# Function to read and filter tage files
def process_tage_files():
    # Pattern to match tage files
    pattern = os.path.join(base_dir, '*tage*.csv')
    files = glob.glob(pattern)
    
    # Combine files with appropriate filtering and column removal
    combined_df = pd.DataFrame()
    for file in files:
        df = pd.read_csv(file)
        # Filter out rows where 'richtung_1' or 'richtung_2' is NA
        df_filtered = df[(df['richtung_1'] != 'NA') & (df['richtung_2'] != 'NA')]
        # Drop 'uhrzeit_start' and 'uhrzeit_ende' columns
        df_filtered = df_filtered.drop(columns=['uhrzeit_start', 'uhrzeit_ende']).fillna(0)
        combined_df = pd.concat([combined_df, df_filtered], ignore_index=True)
    
    return combined_df

# Process files
if not (os.path.join(base_dir, 'combined_15min.csv')):
    combined_15min_df = process_15min_files()
    combined_15min_df.to_csv(os.path.join(base_dir, 'combined_15min.csv'), index=False)
    print("15 min files have been processed and combined.")

if not (os.path.join(base_dir, 'combined_tage.csv')):
    combined_tage_df = process_tage_files()
    combined_tage_df.to_csv(os.path.join(base_dir, 'combined_tage.csv'), index=False)
    print("Day files have been processed and combined.")



# Deskriptive Analyse
combined_tage_df = pd.read_csv(os.path.join(base_dir, 'combined_tage.csv'))

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

station_totals = combined_tage_df.groupby('zaehlstelle')['gesamt'].mean()

# Plot a pie chart for daily rides by counting station
plt.figure(figsize=(10, 8))
station_totals.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Durschnittliche tägliche Fahrten nach Zählstellen')
plt.ylabel('')  # Remove the y-label as it's not needed for pie charts
plt.show()

# Plot distribution of total daily bike rides
plt.figure(figsize=(12, 6))
sns.histplot(combined_tage_df['gesamt'], bins=50, kde=False)
plt.title('Verteilung der täglichen Fahrradfahrten (Gesamt)')
plt.xlabel('Anzahl der Fahrradfahrten')
plt.ylabel('Häufigkeit')
plt.show()

# Relationship between bike rides and weather conditions
fig, axs = plt.subplots(3, 1, figsize=(12, 18))

# Temperature vs. Bike Rides
sns.scatterplot(x='max.temp', y='gesamt', data=combined_tage_df, ax=axs[0], alpha=0.5)
axs[0].set_title('Maximale Temperatur vs. Gesamtanzahl der Fahrradfahrten')
axs[0].set_xlabel('Maximale Temperatur (°C)')
axs[0].set_ylabel('Gesamtanzahl der Fahrradfahrten')

# Precipitation vs. Bike Rides
sns.scatterplot(x='niederschlag', y='gesamt', data=combined_tage_df, ax=axs[1], alpha=0.5)
axs[1].set_title('Niederschlag vs. Gesamtanzahl der Fahrradfahrten')
axs[1].set_xlabel('Niederschlag (mm)')
axs[1].set_ylabel('Gesamtanzahl der Fahrradfahrten')

# Sun Hours vs. Bike Rides
sns.scatterplot(x='sonnenstunden', y='gesamt', data=combined_tage_df, ax=axs[2], alpha=0.5)
axs[2].set_title('Sonnenstunden vs. Gesamtanzahl der Fahrradfahrten')
axs[2].set_xlabel('Sonnenstunden')
axs[2].set_ylabel('Gesamtanzahl der Fahrradfahrten')

plt.tight_layout()
plt.show()

for station, group in combined_tage_df.groupby('zaehlstelle'):
    # Calculating descriptive statistics for 'gesamt' column
    desc_stats = group['gesamt'].describe()
    mode = group['gesamt'].mode().iloc[0]
    range_value = desc_stats['max'] - desc_stats['min']

    # Create a plot page
    plt.figure(figsize=(10, 6))
    plt.bar(['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max'],
            [desc_stats['count'], desc_stats['mean'], desc_stats['std'], desc_stats['min'],
            desc_stats['25%'], desc_stats['50%'], desc_stats['75%'], desc_stats['max']])
    plt.title(f'Deskriptive Statistiken für Gesamtfahrten - {station}')
    plt.xticks(rotation=45)
    plt.ylabel('Wert')
    plt.tight_layout()
    plt.show()


