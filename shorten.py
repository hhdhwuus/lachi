import pandas as pd

# Read the CSV file
df = pd.read_csv('combined_15min.csv')

# Convert the first column to datetime format
df['Date'] = pd.to_datetime(df['datum'])

# Sort the dataframe by the first column (date)
df = df.sort_values('Date')

# Get the current date
current_date = pd.to_datetime('today')

# Calculate the date 2 years ago
two_years_ago = current_date - pd.DateOffset(years=2)

# Filter the dataframe to include data from the last 2 years
df = df[df['Date'] >= two_years_ago]

# Save the filtered dataframe to a new CSV file
df.to_csv('filtered_15min.csv', index=False)