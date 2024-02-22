import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#read ./FahrradMuenchen/combined_15min.csv into data_15min
data_15min = pd.read_csv('./FahrradMuenchen/combined_15min.csv')

# Angenommen, data_15min ist Ihr DataFrame
data_15min['datum'] = pd.to_datetime(data_15min['datum'])  # Stellen Sie sicher, dass 'datum' im Datetime-Format ist
data_15min['wochentag'] = data_15min['datum'].dt.day_name()  # Fügt eine Spalte für den Wochentag hinzu
data_15min['uhrzeit'] = pd.to_datetime(data_15min['uhrzeit_start'], format='%H:%M:%S').dt.hour

# Anpassen der Plotgröße und -struktur für bessere Bildschirmanpassung
fig, axs = plt.subplots(4, 2, figsize=(15, 20), sharex=True, sharey=True)

# Entfernen des leeren Subplots (bei ungerader Anzahl von Wochentagen)
fig.delaxes(axs[3, 1])
wochentage = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for i, wochentag in enumerate(wochentage):
    # Position in der Subplot-Matrix bestimmen
    ax = axs[i // 2, i % 2]
    
    # Berechnen der Gesamtzahl der Fahrten pro Uhrzeit für den jeweiligen Wochentag
    total_rides_per_hour = data_15min[data_15min['wochentag'] == wochentag].groupby('uhrzeit')['gesamt'].sum()
    # Berechnen der Gesamtzahl aller Fahrten für den Wochentag
    total_rides = total_rides_per_hour.sum()
    # Berechnen der anteiligen Fahrten pro Uhrzeit
    proportional_rides_per_hour = (total_rides_per_hour / total_rides) * 100
    
    # Bestimmen der Farben basierend auf dem Anteil
    colors = ['grey' if percentage < 2 else 'skyblue' for percentage in proportional_rides_per_hour]
    
    ax.bar(proportional_rides_per_hour.index, proportional_rides_per_hour, color=colors)
    ax.set_title(f'Anteilige Fahrten pro Uhrzeit - {wochentag}')
    ax.set_ylabel('% der Fahrten')
    ax.grid(axis='y', linestyle='--')

# Setzen gemeinsamer X-Achsen-Labels und -Ticks
for ax in axs.flat:
    ax.set(xlabel='Uhrzeit')
    ax.set_xticks(np.arange(0, 24, 1))  # Stellen Sie sicher, dass alle Stunden angezeigt werden

plt.tight_layout()
plt.show()

# Filtern der Daten, um nur die Wochentage (Montag bis Freitag) zu behalten
werktags_daten = data_15min[data_15min['wochentag'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]

# Berechnen der Gesamtzahl der Fahrten pro Uhrzeit über die Werktage
total_rides_per_hour_weekdays = werktags_daten.groupby('uhrzeit')['gesamt'].sum()

# Berechnen der Gesamtzahl aller Fahrten an Werktagen
total_rides_weekdays = total_rides_per_hour_weekdays.sum()

# Berechnen der anteiligen Fahrten pro Uhrzeit
proportional_rides_per_hour_weekdays = (total_rides_per_hour_weekdays / total_rides_weekdays) * 100

# Werte unter 0 auf 0 begrenzen
proportional_rides_per_hour_weekdays = proportional_rides_per_hour_weekdays.clip(lower=0)

# Berechnen der Gesamtzahl der Fahrten pro Uhrzeit für das Wochenende
wochenende_daten = data_15min[data_15min['wochentag'].isin(['Saturday', 'Sunday'])]
total_rides_per_hour_weekend = wochenende_daten.groupby('uhrzeit')['gesamt'].sum()

# Berechnen der Gesamtzahl aller Fahrten am Wochenende
total_rides_weekend = total_rides_per_hour_weekend.sum()

# Berechnen der anteiligen Fahrten pro Uhrzeit für das Wochenende
proportional_rides_per_hour_weekend = (total_rides_per_hour_weekend / total_rides_weekend) * 100

# Abziehen der anteiligen Fahrten am Wochenende von den anteiligen Fahrten an Werktagen
difference_proportional_rides = proportional_rides_per_hour_weekdays / proportional_rides_per_hour_weekend * 100

# Begrenzen der resultierenden Werte auf 0 für negative Ergebnisse
difference_proportional_rides_clipped = difference_proportional_rides.clip(lower=0)

# Visualisieren der Differenz in einem Balkendiagramm
plt.figure(figsize=(12, 6))
difference_proportional_rides_clipped.plot(kind='bar', color='skyblue')
plt.title('Quotient der anteiligen Fahrten: Werktage minus Wochenende')
plt.xlabel('Uhrzeit')
plt.ylabel('Quotient der anteiligen Fahrten (%)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--')
plt.show()

