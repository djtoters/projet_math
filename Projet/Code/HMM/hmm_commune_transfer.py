import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn import hmm

# 1. Chargement des données
DATA_PATH = "../Filtered_Covid19_data.csv"
df = pd.read_csv(DATA_PATH)
df["DATE"] = pd.to_datetime(df["DATE"])

# Afficher la liste des communes disponibles
communes = sorted(df["TX_DESCR_FR"].unique())
print("Communes disponibles :")
for i, c in enumerate(communes):
    print(f"  {i+1}. {c}")

def select_commune(prompt):
    val = input(prompt)
    # Permettre la sélection par numéro ou par nom
    if val.isdigit():
        idx = int(val) - 1
        if 0 <= idx < len(communes):
            return communes[idx]
        else:
            print("Numéro invalide. Veuillez réessayer.")
            return select_commune(prompt)
    elif val in communes:
        return val
    else:
        print("Nom de commune invalide. Veuillez réessayer.")
        return select_commune(prompt)

commune_train = select_commune("Commune d'entraînement (numéro ou nom) : ")
commune_test = select_commune("Commune de test (numéro ou nom) : ")
train_months = int(input("Combien de mois pour l'entraînement du modèle ? (0 = toute la période) "))
test_months = int(input("Combien de mois pour la prédiction (test) ? "))

# 2. Sélection des données pour chaque commune
train_df = df[df["TX_DESCR_FR"] == commune_train].copy()
test_df = df[df["TX_DESCR_FR"] == commune_test].copy()

# 3. Découpage dynamique selon le choix utilisateur (en se basant sur les dates de la commune d'entraînement)
train_start = train_df["DATE"].min()
if train_months == 0:
    # Utiliser toute la période disponible pour la commune d'entraînement
    train_end = train_df["DATE"].max() + pd.Timedelta(days=1)  # inclure le dernier jour
    test_end = train_end
    print(f"Mode : entraînement sur toute la période ({train_start.date()} à {(train_end - pd.Timedelta(days=1)).date()})")
else:
    train_end = train_start + pd.DateOffset(months=train_months)
    test_end = train_end + pd.DateOffset(months=test_months)

train_mask = (train_df["DATE"] < train_end)
if train_months == 0:
    # Prédire sur la même période pour la commune de test
    test_mask = (test_df["DATE"] >= train_start) & (test_df["DATE"] < train_end)
else:
    test_mask = (test_df["DATE"] >= train_end) & (test_df["DATE"] < test_end)

train_data = train_df.loc[train_mask, "CASES_PER_10K_MA"].values.reshape(-1, 1)
train_dates = train_df.loc[train_mask, "DATE"].values
test_data = test_df.loc[test_mask, "CASES_PER_10K_MA"].values.reshape(-1, 1)
test_dates = test_df.loc[test_mask, "DATE"].values

# Vérification de la présence de données
if len(train_data) == 0:
    print("Erreur : aucune donnée pour la période d'entraînement sélectionnée dans la commune d'entraînement.")
    print(f"Vérifiez la disponibilité des données pour {commune_train} entre {train_start.date()} et {(train_end - pd.Timedelta(days=1)).date()}.")
    exit(1)
if len(test_data) == 0:
    print("Erreur : aucune donnée pour la période de test sélectionnée dans la commune de test.")
    if train_months == 0:
        print(f"Vérifiez la disponibilité des données pour {commune_test} entre {train_start.date()} et {(train_end - pd.Timedelta(days=1)).date()}.")
    else:
        print(f"Vérifiez la disponibilité des données pour {commune_test} entre {train_end.date()} et {(test_end - pd.Timedelta(days=1)).date()}.")
    exit(1)

# 4. Sélection du nombre optimal d'états cachés (BIC)
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

print(f"Nombre optimal d'états cachés (BIC) sur la période d'entraînement ({commune_train}) : {best_n}")

# 5. Application du modèle sur la commune de test
# On prédit la séquence d'états cachés et la valeur attendue (moyenne de l'état)
test_hidden = best_model.predict(test_data)
means = best_model.means_.flatten()
predicted_test = means[test_hidden]

# 6. Visualisation et comparaison
plt.figure(figsize=(15, 6))
plt.plot(test_dates, test_data, 'o-', label=f'Observé ({commune_test})', color='blue')
plt.plot(test_dates, predicted_test, 'o-', label=f'Prédit (HMM entraîné sur {commune_train})', color='orange')
plt.xlabel('Date')
plt.ylabel('Cas pour 10k habitants (MA)')
plt.title(f'Prédiction croisée HMM : entraînement {commune_train}, test {commune_test}\n({train_months} mois entraînement, {test_months} mois test)')
plt.legend()
plt.tight_layout()
plt.show()

# 7. Métrique d'erreur
rmse = np.sqrt(np.mean((test_data.flatten() - predicted_test)**2))
print(f"RMSE (erreur quadratique moyenne) sur la période de test ({commune_test}) : {rmse:.2f}")

# 8. Commentaires mathématiques
print(f"""
- On entraîne le HMM sur la commune source ({commune_train}) sur la période d'entraînement.
- On applique le modèle sur la commune cible ({commune_test}) sur la période de test.
- On compare la prédiction à la réalité avec un graphique et le RMSE.
- Cela permet d'évaluer la transférabilité du modèle entre communes.
""") 