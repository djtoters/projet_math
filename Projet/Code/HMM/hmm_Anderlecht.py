import pandas as pd
from hmmlearn import hmm
import numpy as np

# Charger les données
df = pd.read_csv("../Filtered_Covid19_data.csv")
df["DATE"] = pd.to_datetime(df["DATE"])
df = df[df["TX_DESCR_FR"] == "Anderlecht"]  # Filtrer pour Anderlecht

# Préparation des données
# Nous supposons que 'CASES_PER_10K_MA' est la colonne d'intérêt
data = df["CASES_PER_10K_MA"].values.reshape(-1, 1)

# Configuration du HMM
# Utilisation d'un modèle Gaussian HMM avec 7 états cachés
model = hmm.GaussianHMM(
    n_components=7, covariance_type="diag", n_iter=10000, random_state=42
)

# Entraînement du modèle
model.fit(data)

# Examiner les paramètres appris
print("Matrices de transition entre les états :")
print(model.transmat_)
print("\nMoyennes des distributions gaussiennes pour chaque état :")
print(model.means_)

# Utiliser le modèle pour prédire la séquence des états
hidden_states = model.predict(data)

# Afficher les états cachés pour quelques observations
print("\nÉtats cachés prédits pour les données :")
print(hidden_states[:200])  # Afficher les premiers 200 états prédits
