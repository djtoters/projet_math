import pandas as pd
import numpy as np
import json


def hampel_filter_for_series(s, window_size, n_sigmas=3):
    """
    Applies the Hampel filter to remove outliers from a data series.

    Args:
    s (pd.Series): The data series to filter.
    window_size (int): The size of the rolling window (centered).
    n_sigmas (int): The number of standard deviations to use as the threshold.

    Returns:
    pd.Series: The filtered data series.
    """
    L = window_size // 2
    rolling_median = s.rolling(window=2 * L + 1, center=True).median()
    MAD = lambda x: np.median(np.abs(x - rolling_median))
    rolling_mad = s.rolling(window=2 * L + 1, center=True).apply(MAD)
    threshold = n_sigmas * 1.4826 * rolling_mad
    differences = np.abs(s - rolling_median)
    outlier_idx = differences > threshold
    s[outlier_idx] = rolling_median[outlier_idx]
    return s


def moving_average_filter(s, window_size=21):
    """
    Applies a moving average filter to smooth the data series.

    Args:
    s (pd.Series): The data series to smooth.
    window_size (int): The size of the rolling window (centered).

    Returns:
    pd.Series: The smoothed data series.
    """
    return s.rolling(window=window_size, center=True).mean()


# Load data from JSON file
filename = "Standardized_Covid19_data10K.json"
with open(filename, "r") as file:
    data = json.load(file)

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)
df["CASES_PER_10K"] = pd.to_numeric(df["CASES_PER_10K"])
df["DATE"] = pd.to_datetime(df["DATE"])
df = df[["DATE", "TX_DESCR_FR", "CASES_PER_10K"]]

# Apply filters and round the results
for commune in df["TX_DESCR_FR"].unique():
    mask = df["TX_DESCR_FR"] == commune
    df.loc[mask, "CASES_PER_10K"] = hampel_filter_for_series(
        df.loc[mask, "CASES_PER_10K"], window_size=7, n_sigmas=3
    )
    df.loc[mask, "CASES_PER_10K_MA"] = moving_average_filter(
        df.loc[mask, "CASES_PER_10K"]
    )
    df.loc[mask, "CASES_PER_10K_MA"] = np.round(df.loc[mask, "CASES_PER_10K_MA"], 2)

# Handle NaN values created by moving average filter
df["CASES_PER_10K_MA"] = df.groupby("TX_DESCR_FR")["CASES_PER_10K_MA"].transform(
    lambda x: x.interpolate()
)
df["CASES_PER_10K_MA"].fillna(method="bfill", inplace=True)
df["CASES_PER_10K_MA"].fillna(method="ffill", inplace=True)

# Save the processed data to a CSV file
df.to_csv("Filtered_Covid19_data.csv", index=False)
