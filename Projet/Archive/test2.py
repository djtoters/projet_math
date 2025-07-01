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

# Filtrer les données pour la période du 01/03/2021 au 01/04/2021
start_date = '2021-03-01'
end_date = '2021-04-01'
mask = (df['DATE'] >= start_date) & (df['DATE'] <= end_date)
df_filtered = df.loc[mask]

# Préparation pour l'enregistrement des matrices
filename_txt = 'matriceUnMois.txt'
with open(filename_txt, 'w') as file:
    file.write("")  # Initialiser le fichier

# Liste de toutes les dates dans la plage spécifiée
all_dates = pd.date_range(start=start_date, end=end_date)

# Liste de toutes les communes
all_communes = sorted(df['TX_DESCR_FR'].unique())

# Générer et enregistrer une matrice pour chaque jour
for current_date in all_dates:
    # Initialiser la matrice pour le jour actuel
    matrix = np.zeros((len(all_communes), len(all_communes)))
    
    # Remplir la diagonale de la matrice avec les cas pour chaque commune
    for i, commune in enumerate(all_communes):
        cases = df_filtered[(df_filtered['DATE'] == current_date) & (df_filtered['TX_DESCR_FR'] == commune)]['CASES'].sum()
        matrix[i, i] = cases

    # Conversion de la matrice numpy en DataFrame pandas pour une meilleure lisibilité
    matrix_df = pd.DataFrame(matrix, index=all_communes, columns=all_communes)
    
    # Enregistrer la matrice dans le fichier .txt avec la date
    with open(filename_txt, 'a') as file:
        file.write(f"Matrice des cas pour le {current_date.strftime('%Y-%m-%d')}\n")
        matrix_df.to_string(file)
        file.write("\n\n")  # Espacer les matrices pour une meilleure lisibilité

print(f"Les matrices ont été enregistrées dans '{filename_txt}'.")

# Supposons que 'df_filtered' contient vos données filtrées comme précédemment
# Calcul des facteurs de croissance des cas pour chaque commune et chaque jour
df_filtered['CASES_PREV'] = df_filtered.groupby('TX_DESCR_FR')['CASES'].shift(1)
df_filtered['GROWTH_FACTOR'] = df_filtered['CASES'] / df_filtered['CASES_PREV']

# Initialisation de la structure pour stocker les matrices de transition
transition_matrices = []

# Parcourir chaque date pour calculer la matrice de transition quotidienne
for date in pd.date_range(start=start_date, end=end_date):
    daily_data = df_filtered[df_filtered['DATE'] == date]
    growth_matrix = np.zeros((len(all_communes), len(all_communes)))

    for i, commune in enumerate(all_communes):
        if commune in daily_data['TX_DESCR_FR'].values:
            growth_factor = daily_data[daily_data['TX_DESCR_FR'] == commune]['GROWTH_FACTOR'].values[0]
            growth_matrix[i, i] = growth_factor

    transition_matrices.append(growth_matrix)

# À ce stade, 'transition_matrices' contient vos matrices de transition quotidienne
# basées sur le facteur de croissance. Vous pouvez les enregistrer ou les utiliser
# comme bon vous semble.

# Continuation du script précédent...

# Assurez-vous d'avoir le DataFrame 'df_filtered' prêt comme indiqué précédemment

# Pour sauvegarder les matrices de transition
filename_txt = 'matrices_de_transition.txt'
with open(filename_txt, 'w') as file:
    file.write("")  # Initialiser le fichier

# Pour chaque matrice de transition
for i, matrix in enumerate(transition_matrices):
    # La date correspondante (décalage d'un jour pour correspondre aux transitions)
    date = pd.date_range(start=start_date, end=end_date)[i]
    
    # Convertir la matrice numpy en DataFrame pandas pour une meilleure lisibilité
    matrix_df = pd.DataFrame(matrix, index=all_communes, columns=all_communes)
    
    # Imprimer la matrice de transition dans le fichier et à l'écran
    with open(filename_txt, 'a') as file:
        matrix_str = f"Matrice de transition pour le {date.strftime('%Y-%m-%d')}\n{matrix_df.to_string()}\n\n"
        file.write(matrix_str)
    print(matrix_str)
