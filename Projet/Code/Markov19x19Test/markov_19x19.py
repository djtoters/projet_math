import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from hmmlearn import hmm

# PROMPT utilisateur pour la période d'analyse
print("Analyse de la matrice de transition 19x19 sur une période spécifique")
print("Exemple : mai 2020, semaine 1")
start_date = input("Date de début (YYYY-MM-DD, ex: 2020-05-01) : ")
end_date = input("Date de fin (YYYY-MM-DD, ex: 2020-05-07) : ")

# 1. Chargement des données pour toutes les communes
DATA_PATH = "../../Archive/Filtered_Covid19_data.csv"
df = pd.read_csv(DATA_PATH)
df["DATE"] = pd.to_datetime(df["DATE"])

# 2. Filtrer sur la période choisie
start_dt = pd.to_datetime(start_date)
end_dt = pd.to_datetime(end_date)
df_filtered = df[(df["DATE"] >= start_dt) & (df["DATE"] <= end_dt)].copy()

print(f"Période analysée : du {start_date} au {end_date}")
print(f"Nombre de jours dans la période : {len(df_filtered['DATE'].unique())}")

# 3. Identifier les 19 communes de Bruxelles
communes = sorted(df_filtered["TX_DESCR_FR"].unique())
print(f"Nombre de communes trouvées : {len(communes)}")
print("Communes :", communes)

# 4. Détecter les phases épidémiques pour chaque commune avec HMM
def detect_phases(commune_data, n_states=3):
    """Détecte les phases épidémiques pour une commune donnée"""
    if len(commune_data) == 0:
        return []
    
    data = commune_data["CASES_PER_10K_MA"].values.reshape(-1, 1)
    model = hmm.GaussianHMM(n_components=n_states, covariance_type="diag", n_iter=1000, random_state=42)
    model.fit(data)
    phases = model.predict(data)
    return phases

# 4. Construire la matrice de transition 19x19
# On va créer une matrice basée sur les transitions de phases entre communes
transition_matrix = np.zeros((19, 19))

# Pour chaque jour, on regarde les phases de toutes les communes
dates = sorted(df_filtered["DATE"].unique())
print(f"Nombre de jours dans la période : {len(dates)}")

# On va simplifier : pour chaque jour, on classe les communes par niveau de cas
# et on compte les transitions entre "positions" dans ce classement
for i in range(len(dates) - 1):
    current_date = dates[i]
    next_date = dates[i + 1]
    
    # Récupérer les cas pour toutes les communes à ces deux dates
    current_cases = {}
    next_cases = {}
    
    for commune in communes:
        current_data = df_filtered[(df_filtered["TX_DESCR_FR"] == commune) & (df_filtered["DATE"] == current_date)]
        next_data = df_filtered[(df_filtered["TX_DESCR_FR"] == commune) & (df_filtered["DATE"] == next_date)]
        
        if not current_data.empty:
            current_cases[commune] = current_data["CASES_PER_10K_MA"].iloc[0]
        if not next_data.empty:
            next_cases[commune] = next_data["CASES_PER_10K_MA"].iloc[0]
    
    # Classer les communes par niveau de cas (position 0-18)
    if current_cases and next_cases:
        current_ranking = sorted(current_cases.items(), key=lambda x: x[1])
        next_ranking = sorted(next_cases.items(), key=lambda x: x[1])
        
        # Créer un mapping commune -> position
        current_positions = {commune: pos for pos, (commune, _) in enumerate(current_ranking)}
        next_positions = {commune: pos for pos, (commune, _) in enumerate(next_ranking)}
        
        # Compter les transitions
        for commune in communes:
            if commune in current_positions and commune in next_positions:
                from_pos = current_positions[commune]
                to_pos = next_positions[commune]
                transition_matrix[from_pos][to_pos] += 1

# 5. Normaliser la matrice pour obtenir des probabilités
row_sums = transition_matrix.sum(axis=1)
transition_matrix_normalized = np.zeros_like(transition_matrix)
for i in range(19):
    if row_sums[i] > 0:
        transition_matrix_normalized[i] = transition_matrix[i] / row_sums[i]

# 6. Affichage et analyse
print(f"\nMatrice de transition 19x19 (probabilités) - Période : {start_date} à {end_date} :")
print("Ligne = position actuelle, Colonne = position suivante")
print(transition_matrix_normalized)

# 7. Visualisation
plt.figure(figsize=(12, 10))
sns.heatmap(transition_matrix_normalized, annot=True, fmt='.2f', cmap='Blues')
plt.title(f'Matrice de transition 19x19 entre communes de Bruxelles\n(Période : {start_date} à {end_date})')
plt.xlabel('Position suivante (0 = plus faible, 18 = plus forte)')
plt.ylabel('Position actuelle (0 = plus faible, 18 = plus forte)')
plt.tight_layout()
plt.show()

# 8. Analyse mathématique
print("\nAnalyse de la matrice de transition :")
print(f"- Taille : {transition_matrix_normalized.shape}")
print(f"- Somme de chaque ligne (doit être 1 ou 0) : {transition_matrix_normalized.sum(axis=1)}")
print(f"- Éléments diagonaux (stabilité) : {np.diag(transition_matrix_normalized)}")

# 9. Commentaires mathématiques
print(f"""
Cette matrice 19x19 représente les probabilités de transition entre les positions 
des communes dans le classement par niveau de cas COVID d'un jour à l'autre.
Période analysée : {start_date} à {end_date}
- Position 0 = commune avec le plus faible nombre de cas
- Position 18 = commune avec le plus fort nombre de cas
- Chaque ligne somme à 1 (probabilités de transition)
- Les éléments diagonaux indiquent la stabilité des positions
""") 