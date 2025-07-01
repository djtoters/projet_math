import pandas as pd
from hmmlearn import hmm
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

# Charger les données
df = pd.read_csv("../Filtered_Covid19_data.csv")  # Assurez-vous que le chemin d'accès est correct
df["DATE"] = pd.to_datetime(df["DATE"])
df_bruxelles = df[df["TX_DESCR_FR"] == "Bruxelles"]  # Filtrer pour Bruxelles

# Préparer les données
X = df_bruxelles['CASES_PER_10K_MA'].values.reshape(-1, 1)

# Diviser les données en 70% train et 30% test
X_train, X_test, dates_train, dates_test = train_test_split(X, df_bruxelles['DATE'], test_size=0.3, random_state=425, shuffle=False)

# Configuration du modèle HMM
model = hmm.GaussianHMM(n_components=7, covariance_type="full", n_iter=10000, random_state=425)

# Entraînement du modèle
model.fit(X_train)

# Prédiction des états cachés pour l'ensemble de test
hidden_states_test = model.predict(X_test)

# Affichage des états prédits
print("États cachés prédits pour les données de test :")
print(hidden_states_test)

# Visualisation des états au fil du temps
plt.figure(figsize=(15, 5))
plt.plot(dates_test.reset_index(drop=True), hidden_states_test, drawstyle="steps-post")
plt.title('États cachés prédits sur les données de test')
plt.xlabel('Date')
plt.ylabel('État caché')
plt.show()

# Examiner la matrice de transition
print("Matrice de transition entre les états :")
print(model.transmat_)

# Examiner les moyennes des états
print("Moyennes des états :")
print(model.means_)
