import pandas as pd
from hmmlearn import hmm
import numpy as np

# Charger les données
df = pd.read_csv("Filtered_Covid19_data.csv")
df["DATE"] = pd.to_datetime(df["DATE"])
df = df[df["TX_DESCR_FR"] == "Bruxelles"]  # Filtrer pour Bruxelles

# Préparation des données
# Nous supposons que 'CASES_PER_10K_MA' est la colonne d'intérêt
data = df["CASES_PER_10K_MA"].values.reshape(-1, 1)

# Configuration du HMM
# Utilisation d'un modèle Gaussian HMM avec 7 états cachés
model = hmm.GaussianHMM(
    n_components=6, covariance_type="diag", n_iter=10000, random_state=42
)

# Entraînement du modèle
model.fit(data)

# Examiner les paramètres appris
print("Matrices de transition entre les états :")
print(model.transmat_)
print("\nMoyennes des distributions gaussiennes pour chaque état :")
print(model.means_)

# Utiliser le modèle pour prédire la séquence des états
hidden_states = model.predict(data)

# Afficher les états cachés pour quelques observations
print("\nÉtats cachés prédits pour les données :")
print(hidden_states[:1000])  # Afficher les premiers 100 états prédits

"""
Bien sûr, je vais vous expliquer les différents éléments du code utilisé pour configurer et entraîner le modèle de Markov caché (HMM) avec `hmmlearn`, en mettant l'accent sur les choix spécifiques tels que le `random_state` et le type de matrice de covariance.

### 1. **Choix du modèle : `GaussianHMM`**
Nous utilisons un `GaussianHMM`, un modèle de Markov caché où les émissions suivent une distribution gaussienne. Cela signifie que chaque état caché du modèle produit des observations (ou émissions) qui peuvent être décrites par une distribution normale, caractérisée par une moyenne et une variance. Ce choix est courant pour les séries temporelles de données continues, comme les cas de COVID-19 par 10 000 habitants.

### 2. **Paramètre `n_components`**
Le paramètre `n_components=7` indique que le modèle doit apprendre sept états cachés. Dans votre cas, ces états pourraient correspondre à différents niveaux de sévérité de l'épidémie de COVID-19. Le nombre d'états est choisi en fonction de la complexité des données et de la granularité des insights que vous souhaitez obtenir.

### 3. **Paramètre `covariance_type="diag"`**
- **`"diag"`**: Chaque état a sa propre matrice de covariance diagonale. Cela signifie que les variables observées (dans votre cas, un seul variable, les cas de COVID-19) sont supposées être indépendantes les unes des autres, et chaque variable a sa propre variance. Pour un modèle à une seule dimension comme le vôtre, cela signifie simplement que chaque état a sa propre variance unique pour les observations qu'il génère.
- **Alternatives**:
  - **`"full"`** : Chaque état aurait une matrice de covariance complète, permettant de modéliser les covariances entre toutes les paires de variables observées. Pour des données unidimensionnelles, cela n'est pas nécessaire.
  - **`"spherical"`** et **`"tied"`** offrent d'autres façons de structurer les covariances, mais ne sont pas aussi pertinentes pour votre configuration unidimensionnelle.

### 4. **Paramètre `n_iter`**
`n_iter=1000` indique que l'algorithme d'apprentissage (l'algorithme Expectation-Maximization, ou EM) exécutera jusqu'à 1000 itérations pour tenter de converger vers les meilleurs paramètres du modèle. Plus `n_iter` est élevé, plus l'algorithme a de chances de converger, mais cela augmente aussi le temps de calcul.

### 5. **Paramètre `random_state=42`**
- **Rôle** : Le `random_state` est utilisé pour la reproductibilité des résultats. Dans les modèles statistiques ou de machine learning qui impliquent des processus aléatoires (comme l'initialisation des paramètres), fixer le `random_state` garantit que vous obtiendrez les mêmes résultats à chaque exécution.
- **Choix de `42`** : Le nombre `42` est un choix arbitraire et couramment utilisé dans de nombreux exemples de programmation en raison de sa popularité culturelle (référence au livre "The Hitchhiker's Guide to the Galaxy"). Vous pouvez utiliser n'importe quel entier, l'important étant de le garder constant si vous avez besoin de résultats reproductibles.

### Résumé
Chaque choix dans la configuration du HMM est fait pour adapter le modèle aux spécificités de vos données et à vos objectifs d'analyse. Le `GaussianHMM` avec une matrice de covariance diagonale est adapté pour des séries temporelles unidimensionnelles et continues. Fixer `random_state` et utiliser `n_iter` élevé aide à assurer la stabilité et la convergence de l'apprentissage du modèle.
"""
