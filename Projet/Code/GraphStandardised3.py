import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.ticker as ticker

# Chemin vers le fichier JSON contenant les données standardisées de COVID-19
filename = "Standardized_Covid19_data10K.json"

# Charger les données depuis le fichier JSON
with open(filename, "r") as file:
    data = json.load(file)

# Conversion des données JSON en DataFrame pandas pour une manipulation plus facile
df = pd.DataFrame(data)

# Conversion de 'CASES_PER_10K' en nombres décimaux et de 'DATE' en type date
df["CASES_PER_10K"] = pd.to_numeric(df["CASES_PER_10K"])
df["DATE"] = pd.to_datetime(df["DATE"])

# Sélection des colonnes pertinentes pour l'analyse
df = df[["DATE", "TX_DESCR_FR", "CASES_PER_10K"]]

# Extraction de la liste des communes pour lesquelles des graphiques seront générés
communes = df["TX_DESCR_FR"].unique()

# Génération et enregistrement d'un graphique pour chaque commune
for commune in communes:
    plt.figure(figsize=(10, 6))
    commune_data = df[df["TX_DESCR_FR"] == commune]
    total_cases_per_10k_per_day = (
        commune_data.groupby("DATE")["CASES_PER_10K"].sum().reset_index()
    )
    # Création d'un graphique linéaire avec points pour chaque jour
    plt.plot(
        total_cases_per_10k_per_day["DATE"],
        total_cases_per_10k_per_day["CASES_PER_10K"],
        linestyle="-",
        linewidth=1,
        label=f"Cas/10k habitants",
    )
    plt.scatter(
        total_cases_per_10k_per_day["DATE"],
        total_cases_per_10k_per_day["CASES_PER_10K"],
        s=10,  # Points ajoutés pour chaque jour
    )

    # Configuration des titres et des axes
    plt.title(f"Évolution des cas de COVID-19 pour 10k habitants - {commune}")
    plt.xlabel("Date")
    plt.ylabel("Cas de COVID-19 par 10 000 habitants")
    plt.xticks(rotation=45)
    plt.legend()

    # Ajustement de l'axe des ordonnées pour une meilleure précision
    ax = plt.gca()
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.2f}"))

    plt.tight_layout()

    # Sauvegarde du graphique dans un fichier image
    plt.savefig(f"COVID19_{commune.replace(' ', '_').replace('/', '_')}.png")
    plt.close()  # Fermer la figure courante pour libérer la mémoire
