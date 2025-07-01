import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.ticker as ticker


# Fonction pour appliquer le filtre Hampel à une série
def hampel_filter_for_series(s, window_size, n_sigmas=3):
    L = window_size // 2
    rolling_median = s.rolling(window=2 * L + 1, center=True).median()
    MAD = lambda x: np.median(np.abs(x - np.median(x)))
    rolling_mad = s.rolling(window=2 * L + 1, center=True).apply(MAD)
    threshold = n_sigmas * 1.4826 * rolling_mad
    differences = np.abs(s - rolling_median)
    outlier_idx = differences > threshold
    s_filtered = s.copy()
    s_filtered[outlier_idx] = rolling_median[outlier_idx]
    return s_filtered


# Charger les données depuis le fichier JSON
filename = "Standardized_Covid19_data10K.json"
with open(filename, "r") as file:
    data = json.load(file)

# Convertir les données en DataFrame pandas
df = pd.DataFrame(data)
df["CASES_PER_10K"] = pd.to_numeric(df["CASES_PER_10K"])
df["DATE"] = pd.to_datetime(df["DATE"])
df = df[["DATE", "TX_DESCR_FR", "CASES_PER_10K"]]

# Liste des tailles de fenêtres à tester
window_sizes = [7, 14, 21, 28]  # Une semaine à un mois
n_sigmas = 3

# Tester différentes tailles de fenêtre
for window_size in window_sizes:
    df_filtered = df.copy()
    # Appliquer le filtre Hampel à chaque commune séparément pour chaque taille de fenêtre
    for commune in df["TX_DESCR_FR"].unique():
        mask = df["TX_DESCR_FR"] == commune
        df_filtered.loc[mask, "CASES_PER_10K"] = hampel_filter_for_series(
            df.loc[mask, "CASES_PER_10K"], window_size=window_size, n_sigmas=n_sigmas
        )

    # Générer et sauvegarder un graphique pour chaque commune pour chaque taille de fenêtre
    for commune in df_filtered["TX_DESCR_FR"].unique():
        plt.figure(figsize=(10, 6))
        commune_data = df_filtered[df_filtered["TX_DESCR_FR"] == commune]
        total_cases_per_10k_per_day = (
            commune_data.groupby("DATE")["CASES_PER_10K"].sum().reset_index()
        )
        plt.plot(
            total_cases_per_10k_per_day["DATE"],
            total_cases_per_10k_per_day["CASES_PER_10K"],
            linestyle="-",
            linewidth=1,
            label=f"Cas/10k habitants - Window {window_size}",
        )
        plt.scatter(
            total_cases_per_10k_per_day["DATE"],
            total_cases_per_10k_per_day["CASES_PER_10K"],
            s=10,
        )

        plt.title(
            f"Évolution des cas de COVID-19 pour 10k habitants avec fenêtre {window_size} - {commune}"
        )
        plt.xlabel("Date")
        plt.ylabel("Cas de COVID-19 par 10 000 habitants")
        plt.xticks(rotation=45)
        plt.legend()

        ax = plt.gca()
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.2f}"))

        plt.tight_layout()
        plt.savefig(
            f"COVID19_{window_size}_{commune.replace(' ', '_').replace('/', '_')}.png"
        )
        plt.close()
