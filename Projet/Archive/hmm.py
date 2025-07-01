import json
import numpy as np
from hmmlearn import hmm

# Charger les données du fichier JSON
with open("Updated_Covid19_Data.json", "r") as file:
    data = json.load(file)

# Liste des communes
communes = [
    "Anderlecht",
    "Auderghem",
    "Berchem-Sainte-Agathe",
    "Bruxelles",
    "Etterbeek",
    "Evere",
    "Forest (Bruxelles-Capitale)",
    "Ganshoren",
    "Ixelles",
    "Jette",
    "Koekelberg",
    "Molenbeek-Saint-Jean",
    "Saint-Gilles",
    "Saint-Josse-ten-Noode",
    "Schaerbeek",
    "Uccle",
    "Watermael-Boitsfort",
    "Woluwe-Saint-Lambert",
    "Woluwe-Saint-Pierre",
]

# Organiser les données par commune
# On définie une liste des communes de Bx pour lesquelles les données
# sont analysées.
data_by_commune = {commune: [] for commune in communes}
for entry in data:
    commune_name = entry["TX_DESCR_FR"]
    cases = int(entry["CASES"])
    data_by_commune[commune_name].append(cases)

# Conversion des séquences en format approprié pour hmmlearn
sequences = {
    commune: np.array(cases).reshape(-1, 1)
    for commune, cases in data_by_commune.items()
}
lengths = {commune: len(cases) for commune, cases in data_by_commune.items()}

# Initialisation d'un dictionnaire pour stocker les modèles HMM entraînés pour chaque commune
hmm_models = {}

for commune, X in sequences.items():
    # Créer un modèle HMM Gaussian pour cette commune
    # Pour chaque commune on crée un modèle HMM Gaussian avec 3 états
    # cachés, une matrice de covariance diagonale et un nombre maximal
    # d'itérations pour l'algorithme EM. Le modèle est ensuite
    # entrainé ('fit') sur les séquences des cas covid 19. Le modèles
    # entrainé est stocké dans 'hmm_models'
    model = hmm.GaussianHMM(
        n_components=3, covariance_type="diag", n_iter=100, random_state=42
    )

    model.fit(X)

    # Stocker le modèle entraîné
    hmm_models[commune] = model

    print(f"Modèle HMM entraîné pour {commune} avec {len(X)} données.")

for commune, model in hmm_models.items():
    print(f"Matrice de transition pour {commune}:")
    print(model.transmat_)

    # Ce code devrait vous permettre d'obtenir un aperçu des dynamiques de propagation du COVID-19 dans chaque commune en examinant les matrices de transition estimées. C'est une étape clé pour comprendre comment le virus se propage dans différentes zones géographiques et pourrait informer des mesures de prévention et de contrôle.

# Pour tester les modèles sur l'ensemble de test, vous pourriez calculer la log-vraisemblance des données de test ou analyser les séquences d'états prédites par rapport aux données observées, en gardant à l'esprit les limitations mentionnées précédemment.

log_likelihood_test = {}

for commune, X_test in data_by_commune.items():
    model = hmm_models[commune]  # Récupérer le modèle HMM entraîné pour cette commune
    X_test_array = np.array(X_test).reshape(
        -1, 1
    )  # Convertir les données de test en format approprié
    log_likelihood_test[commune] = model.score(
        X_test_array
    )  # Calculer la log-vraisemblance

    print(f"Log-vraisemblance pour {commune}: {log_likelihood_test[commune]}")

predicted_states_test = {}

for commune, X_test in data_by_commune.items():
    model = hmm_models[commune]  # Récupérer le modèle HMM entraîné pour cette commune
    X_test_array = np.array(X_test).reshape(
        -1, 1
    )  # Convertir les données de test en format approprié
    predicted_states_test[commune] = model.predict(
        X_test_array
    )  # Prédire la séquence d'états cachés

    print(f"États prédits pour {commune}: {predicted_states_test[commune]}")
