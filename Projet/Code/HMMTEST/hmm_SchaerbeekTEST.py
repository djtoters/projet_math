import pandas as pd
import matplotlib.pyplot as plt
from hmmlearn import hmm
from sklearn.model_selection import train_test_split

# Load data and ensure correct date formatting
df = pd.read_csv("../Filtered_Covid19_data.csv")
df["DATE"] = pd.to_datetime(df["DATE"])
df_schaerbeek = df[df["TX_DESCR_FR"] == "Schaerbeek"]

# Prepare data for modeling
X = df_schaerbeek["CASES_PER_10K_MA"].values.reshape(-1, 1)

# Split data into 70% training and 30% testing
X_train, X_test, dates_train, dates_test = train_test_split(
    X, df_schaerbeek["DATE"], test_size=0.3, random_state=425, shuffle=False
)

# Configure the Hidden Markov Model
model = hmm.GaussianHMM(
    n_components=7, covariance_type="full", n_iter=10000, random_state=425
)

# Train the model on the training data
model.fit(X_train)

# Predict hidden states for the test data
hidden_states_test = model.predict(X_test)

# Print predicted hidden states for the test data
print("États cachés prédits pour les données de test :")
print(hidden_states_test)

# Plot the predicted hidden states over time
plt.figure(figsize=(15, 5))
plt.plot(dates_test.reset_index(drop=True), hidden_states_test, drawstyle="steps-post")
plt.title("États cachés prédits sur les données de test")
plt.xlabel("Date")
plt.ylabel("État caché")
plt.show()

# Display the transition matrix of the model
print("Matrice de transition entre les états :")
print(model.transmat_)

# Display the means of each state
print("Moyennes des états :")
print(model.means_)
