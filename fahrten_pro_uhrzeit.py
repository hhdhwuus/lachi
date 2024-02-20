import pandas as pd
import matplotlib.pyplot as plt

# Laden der Daten
file_path = 'combined_15min.csv'  # Aktualisieren Sie dies mit Ihrem tatsächlichen Dateipfad
data = pd.read_csv(file_path)

# Extrahieren der Stunde aus der Uhrzeit
data['uhrzeit'] = pd.to_datetime(data['uhrzeit_start'], format='%H:%M:%S').dt.hour

# Berechnen der Gesamtzahl der Fahrten pro Uhrzeit
total_rides_per_hour = data.groupby('uhrzeit')['gesamt'].sum()

# Berechnen der Gesamtzahl aller Fahrten
total_rides = total_rides_per_hour.sum()

# Berechnen der anteiligen Fahrten pro Uhrzeit
proportional_rides_per_hour = (total_rides_per_hour / total_rides) * 100


# Plot mit angepassten Farben für Anteile unter 2%
colors = ['grey' if percentage < 2 else 'skyblue' for percentage in proportional_rides_per_hour]

plt.figure(figsize=(12, 6))
proportional_rides_per_hour.plot(kind='bar', color=colors)
plt.title('Anteilige Fahrten pro Uhrzeit mit unter 2% Anteil ausgegraut')
plt.xlabel('Uhrzeit')
plt.ylabel('Anteil der Fahrten (%)')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--')
plt.show()

# Filtern der Daten für weitere Betrachtungen
# Entfernen von Uhrzeiten mit weniger als 2% Anteil
filtered_data = data[data['uhrzeit'].isin(proportional_rides_per_hour[proportional_rides_per_hour >= 2].index)]