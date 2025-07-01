import pandas as pd
import numpy as np
import json

# Charger les données depuis le fichier JSON
filename = "Standardized_Covid19_data10K.json"
with open(filename, "r") as file:
    data = json.load(file)

# Convertir les données en DataFrame pandas
df = pd.DataFrame(data)
df["CASES_PER_10K"] = pd.to_numeric(df["CASES_PER_10K"])
df["DATE"] = pd.to_datetime(df["DATE"])
df = df[["DATE", "TX_DESCR_FR", "CASES_PER_10K"]]

# Fonction pour appliquer le filtre Hampel à une série
def hampel_filter_for_series(s, window_size, n_sigmas=3):
    L = window_size // 2
    rolling_median = s.rolling(window=2*L+1, center=True).median()
    MAD = lambda x: np.median(np.abs(x - np.median(x)))
    rolling_mad = s.rolling(window=2*L+1, center=True).apply(MAD)
    threshold = n_sigmas * 1.4826 * rolling_mad
    differences = np.abs(s - rolling_median)
    outlier_idx = differences > threshold
    s_filtered = s.copy()
    s_filtered[outlier_idx] = rolling_median[outlier_idx]
    return s_filtered

# Fonction pour appliquer le lissage par moyenne mobile
def moving_average_filter(s, window_size=7):
    return s.rolling(window=window_size, center=True).mean()

# Appliquer les filtres Hampel et moyenne mobile à chaque commune
for commune in df["TX_DESCR_FR"].unique():
    mask = df["TX_DESCR_FR"] == commune
    df.loc[mask, "CASES_PER_10K"] = hampel_filter_for_series(
        df.loc[mask, "CASES_PER_10K"], window_size=7, n_sigmas=3
    )
    df.loc[mask, "CASES_PER_10K_MA"] = moving_average_filter(
        df.loc[mask, "CASES_PER_10K"]
    )

# Interpolation pour les valeurs NaN générées par le lissage moyen mobile
df["CASES_PER_10K_MA"] = df.groupby("TX_DESCR_FR")["CASES_PER_10K_MA"].transform(lambda x: x.interpolate())
# Remplissage des valeurs NaN restantes aux extrémités
df["CASES_PER_10K_MA"].fillna(method='bfill', inplace=True)
df["CASES_PER_10K_MA"].fillna(method='ffill', inplace=True)

# df_filtered maintenant contient les données traitées sans NaN
df_filtered = df

# Sauvegarde du DataFrame traité pour une utilisation future
df_filtered.to_csv('Filtered_Covid19_data.csv', index=False)
