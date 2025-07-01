from hmmlearn import hmm
import numpy as np
import json

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
data_by_commune = {commune: [] for commune in communes}
for entry in data:
    commune_name = entry["TX_DESCR_FR"]
    cases = int(entry["CASES"])
    data_by_commune[commune_name].append(cases)

# Diviser en ensembles d'entraînement et de test pour chaque commune
data_by_commune_train = {}
data_by_commune_test = {}

for commune, cases in data_by_commune.items():
    index_cutoff = int(len(cases) * 2 / 3)  # Calcul de l'index de coupure pour chaque commune
    data_by_commune_train[commune] = cases[:index_cutoff]
    data_by_commune_test[commune] = cases[index_cutoff:]

# Conversion des séquences d'entraînement en format approprié pour hmmlearn
sequences_train = {
    commune: np.array(cases).reshape(-1, 1)
    for commune, cases in data_by_commune_train.items()
}

# Entraînement des modèles HMM sur l'ensemble d'entraînement
hmm_models = {}
for commune, X_train in sequences_train.items():
    model = hmm.GaussianHMM(
        n_components=3, covariance_type="diag", n_iter=100, random_state=42
    )
    model.fit(X_train)
    hmm_models[commune] = model
    print(f"Modèle HMM entraîné pour {commune} avec {len(X_train)} données.")

# Afficher les matrices de transition pour chaque modèle entraîné
for commune, model in hmm_models.items():
    print(f"Matrice de transition pour {commune}:")
    print(model.transmat_)

# Pour tester les modèles sur l'ensemble de test, vous pourriez calculer la log-vraisemblance des données de test ou analyser les séquences d'états prédites par rapport aux données observées, en gardant à l'esprit les limitations mentionnées précédemment.

log_likelihood_test = {}

for commune, X_test in data_by_commune_test.items():
    model = hmm_models[commune]  # Récupérer le modèle HMM entraîné pour cette commune
    X_test_array = np.array(X_test).reshape(-1, 1)  # Convertir les données de test en format approprié
    log_likelihood_test[commune] = model.score(X_test_array)  # Calculer la log-vraisemblance

    print(f"Log-vraisemblance pour {commune}: {log_likelihood_test[commune]}")

predicted_states_test = {}

for commune, X_test in data_by_commune_test.items():
    model = hmm_models[commune]  # Récupérer le modèle HMM entraîné pour cette commune
    X_test_array = np.array(X_test).reshape(-1, 1)  # Convertir les données de test en format approprié
    predicted_states_test[commune] = model.predict(X_test_array)  # Prédire la séquence d'états cachés

    print(f"États prédits pour {commune}: {predicted_states_test[commune]}")
