import pandas as pd
import numpy as np
import json

# Chargement des données
filename = 'Updated_Covid19_Data.json'
with open(filename, 'r') as file:
    data = json.load(file)

# Conversion en DataFrame
df = pd.DataFrame(data)

# Conversion des types de données
df['DATE'] = pd.to_datetime(df['DATE'])
df['CASES'] = pd.to_numeric(df['CASES'])

# Calcul de l'augmentation quotidienne des cas pour chaque commune
df.sort_values(by=['TX_DESCR_FR', 'DATE'], inplace=True)
df['DAILY_CASES'] = df.groupby('TX_DESCR_FR')['CASES'].diff().fillna(0)

# Sélection d'un jour spécifique pour la visualisation, par exemple "2020-09-28"
specific_date = '2020-09-28'
daily_cases = df[df['DATE'] == pd.to_datetime(specific_date)][['TX_DESCR_FR', 'DAILY_CASES']]

# Assurer que toutes les communes sont présentes, même celles sans cas ce jour-là
all_communes = sorted(df['TX_DESCR_FR'].unique())
matrix = np.zeros((len(all_communes), len(all_communes)))

for i, commune in enumerate(all_communes):
    if commune in daily_cases['TX_DESCR_FR'].values:
        cases = daily_cases[daily_cases['TX_DESCR_FR'] == commune]['DAILY_CASES'].values[0]
        matrix[i, i] = cases

# Affichage de la matrice
print(matrix)

# Optionnel : convertir la matrice numpy en DataFrame pandas pour une meilleure lisibilité
matrix_df = pd.DataFrame(matrix, index=all_communes, columns=all_communes)
print(matrix_df)
