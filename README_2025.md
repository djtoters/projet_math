---

# Rapport détaillé sur le traitement, l’analyse et l’amélioration des données COVID-19 à Bruxelles

---

## 1. **Traitement initial des données COVID-19 (travail de l’équipe précédente)**

### a) **Nettoyage et correction des données**

- **Source** : Un fichier Excel listant tous les cas d’infection en Belgique du 01-03-2020 au 03-04-2021.
- **Filtrage** : Suppression des données inutiles pour ne garder que les 19 communes de Bruxelles.
- **Remplacement des valeurs** `<5` : Les valeurs `<5` (cas très faibles) ont été remplacées par 2, pour éviter de fausser les analyses tout en restant conservateur.
- **Complétion des données manquantes** : Un script (`updateJson.py`) a été utilisé pour ajouter les jours manquants (où une commune n’apparaissait pas), en leur attribuant 0 cas.
- **Standardisation** : Les cas ont été rapportés à la population de chaque commune (cas pour 10 000 habitants) grâce au script `standart.py` et aux données de population officielles.
- **Format final** : Les données nettoyées et standardisées ont été sauvegardées dans des fichiers JSON et CSV, utilisables pour l’analyse.

### b) **Filtrage et lissage**

- **Filtrage Hampel** : Utilisé pour supprimer les valeurs aberrantes (outliers) dans les séries temporelles, en remplaçant les points anormaux par la médiane locale.
- **Moyenne mobile (MA)** : Appliquée pour lisser les courbes et mieux visualiser les tendances, en réduisant le bruit.
- **Combinaison Hampel + MA** : Permet d’obtenir des séries temporelles robustes, sans outliers et lissées, prêtes pour la modélisation.

---

## 2. **Premières analyses et algorithmes utilisés**

### a) **Visualisation**

- Génération de graphiques pour chaque commune, montrant l’évolution des cas standardisés, avec et sans lissage.

### b) **Détection de phases**

- Utilisation de l’algorithme de Hampel pour détecter les changements de régime (changements brusques dans la série).

### c) **Modélisation HMM (Hidden Markov Model)**

- Application de HMM pour modéliser les “phases cachées” de l’épidémie (faible, moyen, fort).
- Utilisation de l’algorithme EM pour estimer les paramètres du HMM.
- Sélection du nombre d’états cachés de façon empirique (souvent fixé à 7).
- Résultats : Séquences d’états cachés, matrices de transition, moyennes par état, visualisation des phases.

---

## 3. **Limites des méthodes initiales**

- **Choix arbitraire du nombre d’états cachés** (pas de sélection optimale).
- **Pas de validation croisée ni de test de robustesse**.
- **Peu d’analyse prédictive** (modèle descriptif, peu de tests de prévision).
- **Pas d’analyse de la transférabilité entre communes**.
- **Pas de matrice de transition inter-communes (19x19)**.

---

## 4. **Améliorations et nouvelles approches mises en place**

### a) **Sélection optimale du modèle**

- Utilisation du critère BIC pour choisir automatiquement le nombre d’états cachés ou de composantes (HMM/GMM).

### b) **Analyse mathématique avancée**

- Classement automatique des états cachés (faible, intermédiaire, pic).
- Statistiques détaillées : durée, nombre d’épisodes, dates de début/fin, etc.
- Visualisation enrichie avec légende et annotation des phases.

### c) **Prédiction et validation**

- Découpage de la série temporelle en période d’entraînement et de test.
- Entraînement du HMM sur une période, prédiction sur la suivante, comparaison à la réalité (graphique + RMSE).

### d) **Transférabilité inter-communes**

- Entraînement du modèle sur une commune, application à une autre, comparaison des prédictions à la réalité.

### e) **Modélisation GMM/EM**

- Application d’un modèle de mélange gaussien (GMM) pour détecter les phases, avec explication du rôle de l’algorithme EM.

### f) **Matrice de transition 19x19**

- Construction d’une matrice de transition entre les 19 communes, basée sur le classement quotidien par nombre de cas.
- Visualisation et analyse de la stabilité des positions des communes.

### g) **Ergonomie et robustesse**

- Sélection conviviale des communes (liste interactive).
- Prompts pour choisir la période d’analyse.
- Vérification automatique de la présence de données.

---

## 5. **Comparaison des résultats**

| Aspect                | Approche initiale        | Améliorations apportées                   |
|-----------------------|--------------------------|-------------------------------------------|
| Nettoyage des données | Oui, mais manuel         | Oui, + robustesse et standardisation      |
| Lissage/filtrage      | Hampel, MA               | Hampel + MA, choix de fenêtre optimisé    |
| Modélisation HMM      | Oui, nombre d’états fixé | Sélection optimale (BIC), analyse avancée |
| Prédiction            | Non                      | Oui, validation sur période de test       |
| Transférabilité       | Non                      | Oui, test inter-communes                  |
| GMM/EM                | Non                      | Oui, explication pédagogique              |
| Matrice 19x19         | Non                      | Oui, analyse spatiale                     |
| Ergonomie             | Scripts manuels          | Prompts interactifs, vérifications        |

---

## 6. Détail des différentes approches mises en place (explications pédagogiques)

---

### a) **HMM par commune (modélisation des phases cachées)**

**But** :  
Découvrir automatiquement les différentes “phases” de l’épidémie (périodes calmes, pics, etc.) dans chaque commune, même si on ne les observe pas directement.

**Comment ça marche ?**

- On suppose que chaque jour, la situation d’une commune (faible, moyenne, forte circulation du virus) est “cachée”.
- On observe seulement le nombre de cas.
- Le modèle HMM (Hidden Markov Model) “devine” pour chaque jour dans quelle phase la commune se trouve, en se basant sur l’évolution des cas.

**Ce que le script fait :**

- Il choisit automatiquement le nombre de phases à détecter (grâce au BIC).
- Il attribue à chaque jour une phase cachée.
- Il affiche la courbe des cas, colorée selon la phase détectée.
- Il donne des statistiques : combien de jours dans chaque phase, quelles sont les moyennes de cas, etc.

**Exemple imagé :**

> Imagine que tu observes la météo chaque jour (pluie, soleil, nuages), mais tu ne sais pas s’il fait chaud ou froid. Le HMM va “deviner” les périodes chaudes et froides, même si tu ne les vois pas directement, juste en regardant la météo.

![hmm_bxl.png](.attachments.1649050/hmm_bxl.png)

---

### b) **GMM/EM (détection de phases par mélange gaussien)**

**But** :  
Regrouper les jours qui se ressemblent en “phases” (faible, moyen, fort) sans tenir compte de l’ordre dans le temps.

**Comment ça marche ?**

- On suppose que les nombres de cas observés viennent de plusieurs groupes (ou “cloches” statistiques).
- Le modèle GMM (Gaussian Mixture Model) va regrouper les jours en fonction de leur niveau de cas.
- L’algorithme EM (Expectation-Maximization) sert à trouver automatiquement ces groupes.

**Ce que le script fait :**

- Il choisit le nombre de groupes optimal (grâce au BIC).
- Il attribue chaque jour à un groupe (phase).
- Il affiche la courbe des cas, colorée selon le groupe.

**Exemple imagé :**

> Imagine que tu ranges des billes de différentes couleurs dans des boîtes, sans savoir combien de boîtes il te faut. Le GMM va trouver le bon nombre de boîtes et ranger chaque bille dans la bonne boîte selon sa couleur.

---

### c) **Prédiction intra-commune (entraînement sur une période, test sur une autre)**

**But** :  
Vérifier si le modèle peut prévoir l’évolution des cas dans une commune, en se basant sur ce qui s’est passé avant.

**Comment ça marche ?**

- On coupe la courbe des cas en deux : une partie pour “apprendre” (entraînement), une partie pour “prédire” (test).
- On entraîne le modèle HMM sur la première partie.
- On demande au modèle de prédire la suite (la phase cachée et le nombre de cas attendu).
- On compare la prédiction à la réalité.

**Ce que le script fait :**

- Il affiche la courbe réelle et la courbe prédite.
- Il calcule l’erreur de prédiction (plus elle est faible, mieux c’est).

**Exemple imagé :**

> C’est comme apprendre à reconnaître le rythme d’un morceau de musique, puis essayer de deviner la suite du morceau sans l’écouter.

![hmm_forecast.png](.attachments.1649050/hmm_forecast.png)

---

### d) **Transférabilité inter-communes (entraîner sur une commune, tester sur une autre)**

**But** :  
Voir si ce qu’on a appris sur une commune peut servir à comprendre ou prévoir ce qui se passe dans une autre commune.

**Comment ça marche ?**

- On entraîne le modèle HMM sur toutes les données d’une commune (ex : Bruxelles).
- On applique ce modèle à une autre commune (ex : Anderlecht) pour voir si les phases détectées et les prédictions sont cohérentes.
- On compare la prédiction à la réalité sur la commune test.

**Ce que le script fait :**

- Il affiche la courbe réelle de la commune test et la courbe prédite par le modèle entraîné ailleurs.
- Il calcule l’erreur de prédiction.

**Exemple imagé :**

> C’est comme apprendre à reconnaître les saisons en France, puis essayer de deviner les saisons en Belgique avec la même méthode.

![hmm_commune_transfert.png](.attachments.1649050/hmm_commune_transfert.png)

---

### e) **Matrice de transition 19x19 (analyse spatiale entre communes)**

**But** :  
Analyser comment les communes de Bruxelles changent de place dans le classement des cas COVID d’un jour à l’autre.

**Comment ça marche ?**

- Chaque jour, on classe les 19 communes de la moins touchée à la plus touchée.
- On regarde, pour chaque commune, si elle garde sa place ou si elle monte/descend dans le classement le lendemain.
- On compte toutes ces transitions pour construire une grande matrice 19x19.

**Ce que le script fait :**

- Il affiche une matrice où chaque case (i, j) donne la probabilité qu’une commune passe de la position i à la position j d’un jour à l’autre.
- Il affiche une “carte de chaleur” (heatmap) pour visualiser la stabilité ou la volatilité du classement.

**Exemple imagé :**

> C’est comme suivre le classement d’une ligue de football : la matrice te dit si les équipes (communes) gardent leur place ou changent souvent de rang d’un match à l’autre.

![export matrice 19x19.png](.attachments.1649050/image.png)

![matrice19_19_1week.png](.attachments.1649050/matrice19_19_1week.png)

---

## **Résumé visuel**

- **HMM par commune** : Découvrir les phases cachées dans chaque commune.
- **GMM/EM** : Regrouper les jours similaires sans tenir compte du temps.
- **Prédiction intra-commune** : Tester si le modèle peut prévoir la suite dans une même commune.
- **Transférabilité inter-communes** : Tester si ce qu’on a appris sur une commune marche ailleurs.
- **Matrice 19x19** : Voir comment les communes changent de place dans le classement des cas.

---

## 7. **Perspectives d’amélioration**

- **Automatisation de l’analyse sur toutes les communes**.
- **Ajout de variables explicatives** (mobilité, météo, mesures sanitaires…).
- **Test d’autres modèles** (changepoint detection, modèles non-gaussiens…).
- **Création d’un notebook interactif** pour l’exploration pédagogique.
- **Analyse de la causalité ou de la propagation spatiale** (si données de mobilité disponibles).
- **Validation croisée et robustesse statistique**.

---

## 8. **Points positifs et négatifs**

### **Points positifs**

- Données nettoyées, standardisées, robustes.
- Méthodes mathématiques avancées (HMM, GMM, EM, BIC).
- Validation des modèles (prédiction, RMSE).
- Analyse spatiale (matrice 19x19).
- Scripts interactifs, adaptables, bien documentés.

### **Points négatifs**

- Les modèles restent descriptifs : la prédiction pure reste limitée.
- Pas d’intégration de variables explicatives externes.
- La matrice 19x19 ne modélise pas explicitement la propagation (juste le classement).
- Les résultats dépendent de la qualité et de la granularité des données.
- Peu d’analyse de la robustesse statistique (validation croisée, incertitude…).

---

## **Conclusion**

Le projet a évolué d’un simple nettoyage et lissage de données à une analyse mathématique avancée, avec modélisation probabiliste, validation, et analyse spatiale.  
Les outils mis en place permettent d’explorer la dynamique de l’épidémie à l’échelle des communes, de comparer différentes approches, et d’ouvrir la voie à des analyses encore plus poussées.

---