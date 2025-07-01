import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

# Chemin vers votre fichier JSON - assurez-vous que c'est le fichier correctement standardisé
filename = "Standardized_Covid19_data.json"  # Nom mis à jour pour correspondre à la sortie du script précédent

# Charger les données depuis le fichier JSON
with open(filename, "r") as file:
    data = json.load(file)

# Convertir les données en DataFrame pandas
df = pd.DataFrame(data)

# Convertir 'CASES_PER_100K' en nombres décimaux et les dates en type date
df["CASES_PER_100K"] = pd.to_numeric(df["CASES_PER_100K"])
df["DATE"] = pd.to_datetime(df["DATE"])

# Sélectionner un sous-ensemble de colonnes pertinentes, en incluant 'CASES_PER_100K'
df = df[["DATE", "TX_DESCR_FR", "CASES_PER_100K"]]

# Générer un nuage de points avec une ligne pour chaque commune
plt.figure(figsize=(28, 16))

# Liste de couleurs pour distinguer chaque commune
colors = plt.cm.jet(np.linspace(0, 1, len(df["TX_DESCR_FR"].unique())))

for commune, color in zip(df["TX_DESCR_FR"].unique(), colors):
    commune_data = df[df["TX_DESCR_FR"] == commune]
    total_cases_per_100k_per_day = (
        commune_data.groupby("DATE")["CASES_PER_100K"].sum().reset_index()
    )
    plt.scatter(
        total_cases_per_100k_per_day["DATE"],
        total_cases_per_100k_per_day["CASES_PER_100K"],
        color=color,
        label=commune,
    )
    plt.plot(
        total_cases_per_100k_per_day["DATE"],
        total_cases_per_100k_per_day["CASES_PER_100K"],
        color=color,
        linestyle="-",
        linewidth=1,
    )  # Ligne fine ajoutée ici

plt.title(
    "Évolution du nombre total de cas de COVID-19 par 100 000 habitants par jour et par commune"
)
plt.xlabel("Date")
plt.ylabel("Cas de COVID-19 par 100 000 habitants")
plt.xticks(rotation=45)
plt.legend(title="Commune", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

# Afficher le graphique
plt.show()
