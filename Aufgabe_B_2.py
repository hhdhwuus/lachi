import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv('./ProcessedData/combined_tage.csv')	
# Umwandlung des 'datum' in ein datetime-Objekt für leichtere Manipulation
data['datum'] = pd.to_datetime(data['datum'])

# Kreuther Zählstelle entfernen aufgrund von Umbau 2020. Dadurch wurden die Daten verfälscht
data = data[data['zaehlstelle'] != 'Kreuther']

# Gruppierung der Daten nach Datum und Zählstelle, Berechnung des Durchschnitts
daily_avg = data.groupby(['datum', 'zaehlstelle']).agg({'gesamt':'mean'}).reset_index()

# Berechnung des täglichen Durchschnitts über alle Zählstellen
overall_daily_avg = daily_avg.groupby('datum').agg({'gesamt':'mean'}).reset_index()

# Extraktion des Jahres aus dem Datum für die Jahresdurchschnittsberechnung
daily_avg['jahr'] = daily_avg['datum'].dt.year
overall_daily_avg['jahr'] = overall_daily_avg['datum'].dt.year

# Berechnung des Jahresdurchschnitts für jede Zählstelle und insgesamt
annual_avg_per_count = daily_avg.groupby(['jahr', 'zaehlstelle']).agg({'gesamt':'mean'}).reset_index()
overall_annual_avg = overall_daily_avg.groupby('jahr').agg({'gesamt':'mean'}).reset_index()

# Erstellung der Grafik
plt.figure(figsize=(15, 8))

# Jahresdurchschnitte der einzelnen Zählstellen in weniger gesättigten Farben
for zaehlstelle in annual_avg_per_count['zaehlstelle'].unique():
    zaehlstelle_data = annual_avg_per_count[annual_avg_per_count['zaehlstelle'] == zaehlstelle]
    plt.plot(zaehlstelle_data['jahr'], zaehlstelle_data['gesamt'], label=zaehlstelle, alpha=0.5)

# Jahresdurchschnitt über alle Zählstellen in gesättigter Farbe
plt.plot(overall_annual_avg['jahr'], overall_annual_avg['gesamt'], label='Gesamtdurchschnitt', color='black', linewidth=2)

plt.title('Jahresdurchschnitt der Fahrradfahrer an verschiedenen Zählstellen')
plt.xlabel('Jahr')
plt.ylabel('Durchschnittliche Anzahl der Fahrradfahrer')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)
plt.suptitle('Frage 2: Gibt es Langfristige Trends im Fahrradverkehr?', fontsize=16)

plt.tight_layout()
plt.show()
