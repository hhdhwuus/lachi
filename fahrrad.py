import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Korrekter Pfad unter Verwendung eines rohen Strings, um Escape-Probleme zu vermeiden
file_path = r'C:\Users\Wessner\Desktop\Python 2nd sem\progs\data_2008_daily_corrected.csv'

# Korrektes Laden der CSV-Datei ohne das Schlüsselwort 'file_path='
data_2008_daily_corrected = pd.read_csv(file_path, sep=',', quotechar='"')

file_path = r'C:\Users\Wessner\Desktop\Python 2nd sem\progs\monthly_avg_2008.csv'

monthly_avg = pd.read_csv(file_path, sep=',', quotechar='"')

file_path = r'C:\Users\Wessner\Desktop\Python 2nd sem\progs\weekday_weekend_avg_2008.csv'

weekday_weekend_avg = pd.read_csv(file_path, sep=',', quotechar='"')

# Setzen des Seaborn-Stils für die Plots
sns.set_theme(style="whitegrid")

# Temperatur vs. Gesamtanzahl der Fahrradfahrer
plt.figure(figsize=(12, 6))
sns.regplot(x='max.temp', y='gesamt', data=data_2008_daily_corrected, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('Maximale Temperatur vs. Gesamtanzahl der Fahrradfahrer')
plt.xlabel('Maximale Temperatur (°C)')
plt.ylabel('Gesamtanzahl der Fahrradfahrer')
plt.show()

# Niederschlag vs. Gesamtanzahl der Fahrradfahrer
plt.figure(figsize=(12, 6))
sns.regplot(x='niederschlag', y='gesamt', data=data_2008_daily_corrected, scatter_kws={'alpha':0.5}, line_kws={'color':'blue'})
plt.title('Niederschlag vs. Gesamtanzahl der Fahrradfahrer')
plt.xlabel('Niederschlag (mm)')
plt.ylabel('Gesamtanzahl der Fahrradfahrer')
plt.show()

# Saisonale Trends - Durchschnittliche Anzahl der Fahrradfahrer pro Monat
plt.figure(figsize=(12, 6))
sns.barplot(x='monat', y='gesamt', data=monthly_avg)
plt.title('Durchschnittliche Anzahl der Fahrradfahrer pro Monat')
plt.xlabel('Monat')
plt.ylabel('Durchschnittliche Anzahl der Fahrradfahrer')
plt.show()

# Unterschiede zwischen Werktagen und Wochenenden
plt.figure(figsize=(12, 6))
sns.barplot(x='tag_typ', y='gesamt', data=weekday_weekend_avg)
plt.title('Durchschnittliche Anzahl der Fahrradfahrer: Werktag vs. Wochenende')
plt.xlabel('Tag Typ')
plt.ylabel('Durchschnittliche Anzahl der Fahrradfahrer')
plt.show()

test