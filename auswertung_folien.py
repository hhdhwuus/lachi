import pandas as pd
import os

combined_tage_df = pd.read_csv(os.path.join('./ProcessedData/combined_tage.csv'))

for station, group in combined_tage_df.groupby('zaehlstelle'):
    
    print(station, group['gesamt'].sum(), group['gesamt'].mean())
    