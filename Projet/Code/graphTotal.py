import pandas as pd
import matplotlib.pyplot as plt
import json

# Chemin vers votre fichier JSON
filename = 'Updated_Covid19_Data.json'

# Charger les données depuis le fichier JSON
with open(filename, 'r') as file:
    data = json.load(file)

# Convertir les données en DataFrame pandas
df = pd.DataFrame(data)

# Convertir les cases en nombres entiers et les dates en type date
df['CASES'] = pd.to_numeric(df['CASES'])
df['DATE'] = pd.to_datetime(df['DATE'])

# Grouper les données par date et calculer le nombre total de cas pour chaque jour
total_cases_per_day = df.groupby('DATE')['CASES'].sum().reset_index()

# Créer un nuage de points du nombre total de cas pour chaque jour
plt.figure(figsize=(20, 12))
plt.scatter(total_cases_per_day['DATE'], total_cases_per_day['CASES'], color='blue')
plt.title('Nombre total de cas de COVID-19 par jour')
plt.xlabel('Date')
plt.ylabel('Nombre total de cas')
plt.xticks(rotation=45)
plt.tight_layout()

# Afficher le graphique
plt.show()
