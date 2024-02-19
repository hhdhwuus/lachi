import pandas as pd
import os
import glob

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
combined_15min_df = process_15min_files()
combined_tage_df = process_tage_files()

# Save the combined files to new CSV files
combined_15min_df.to_csv(os.path.join(base_dir, 'combined_15min.csv'), index=False)
combined_tage_df.to_csv(os.path.join(base_dir, 'combined_tage.csv'), index=False)

print("Files have been processed and combined.")
