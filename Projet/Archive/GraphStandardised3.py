import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.ticker as ticker

# Chemin vers votre fichier JSON standardisé
filename = "Standardized_Covid19_data10K.json"

# Charger les données depuis le fichier JSON
with open(filename, "r") as file:
    data = json.load(file)

# Convertir les données en DataFrame pandas
df = pd.DataFrame(data)

# Assurer que 'CASES_PER_10K' est en nombres décimaux et les dates en type date
df["CASES_PER_10K"] = pd.to_numeric(df["CASES_PER_10K"])
df["DATE"] = pd.to_datetime(df["DATE"])

# Sélectionner un sous-ensemble de colonnes pertinentes, en incluant 'CASES_PER_10K'
df = df[["DATE", "TX_DESCR_FR", "CASES_PER_10K"]]

# Obtenir la liste unique des communes
communes = df["TX_DESCR_FR"].unique()

# Générer et sauvegarder un graphique pour chaque commune
for commune in communes:
    plt.figure(figsize=(10, 6))
    commune_data = df[df["TX_DESCR_FR"] == commune]
    total_cases_per_10k_per_day = (
        commune_data.groupby("DATE")["CASES_PER_10K"].sum().reset_index()
    )
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

    plt.title(f"Évolution des cas de COVID-19 pour 10k habitants - {commune}")
    plt.xlabel("Date")
    plt.ylabel("Cas de COVID-19 par 10 000 habitants")
    plt.xticks(rotation=45)
    plt.legend()

    # Ajuster la précision de l'axe des ordonnées
    ax = plt.gca()  # Get current axes
    ax.yaxis.set_major_locator(
        ticker.AutoLocator()
    )  # Ajuste automatiquement les graduations
    ax.yaxis.set_minor_locator(
        ticker.AutoMinorLocator()
    )  # Ajoute des graduations mineures pour plus de précision
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f"{x:.2f}")
    )  # Format avec 2 décimales

    plt.tight_layout()

    # Sauvegarder le graphique avec un nom de fichier basé sur le nom de la commune
    plt.savefig(f"COVID19_{commune.replace(' ', '_').replace('/', '_')}.png")
    plt.close()  # Fermer la figure courante pour libérer la mémoire
