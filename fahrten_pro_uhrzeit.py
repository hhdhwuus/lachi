import pandas as pd
import matplotlib.pyplot as plt

# Stellen Sie sicher, dass Sie Ihren tatsächlichen Dateipfad hier aktualisieren
file_path = 'FahrradMuenchen/combined_15min.csv'
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
bars = plt.bar(proportional_rides_per_hour.index, proportional_rides_per_hour.values, color='skyblue')

# Balken unter 2 Prozent in Rot markieren
for bar, value in zip(bars, proportional_rides_per_hour.values):
    if value < 2:
        bar.set_color('#ff6b6b')

plt.title('Anteilige Fahrten pro Uhrzeit')
plt.xlabel('Uhrzeit')
plt.ylabel('Anteil der Fahrten (%)')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--')
plt.show()
