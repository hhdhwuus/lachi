import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Load your dataset
data = pd.read_csv('./ProcessedData/combined_tage.csv')  # Adjust the path to your dataset
df = pd.read_csv(data)

# Umwandlung des Datums in ein datetime-Objekt und Hinzufügen einer Spalte für den Wochentag
df['datum'] = pd.to_datetime(df['datum'])
df['wochentag'] = df['datum'].dt.dayofweek  # Montag=0, Sonntag=6

# Einführung einer Spalte für Jahreszeiten: 0=Frühling, 1=Sommer, 2=Herbst, 3=Winter
# Definition der Jahreszeiten anhand von Monaten (vereinfachte Annahme)
seasons = {3: 0, 4: 0, 5: 0, # Frühling März, April, Mai
           6: 1, 7: 1, 8: 1, # Sommer Juni, Juli, August
           9: 2, 10: 2, 11: 2, # Herbst September, Oktober, November
           12: 3, 1: 3, 2: 3} # Winter Dezember, Januar, Februar

df['jahreszeit'] = df['datum'].dt.month.map(seasons)

# Gruppieren der Daten nach Jahreszeit und Wochentag, Berechnung des Durchschnitts
wochentags_durchschnitt = df.groupby(['jahreszeit', 'wochentag'])['gesamt'].mean().unstack()

# Visualisierung
fig, ax = plt.subplots(figsize=(10, 6))
wochentags_durchschnitt.plot(kind='bar', ax=ax)
ax.set_title('Durchschnittliche Anzahl von Fahrradfahrten nach Jahreszeit und Wochentag')
ax.set_xlabel('Jahreszeit (0=Frühling, 1=Sommer, 2=Herbst, 3=Winter)')
ax.set_ylabel('Durchschnittliche Anzahl von Fahrten')
ax.set_xticklabels(['Frühling', 'Sommer', 'Herbst', 'Winter'], rotation=45)
ax.legend(title='Wochentag', labels=['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])
plt.tight_layout()
plt.show()
