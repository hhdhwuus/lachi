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

# Erstellen eines Balkendiagramms für die anteiligen Fahrten pro Uhrzeit
plt.figure(figsize=(12, 6))
proportional_rides_per_hour.plot(kind='bar', color='skyblue')
plt.title('Anteilige Fahrten pro Uhrzeit')
plt.xlabel('Uhrzeit')
plt.ylabel('Anteil der Fahrten (%)')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--')
plt.show()
