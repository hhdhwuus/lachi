import pandas as pd
import os

combined_tage_df = pd.read_csv(os.path.join('./ProcessedData/combined_tage.csv'))
combined_tage_df['datum'] = pd.to_datetime(combined_tage_df['datum'])

print("durchschnitt tag: ", combined_tage_df.groupby(combined_tage_df['datum'].dt.date)["gesamt"].sum().mean())

grouped_year_df = combined_tage_df.groupby(combined_tage_df['datum'].dt.year)['gesamt'].sum()

print("durchschnitt jahr:", grouped_year_df.mean())

for station, group in combined_tage_df.groupby('zaehlstelle'):
    
    print(station, group['gesamt'].sum(), group['gesamt'].mean())
    