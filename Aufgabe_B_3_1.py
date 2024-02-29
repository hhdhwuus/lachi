from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import inquirer



# Einlesen des Datensatzes
data_15min = pd.read_csv('./ProcessedData/combined_15min.csv')  # Pfad anpassen

# Vorbereitung der Daten
data_15min['datum'] = pd.to_datetime(data_15min['datum'])
data_15min['tag_typ'] = data_15min['datum'].dt.dayofweek.apply(lambda x: 'Wochenende' if x >= 5 else 'Werktag')
data_15min['uhrzeit'] = pd.to_datetime(data_15min['uhrzeit_start'], format='%H:%M:%S').dt.hour

questions = [
    inquirer.List(
        "zaehlstelle",
        message="Zählstation auswählen",
        choices=data_15min['zaehlstelle'].unique().tolist(),
    ),
]
# Auswahl der Daten für eine bestimmte Zählstation
zaehlstelle = inquirer.prompt(questions)['zaehlstelle']

print("zeige Daten für " + zaehlstelle)
data_station = data_15min[data_15min['zaehlstelle'] == zaehlstelle]

# Plotgröße anpassen
fig, axs = plt.subplots(2, 1, figsize=(15, 7))  # Modified figsize to (15, 7)

# Breite der Balken
bar_width = 0.35

# Tagtypen
tag_typen = ['Werktag', 'Wochenende']

for i, tag_typ in enumerate(tag_typen):
    # Berechnung der Gesamtzahl der Fahrten pro Stunde und Richtung für den jeweiligen Tagtyp
    total_rides_per_hour_r1 = data_station[data_station['tag_typ'] == tag_typ].groupby('uhrzeit')['richtung_1'].sum()
    total_rides_per_hour_r2 = data_station[data_station['tag_typ'] == tag_typ].groupby('uhrzeit')['richtung_2'].sum()
    
    # X-Werte für die Balkendiagramme
    indices = np.arange(len(total_rides_per_hour_r1))
    
    # Erstellung der Balkendiagramme für beide Richtungen, nebeneinander
    axs[i].bar(indices - bar_width/2, total_rides_per_hour_r1, bar_width, label='Richtung 1')
    axs[i].bar(indices + bar_width/2, total_rides_per_hour_r2, bar_width, label='Richtung 2')

    # Beschriftungen und Legende hinzufügen
    axs[i].set_xlabel('Uhrzeit')
    axs[i].set_ylabel('Anzahl der Fahrten')
    axs[i].set_title(f'Fahrtenverteilung bei der Zählstation {zaehlstelle} - {tag_typ}')
    axs[i].set_xticks(indices)
    axs[i].set_xticklabels(total_rides_per_hour_r1.index)
    axs[i].legend()

plt.tight_layout()
plt.show()
