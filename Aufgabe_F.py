import numpy as np


# quelle https://stadt.muenchen.de/dam/jcr:3aebd2f1-e895-4b49-9ec1-ada18e4e4246/230703_Uebersicht_NO2_Messstellen_LHM_LfU_2023_KW_1-22.pdf
data = [
    ["MP 1", "Verdistraße 73", "M-BBM", 39, 35, 32, 27, 27],
    ["MP 2", "Planegger Straße 25", "M-BBM", 38, 34, 29, 25, 26],
    ["MP 3", "Eversbuschstraße 171", "M-BBM", 36, 34, 30, 25, 25],
    ["MP 4", "Feldmochinger Straße 25 a", "M-BBM", 28, 26, 24, 20, 21],
    ["MP 5", "Schleißheimer Straße 273", "M-BBM", 35, 33, 29, 26, 25],
    ["MP 6", "Rheinstraße 26", "M-BBM", 28, 27, 24, 20, 20],
    ["MP 7", "Tegernseer Landstraße 150", "M-BBM", 57, 55, 48, 43, 43],
    ["MP 8", "Chiemgaustraße 140", "M-BBM", 58, 53, 46, 39, 39],
    ["MP 9", "Kreillerstraße 111", "M-BBM", 32, 30, 26, 23, 23],
    ["MP 10", "Bajuwarenstraße 92", "M-BBM", 29, 27, 24, 20, 21],
    ["MP 11", "Fürstenrieder Straße 285", "M-BBM", 36, 32, 25, 21, 20],
    ["MP 12", "Liesl-Karlstadt-Straße 7/9", "M-BBM", 37, 34, 29, 25, 25],
    ["MP 13", "Hofbrunnstraße 68", "M-BBM", 19, 18, 16, 14, 14],
    ["MP 14", "Frauenstraße 16/18", "M-BBM", 49, 46, 35, 30, 31],
    ["MP 15", "Wotanstraße 103a/105", "M-BBM", 39, 35, 31, 27, 27],
    ["MP 16", "Steinsdorfer Straße 15", "M-BBM", 44, 41, 0, 0, 0],
    ["MP 17", "LÜB München-Lothstraße", "M-BBM", 27, 29, 24, 21, 20],
    ["MP 18", "Situlistraße 21", "M-BBM", 38, 36, 30, 27, 27],
    ["MP 19", "Ruth-Schaumann-Straße 8/10", "M-BBM", 22, 21, 20, 18, 18],
    ["MP 20", "Boschetsrieder Straße 83/83a", "M-BBM", 27, 24, 21, 19, 19],
    ["MP 21", "Offenbachstraße 48", "M-BBM", 29, 27, 24, 20, 20],
    ["MP 22", "Altostraße 24", "M-BBM", 0, 27, 24, 19, 18],
    ["MP 23", "Dachauer Straße 264", "M-BBM", 0, 31, 27, 22, 22],
    ["MP 24", "Lerchenauer Straße 207", "M-BBM", 0, 34, 29, 23, 22],
    ["MP 25", "Dülferstraße 28", "M-BBM", 0, 26, 24, 19, 19],
    ["MP 26", "Oberföhringer Straße 236", "M-BBM", 0, 29, 24, 19, 18],
    ["MP 27", "Tegernseer Landstraße 19", "DWD", 0, 46, 38, 28, 27],
    ["MP 28", "Hansastraße 99", "DWD", 0,34, 29, 23, 23],
    ["MP 29", "Paul-Heyse-Str. 8", "DWD", "k.A.", 56, 43, "k.A.", "k.A."],
    ["MP 30", "Sauerbruchstraße 52", "M-BBM", "k.A.", 25, 22, 17, 17],
    ["MP 31", "Belgradstraße 10", "M-BBM", "k.A.", 31, 26, 23, 21],
    ["MP 32", "Mühlbaurstraße 31", "M-BBM", "k.A.", 26, 23, 20, 18],
    ["MP 33", "Welfenstraße 38", "M-BBM", "k.A.", 33, 29, 23, 22],
    ["MP 34", "Bad-Schachener-Straße 69", "M-BBM", "k.A.", 34, 28, 25, 24],
    ["MP 35", "Putzbrunner Straße 5", "M-BBM", "k.A.", 35, 28, 23, 22],
    ["MP 36", "Humboldstr. 13", "DWD", "k.A.", 49, 38, 33, 31],
    ["MP 37", "Ridlerstraße 30", "M-BBM", "k.A.", 35, 29, 26, 25],
    ["MP 38", "Plinganser Str. 18", "DWD", "k.A.", 40, 33, "k.A.", 28],
    ["MP 39", "Elsenheimer Straße 53", "M-BBM", "k.A.", 31, 26, 23, 23],
    ["MP 40", "Gabelsbergerstraße 81", "M-BBM", "k.A.", 33, 27, 24, 23],
    ["MP 41", "Fraunhoferstr. 32", "DWD", "k.A.", 45, 37, 32, 31],
    ["MP 42", "LÜB-Station Stachus", "M-BBM", "k.A.", 46, 36, 31, 31],
    ["MP 43", "Prinzregentenstr. 74", "DWD", "k.A.", 48, 39, 33, 32],
    ["MP 44", "Prinzregentenstr. 115", "DWD", "k.A.", 45, 35, 31, 31],
    ["MP 45", "Leuchtenbergring (Streitfeldstr. 6)", "M-BBM-neu ab 2023", "k.A.", "k.A.", "k.A.", "k.A.", "k.A."],
    ["MP 46", "Fürstenrieder Straße 20", "M-BBM-neu ab 2023", "k.A.", "k.A.", "k.A.", "k.A.", "k.A."],
    ["MP 47", "Hofangerstraße 71", "M-BBM-neu ab 2023", "k.A.", "k.A.", "k.A.", "k.A.", "k.A."],
    ["MP 48", "Naupliastraße 20", "M-BBM-neu ab 2023", "k.A.", "k.A.", "k.A.", "k.A.", "k.A."],
    ["MP 49", "Cosimastraße 106", "M-BBM-neu ab 2023", "k.A.", "k.A.", "k.A.", "k.A.", "k.A."],
    ["MP 50", "Wintrichring 46", "M-BBM-neu ab 2023", "k.A.", "k.A.", "k.A.", "k.A.", "k.A."],
    ["MP 51", "Moosacher Straße 10", "M-BBM-neu ab 2023", "k.A.", "k.A.", "k.A.", "k.A.", "k.A."],
    ["LFU 101", "Landshuter Allee 99/101", "", "k.A.", 63, 49, 45, 44],
    ["LFU 102", "Trappentreustraße 4", "", "k.A.", 60, 45, 41, 41],
    ["LFU 103", "Schäftlarnstraße 104/106", "", "k.A.", 28, 23, 23, 21],
    ["LÜB 1", "Landshuter Allee 66", "", 63, 54, 51, 49, 45],
    ["LÜB 2", "Stachus (Karlsplatz)", "", 48, 42, 33, 30, 31],
    ["LÜB 3", "Lothstraße", "", 27, 27, 23, 21, 20],
    ["LÜB 4", "Allach", "", 24, 21, 19, 18, 17],
    ["LÜB 5", "Johanneskirchen", "", 20, 19, 17, 15, 14]
]


values_adjusted = np.array([[np.nan if value == 'k.A.' or value == 0 else float(value) for value in row[3:]] for row in data])

# Berechnung des Mittelwerts für jedes Jahr, Ausschluss von 'k.A.' durch np.nanmean
yearly_averages_adjusted = np.nanmean(values_adjusted, axis=0)

print(yearly_averages_adjusted)