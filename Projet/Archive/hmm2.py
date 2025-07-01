import json
import numpy as np


# Fonction pour charger les données depuis un fichier JSON
def load_data_from_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


# Chemin vers votre fichier JSON
filename = "Updated_Covid19_Data.json"
data = load_data_from_json(filename)

# Convertir les données en une structure plus manipulable
cases = {}
for entry in data:
    commune = entry["TX_DESCR_FR"]
    date = entry["DATE"]
    nombre_de_cas = int(entry["CASES"])

    if commune not in cases:
        cases[commune] = {}
    cases[commune][date] = nombre_de_cas

# Calculer la matrice de transition basée sur l'augmentation des cas
dates = sorted(list({entry["DATE"] for entry in data}))
communes = sorted(cases.keys())

transition_matrix = np.zeros((len(communes), len(communes)))

for i, commune in enumerate(communes):
    for j, next_commune in enumerate(communes):
        if commune == next_commune:
            continue  # Ignorer les transitions internes

        somme_transitions = 0
        for k in range(len(dates) - 1):
            cas_aujourdhui = cases[commune].get(dates[k], 0)
            cas_demain = cases[next_commune].get(dates[k + 1], 0)

            # Calcul simple du changement relatif d'un jour à l'autre entre communes
            if cas_aujourdhui > 0 and cas_demain > 0:
                somme_transitions += (cas_demain - cas_aujourdhui) / cas_aujourdhui

        # Moyenne de transition entre communes
        transition_matrix[i, j] = (
            somme_transitions / (len(dates) - 1) if somme_transitions > 0 else 0
        )

# Affichage de la matrice de transition
print("Matrice de transition (simplifiée) entre les communes :")
for i, commune in enumerate(communes):
    for j, next_commune in enumerate(communes):
        print(f"De {commune} à {next_commune}: {transition_matrix[i, j]:.4f}")

"""
Cette approche simplifiée calcule une sorte de "taux de transmission" basé sur l'augmentation 
relative des cas entre chaque paire de communes d'un jour à l'autre, plutôt qu'une vraie modélisation
de transitions d'états cachés comme dans un HMM classique. Il est crucial de reconnaître que cette méthode 
ne reflète pas l'utilisation standard des HMM pour la modélisation de données temporelles et ne capture pas
directement les dynamiques de transmission de maladie ou les variables cachées sous-jacentes. Pour une analyse
épidémiologique précise, l'approche devrait être considérablement raffinée et basée sur des modèles épidémiologiques
validés.
"""
