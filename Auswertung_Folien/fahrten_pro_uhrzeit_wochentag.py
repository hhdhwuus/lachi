import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#read ./FahrradMuenchen/combined_15min.csv into data_15min
data_15min = pd.read_csv('./ProcessedData/combined_15min.csv')

# Definition von Werktagen und Wochenenden
data_15min['tag_typ'] = np.where(data_15min['wochentag'].isin(['Saturday', 'Sunday']), 'Wochenende', 'Werktag')

# Gruppierung der Daten nach Zählstation, Tagtyp, Uhrzeit und Berechnung der Summen für richtung_1 und richtung_2
grouped_data = data_15min.groupby(['zaehlstelle', 'tag_typ', 'uhrzeit']).agg({
    'richtung_1': 'sum',
    'richtung_2': 'sum'
}).reset_index()

# Einzigartige Zählstationen für die Plot-Erstellung
zaehlstellen = grouped_data['zaehlstelle'].unique()

# Plot-Erstellung
rows = len(zaehlstellen)  # Anzahl der Zeilen basierend auf der Anzahl der Zählstationen
fig, axs = plt.subplots(rows, 2, figsize=(15, 5*rows), sharex=True, sharey=True)  # 2 Spalten für Werktag und Wochenende

# Sicherstellen, dass axs immer ein zweidimensionales Array ist für den Fall, dass nur eine Zählstation vorhanden ist
if rows == 1:
    axs = axs.reshape(1, -1)

for i, zaehlstelle in enumerate(zaehlstellen):
    for j, tag_typ in enumerate(['Werktag', 'Wochenende']):
        # Filtern der Daten für die aktuelle Zählstation und Tagtyp
        zaehlstelle_data = grouped_data[(grouped_data['zaehlstelle'] == zaehlstelle) & (grouped_data['tag_typ'] == tag_typ)]
        
        # Daten für Richtung 1 und 2
        richtung_1_data = zaehlstelle_data['richtung_1']
        richtung_2_data = zaehlstelle_data['richtung_2']
        
        # Bar-Plots für beide Richtungen
        width = 0.35  # Balkenbreite
        axs[i, j].bar(zaehlstelle_data['uhrzeit'] - width/2, richtung_1_data, width, label='Richtung 1', color='skyblue')
        axs[i, j].bar(zaehlstelle_data['uhrzeit'] + width/2, richtung_2_data, width, label='Richtung 2', color='orange')
        
        # Titel und Legende
        axs[i, j].set_title(f'{zaehlstelle} - {tag_typ}')
        axs[i, j].legend()

# Gemeinsame Achsenbeschriftungen und Anpassungen
for ax in axs.flat:
    ax.set(xlabel='Uhrzeit', ylabel='Anzahl der Fahrten')
    ax.set_xticks(np.arange(0, 24, 1))  # Stellen Sie sicher, dass alle Stunden angezeigt werden
    ax.grid(axis='y', linestyle='--')

plt.tight_layout()
plt.show()



