import pandas as pd
import matplotlib.pyplot as plt
from hmmlearn import hmm
from sklearn.model_selection import train_test_split

# Charger les données et s'assurer que le formatage des dates est correct
df = pd.read_csv("../Filtered_Covid19_data.csv")
df["DATE"] = pd.to_datetime(df["DATE"])

# Liste de toutes les communes de Bruxelles
communes = [
    "Anderlecht",
    "Auderghem",
    "Berchem-Sainte-Agathe",
    "Bruxelles",
    "Etterbeek",
    "Evere",
    "Forest (Bruxelles-Capitale)",
    "Ganshoren",
    "Ixelles",
    "Jette",
    "Koekelberg",
    "Molenbeek-Saint-Jean",
    "Saint-Gilles",
    "Saint-Josse-ten-Noode",
    "Schaerbeek",
    "Uccle",
    "Watermael-Boitsfort",
    "Woluwe-Saint-Lambert",
    "Woluwe-Saint-Pierre",
]

# Traiter les données pour chaque commune
for commune in communes:
    df_commune = df[df["TX_DESCR_FR"] == commune]
    X = df_commune["CASES_PER_10K_MA"].values.reshape(-1, 1)

    # Diviser les données en 70% pour l'entraînement et 30% pour les tests
    X_train, X_test, dates_train, dates_test = train_test_split(
        X, df_commune["DATE"], test_size=0.3, random_state=425, shuffle=False
    )

    # Configurer le modèle de Markov caché
    model = hmm.GaussianHMM(
        n_components=7, covariance_type="full", n_iter=10000, random_state=425
    )

    # Entraîner le modèle sur les données d'entraînement
    model.fit(X_train)

    # Prédire les états cachés pour les données de test
    hidden_states_test = model.predict(X_test)

    # Afficher les états cachés prédits pour les données de test
    print(f"États cachés prédits pour les données de test - {commune}:")
    print(hidden_states_test)

    # Tracer les états cachés prédits dans le temps
    plt.figure(figsize=(15, 5))
    plt.plot(
        dates_test.reset_index(drop=True), hidden_states_test, drawstyle="steps-post"
    )
    plt.title(f"États cachés prédits sur les données de test - {commune}")
    plt.xlabel("Date")
    plt.ylabel("État caché")
    plt.show()

    # Afficher la matrice de transition du modèle
    print(f"Matrice de transition entre les états - {commune}:")
    print(model.transmat_)

    # Afficher les moyennes de chaque état
    print(f"Moyennes des états - {commune}:")
    print(model.means_)
