import pandas as pd
from hmmlearn import hmm
import numpy as np
import matplotlib.pyplot as plt

# Charger les données
# On travaille sur la commune de Bruxelles
# Les données sont supposées être dans la colonne 'CASES_PER_10K_MA'
df = pd.read_csv("../Filtered_Covid19_data.csv")
df["DATE"] = pd.to_datetime(df["DATE"])
df = df[df["TX_DESCR_FR"] == "Bruxelles"]  # Filtrer pour Bruxelles

data = df["CASES_PER_10K_MA"].values.reshape(-1, 1)
dates = df["DATE"].values

# Sélection optimale du nombre d'états cachés (n_components)
# On utilise le critère BIC (Bayesian Information Criterion)
bics = []
models = []
range_n = range(2, 11)
for n in range_n:
    model = hmm.GaussianHMM(n_components=n, covariance_type="diag", n_iter=1000, random_state=42)
model.fit(data)
    logL = model.score(data)
    # Calcul du nombre de paramètres :
    # n(n-1) pour la matrice de transition (hors diagonale), n pour les poids initiaux, n pour les moyennes, n pour les variances
    n_params = n * n + 2 * n  # approximation pour 1D
    bic = -2 * logL + n_params * np.log(len(data))
    bics.append(bic)
    models.append(model)

# Sélection du meilleur modèle
best_idx = np.argmin(bics)
best_n = range_n[best_idx]
best_model = models[best_idx]

print(f"Nombre optimal d'états cachés (selon BIC) : {best_n}")
print(f"BIC pour chaque n_components : {dict(zip(range_n, bics))}")

# Affichage des paramètres du meilleur modèle
print("\nMatrice de transition entre les états :")
print(best_model.transmat_)
print("\nMoyennes des distributions gaussiennes pour chaque état :")
print(best_model.means_)

# Prédiction de la séquence des états cachés
hidden_states = best_model.predict(data)

# Analyse mathématique avancée des états cachés
state_means = best_model.means_.flatten()
# Classement des états par moyenne croissante
sorted_idx = np.argsort(state_means)
state_labels = {}
phases = []
for rank, idx in enumerate(sorted_idx):
    mean = state_means[idx]
    if rank == 0:
        label = f"État {idx+1} (faible circulation)"
        phase = "faible"
    elif rank == len(sorted_idx) - 1:
        label = f"État {idx+1} (pic/haut)"
        phase = "haut"
    else:
        label = f"État {idx+1} (intermédiaire)"
        phase = "intermédiaire"
    state_labels[idx] = label
    phases.append(phase)

# Statistiques par état
print("\nAnalyse mathématique des états cachés :")
for idx in sorted_idx:
    mask = hidden_states == idx
    n_days = np.sum(mask)
    mean_val = state_means[idx]
    # Durée moyenne d'un épisode dans cet état
    # On compte les séquences consécutives
    episodes = np.split(mask, np.where(np.diff(mask) != 0)[0]+1)
    episode_lengths = [len(ep) for ep in episodes if ep[0]]
    mean_episode = np.mean(episode_lengths) if episode_lengths else 0
    # Dates de début/fin des épisodes majeurs (>10 jours)
    # Correction : on utilise des index globaux pour éviter l'IndexError
    global_idx = np.where(mask)[0]
    cursor = 0
    for i, ep in enumerate(episodes):
        if ep[0] and len(ep) > 10:
            start_idx = global_idx[cursor]
            end_idx = global_idx[cursor + len(ep) - 1]
            start = dates[start_idx]
            end = dates[end_idx]
            print(f"  - Épisode majeur du {str(start)[:10]} au {str(end)[:10]} ({len(ep)} jours)")
        if ep[0]:
            cursor += len(ep)
    print(f"{state_labels[idx]} : moyenne = {mean_val:.2f}, jours = {n_days}, durée moyenne épisode = {mean_episode:.1f} jours")

# Visualisation mathématique enrichie :
plt.figure(figsize=(15, 6))
colors = plt.cm.get_cmap('tab10', best_n)
for i in range(best_n):
    mask = hidden_states == i
    plt.plot(dates[mask], data[mask], '.', label=state_labels[i], color=colors(i))
plt.plot(dates, data, color='lightgray', alpha=0.5, label='Série originale')
plt.xlabel('Date')
plt.ylabel('Cas pour 10k habitants (MA)')
plt.title(f'HMM sur Bruxelles : {best_n} états cachés (choisis par BIC)')
plt.legend()
plt.tight_layout()
plt.show()

# Explications mathématiques :
# - On cherche à modéliser la série temporelle X_t par un processus de Markov caché Z_t (états cachés)
# - Le modèle HMM apprend la matrice de transition P(Z_{t+1}|Z_t) et les distributions d'émission P(X_t|Z_t)
# - Le critère BIC permet de choisir le nombre d'états cachés en pénalisant la complexité du modèle
# - La visualisation permet d'interpréter les régimes/stades épidémiques détectés automatiquement
# - On classe les états cachés selon leur moyenne pour interpréter les phases épidémiques.
# - On calcule la durée moyenne passée dans chaque état et les épisodes majeurs.
# - Cela permet d'identifier les périodes de faible, moyenne ou forte circulation du virus.
