import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# Define the base directory where the CSV files are located
base_dir = './FahrradMuenchen'
combined_tage_df = pd.read_csv(os.path.join(base_dir, 'combined_tage.csv'))
print(combined_tage_df)


# Wie beeinflusst Temperatur Anzahl der Fahrradfahrer?