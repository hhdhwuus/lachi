import pandas as pd
import os

combined_tage_df = pd.read_csv(os.path.join('../ProcessedData/combined_tage.csv'))
combined_tage_df['datum'] = pd.to_datetime(combined_tage_df['datum'])

print("durchschnitt tag: ", combined_tage_df.groupby(combined_tage_df['datum'].dt.date)["gesamt"].sum().mean())

print("durchschnitt jahr:", combined_tage_df.groupby(combined_tage_df['datum'].dt.year)['gesamt'].sum().mean())

for station, group in combined_tage_df.groupby('zaehlstelle'):
    print(station, group['gesamt'].sum(), group['gesamt'].mean())



grouped_year_df = combined_tage_df.groupby(combined_tage_df['datum'].dt.year)['gesamt'].sum()

combined_tage_df = combined_tage_df[combined_tage_df['zaehlstelle'] != 'Kreuther']
combined_tage_df = combined_tage_df[combined_tage_df['zaehlstelle'] != 'Arnulf']


# Filtern der Daten für 2012 und 2022
data_2012 = combined_tage_df[combined_tage_df['datum'].dt.year == 2012]
data_2012 = data_2012.groupby(data_2012['datum'])
data_2022 = combined_tage_df[combined_tage_df['datum'].dt.year == 2022]
data_2022 = data_2022.groupby(data_2022['datum'])

# Berechnung der durchschnittlichen täglichen Radverkehrszahlen für beide Jahre
avg_daily_traffic_2012 = data_2012['gesamt'].sum().mean()
avg_daily_traffic_2022 = data_2022['gesamt'].sum().mean()

avg_daily_traffic_2012 = avg_daily_traffic_2012/4
avg_daily_traffic_2022 = avg_daily_traffic_2022/4

# Ausgabe der durchschnittlichen täglichen Radverkehrszahlen
print(avg_daily_traffic_2012, avg_daily_traffic_2022)
