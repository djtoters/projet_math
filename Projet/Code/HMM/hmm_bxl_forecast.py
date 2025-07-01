import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn import hmm

# PROMPT utilisateur
train_months = int(input("Combien de mois pour l'entraînement du modèle ? "))
test_months = int(input("Combien de mois pour la prédiction (test) ? "))

# 1. Chargement des données de Bruxelles
DATA_PATH = "../Filtered_Covid19_data.csv"
df = pd.read_csv(DATA_PATH)
df["DATE"] = pd.to_datetime(df["DATE"])
df = df[df["TX_DESCR_FR"] == "Bruxelles"]
data = df["CASES_PER_10K_MA"].values.reshape(-1, 1)
dates = df["DATE"].values

# 2. Découpage dynamique selon le choix utilisateur
train_end = df["DATE"].min() + pd.DateOffset(months=train_months)
test_end = train_end + pd.DateOffset(months=test_months)
train_mask = (df["DATE"] < train_end)
test_mask = (df["DATE"] >= train_end) & (df["DATE"] < test_end)

train_data = data[train_mask]
train_dates = dates[train_mask]
test_data = data[test_mask]
test_dates = dates[test_mask]

# 3. Sélection du nombre optimal d'états cachés (BIC)
bics = []
models = []
range_n = range(2, 8)
for n in range_n:
    model = hmm.GaussianHMM(n_components=n, covariance_type="diag", n_iter=1000, random_state=42)
    model.fit(train_data)
    logL = model.score(train_data)
    n_params = n * n + 2 * n
    bic = -2 * logL + n_params * np.log(len(train_data))
    bics.append(bic)
    models.append(model)
best_idx = np.argmin(bics)
best_n = range_n[best_idx]
best_model = models[best_idx]

print(f"Nombre optimal d'états cachés (BIC) sur la période d'entraînement : {best_n}")

# 4. Prédiction des états cachés et observations sur la période de test
# On concatène train+test pour avoir la séquence complète d'états
all_data = np.concatenate([train_data, test_data])
all_dates = np.concatenate([train_dates, test_dates])
all_hidden = best_model.predict(all_data)

# Pour la période de test, on prédit les observations attendues comme la moyenne de l'état caché prédit
means = best_model.means_.flatten()
test_hidden = all_hidden[len(train_data):]
predicted_test = means[test_hidden]

# 5. Visualisation et comparaison
plt.figure(figsize=(15, 6))
plt.plot(test_dates, test_data, 'o-', label='Observé (réalité)', color='blue')
plt.plot(test_dates, predicted_test, 'o-', label='Prédit (HMM)', color='orange')
plt.xlabel('Date')
plt.ylabel('Cas pour 10k habitants (MA)')
plt.title(f'Prédiction HMM sur Bruxelles ({train_months} mois entraînement, {test_months} mois test)')
plt.legend()
plt.tight_layout()
plt.show()

# 6. Métrique d'erreur
rmse = np.sqrt(np.mean((test_data.flatten() - predicted_test)**2))
print(f"RMSE (erreur quadratique moyenne) sur la période de test : {rmse:.2f}")

# 7. Commentaires mathématiques
print("""
- On découpe la série temporelle en deux : entraînement (pour ajuster le modèle) et test (pour évaluer la capacité de prédiction).
- Le HMM apprend les états cachés et leurs moyennes sur la période d'entraînement.
- Sur la période de test, on prédit la moyenne de l'état caché détecté comme valeur attendue.
- On compare la prédiction à la réalité avec un graphique et le RMSE.
""") 