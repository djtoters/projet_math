import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

# 1. Chargement des données de Bruxelles
# On suppose que le fichier est au même endroit que pour le HMM
DATA_PATH = "../../Archive/Filtered_Covid19_data.csv"
df = pd.read_csv(DATA_PATH)
df["DATE"] = pd.to_datetime(df["DATE"])
df = df[df["TX_DESCR_FR"] == "Bruxelles"]
data = df["CASES_PER_10K_MA"].values.reshape(-1, 1)
dates = df["DATE"].values

# 2. Sélection du nombre optimal de composantes (phases) par BIC
bics = []
gmms = []
range_n = range(2, 11)
for n in range_n:
    gmm = GaussianMixture(n_components=n, covariance_type='full', n_init=10, random_state=42)
    gmm.fit(data)
    bic = gmm.bic(data)
    bics.append(bic)
    gmms.append(gmm)
best_idx = np.argmin(bics)
best_n = range_n[best_idx]
best_gmm = gmms[best_idx]

print(f"Nombre optimal de phases (composantes) selon BIC : {best_n}")
print(f"BIC pour chaque n_components : {dict(zip(range_n, bics))}")

# 3. Prédiction des phases pour chaque observation
phases = best_gmm.predict(data)
means = best_gmm.means_.flatten()
sorted_idx = np.argsort(means)

# 4. Affichage mathématique et interprétation
print("\nParamètres des phases (moyennes des gaussiennes) :")
for rank, idx in enumerate(sorted_idx):
    print(f"Phase {rank+1} : moyenne = {means[idx]:.2f}, poids = {best_gmm.weights_[idx]:.2f}")

# 5. Visualisation
plt.figure(figsize=(15, 6))
colors = plt.cm.get_cmap('tab10', best_n)
for i, idx in enumerate(sorted_idx):
    mask = phases == idx
    plt.plot(dates[mask], data[mask], '.', label=f"Phase {i+1}", color=colors(i))
plt.plot(dates, data, color='lightgray', alpha=0.5, label='Série originale')
plt.xlabel('Date')
plt.ylabel('Cas pour 10k habitants (MA)')
plt.title(f'GMM (EM) sur Bruxelles : {best_n} phases (choisies par BIC)')
plt.legend()
plt.tight_layout()
plt.show()

# 6. Explication mathématique du rôle de l'EM
print("""
L'algorithme EM (Expectation-Maximization) est utilisé ici pour ajuster les paramètres du modèle de mélange gaussien (GMM).
- E-step : pour chaque point, calculer la probabilité d'appartenance à chaque phase (composante gaussienne)
- M-step : mettre à jour les paramètres (moyennes, covariances, poids) pour maximiser la vraisemblance totale
Le processus alterne E et M jusqu'à convergence.
Dans ce contexte, chaque phase détectée correspond à un régime épidémique caractérisé par une moyenne différente de cas.
""") 