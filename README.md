# MathCovidHMM
<h2>Projet de groupe dans le cadre du cours de mathématique appliqué à l'informatique.</h2>

<h3>
Nos consignes:<br>
<h4>sur base du modèle d'optimisation des chaines de markov à variables cachées, <br>
utilisez l'algorithme EM pour génerer des matrices de transition pour un graphe à<br>
19 sommets (communes de bxl), en utilisant les données du fichier Json.
</h4>
</h3>

<h3>Qu'est ce que le hidden markov model ?</h3>
<img src='./img/1-hmm.png' width=70%> <br>
Un processus de Markov est un processus stochastique dans lequel la distribution de probabilité conditionnelle d'un état futur dépend uniquement de l'état actuel et, étant donné l'état actuel, il est conditionnellement indépendant du passé. Un modèle de Markov caché (HMM) est une extension dans laquelle la séquence d'états est latente et est révélée indirectement via un mécanisme probabiliste. En d'autres termes, un HMM est un processus stochastique doublement imbriqué avec une dynamique stochastique sous-jacente (par exemple, l'état de sévérité de la pandémie de COVID-19 dans une région géographique ou un état) qui, bien qu'inobservable (caché), peut être inféré par l'observation d'un autre ensemble de processus stochastiques liés (par exemple, les taux d'infection, les décès). Les HMM fournissent l'appareillage théorique nécessaire pour apprendre un modèle probabiliste à partir des données ; et en permettant à un HMM d'analyser les observations du COVID-19 dans une région, il est possible d'estimer quel état de sévérité caractérise actuellement celle-ci, et également de prédire l'évolution la plus probable de l'état de sévérité au fil du temps.

<br>

Nous avons commencé par un fichier excel relatant tous les cas d'infection en Belgique
sur une période du `01-03-2020` au `03-04-2021`.
Le fichier était pollué de données inutiles sachant que nous devions nous concentrer
sur les 19 communes de Bruxelles.<br>
Voici à quoi ressemblait le fichier excel initial:<br>
<img src='./img/2-fichierInitial.png' width=70%> <br>

<br>

<h3>Etape 1: Traitement des données</h3>

Nous avons nettoyé les données pour n'avoir que ce dont
nous avions besoin. <br>
<img src='./img/3-donneesV1.png' width=70%> <br>

<br>
Puis nous avons remplacé tous les <5 par des 2. En dessous de 5
voulait dire un nombre de cas proche de 0 donc pour ne pas trop
off set les données, nous avons choisi en dessous de la médiane.
Et avons obtenu ceci: <br>
<img src='./img/4-donnesV2.png' width=70%> <br>

Ce dernier fichier excel a ensuite été transformé en fichier Json intitulé `Covid19CleanChanged3.json`.
Celui-ci n'était pas encore complet et utilisable.
Il nous manquait encore les données des jours où il y avait 0 cas
par commune. Celles-ci n'étant pas présentent, nous avons écrit un script
pour remplir les trous. A chaque jour où une commune n'apparaîssait pas, celle-ci se voyait
ajoutée au fichier Json et attribué un nombre de cas covid de 0.
<br>

Le script utilisé est le `updateJson.py`
Ceci nous donne notre `Updated_Covid19_Data.json`:


<img src="./img/5-donneesV3.png" width="70%">

<br>

En nous basant sur plusieurs articles que nous avons lus, l'approche générale est de
standardiser les données. Nous avons donc multiplié le nombre de cas de chaque commune par 10 000
et divisé chacun de ces nombres par la population respective de celles-ci.
Voici les différentes populations: <br>
"Anderlecht": 121723

"Auderghem": 34543

"Berchem-Sainte-Agathe": 24113

"Bruxelles": 186784

"Etterbeek": 48672

"Evere": 42693

"Forest (Bruxelles-Capitale)": 56866

"Ganshoren": 25206

"Ixelles": 87517

"Jette": 52952

"Koekelberg": 22168

"Molenbeek-Saint-Jean": 97637

"Saint-Gilles": 49662

"Saint-Josse-ten-Noode": 27050

"Schaerbeek": 131892

"Uccle": 84188

"Watermael-Boitsfort": 25202

"Woluwe-Saint-Lambert": 58040

"Woluwe-Saint-Pierre": 42038

Ces chiffres ont été obtenues via : https://ibsa.brussels/chiffres/chiffres-cles-de-la-region

<br>

Grâce au script `standart.py`, nous obtenons donc un fichier Json presque utilisable intitulé:
`Standardized_Covid19_data10K.json` <br>
Nous avions aussi fait le test en prenant le nombre de cas par 100 000 mais nous obtenions des nombres 
de cas par jour trop farfelus. <br>
Nous obtenons donc des graphiques avec `GraphStandardised3.py` comme ceci : <br>
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Anderlecht.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Auderghem.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Berchem-Sainte-Agathe.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Bruxelles.png" width="25%">
<br>
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Etterbeek.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Evere.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Forest_(Bruxelles-Capitale).png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Ganshoren.png" width="25%">
<br>
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Ixelles.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Jette.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Koekelberg.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Molenbeek-Saint-Jean.png" width="25%">
<br>
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Saint-Gilles.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Saint-Josse-ten-Noode.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Schaerbeek.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Uccle.png" width="25%">
<br>
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Watermael-Boitsfort.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Woluwe-Saint-Lambert.png" width="25%">
<img src="./Projet/Archive/GraphStandard10KParCommune/COVID19_Woluwe-Saint-Pierre.png" width="25%">

<br>

Une fois les données standardisée, nous devons encore les traiter un peu pour pouvoir les utiliser.
L'algorithme de Hampel, souvent utilisé dans le cadre du filtrage Hampel pour la suppression des valeurs aberrantes (ou "outliers"), est une technique robuste pour identifier et traiter les points anormaux dans des séries de données. Voici une explication simple et détaillée de cet algorithme :

### Fonctionnement de base
1. **Fenêtre glissante** : L'algorithme parcourt les données à l'aide d'une fenêtre glissante de taille configurable. Cela signifie qu'à chaque étape, il considère un sous-ensemble des données autour d'un point central. La taille de cette fenêtre détermine combien de points de données sont pris en compte à chaque étape.

2. **Calcul de la médiane et de l'écart-type robuste** : À l'intérieur de chaque fenêtre, l'algorithme calcule la médiane des données. La médiane est moins sensible aux valeurs extrêmes que la moyenne, ce qui la rend plus robuste. Ensuite, il calcule également une version robustifiée de l'écart-type, qui est une mesure de la dispersion des données autour de la médiane.

3. **Détection des outliers** : Pour chaque point de données dans la fenêtre, l'algorithme vérifie si ce point s'écarte de manière significative de la médiane par rapport à l'écart-type robustifié. Un point est généralement considéré comme aberrant si sa valeur dépasse la médiane de plus d'un certain multiple de l'écart-type robustifié (souvent autour de 2,5 à 3 fois).

4. **Remplacement des outliers** : Si un point est identifié comme un outlier, il est remplacé par la médiane de la fenêtre. Cette méthode de remplacement assure que les données restent lisses et moins affectées par des erreurs sporadiques ou des anomalies.

### Pourquoi utiliser le filtrage Hampel ?
- **Robustesse** : Le filtrage Hampel est particulièrement robuste contre les valeurs aberrantes car il n'utilise pas la moyenne, qui peut être fortement influencée par des valeurs extrêmes.
- **Adaptabilité** : La taille de la fenêtre et le multiple de l'écart-type peuvent être ajustés en fonction de la spécificité des données et du degré de sensibilité aux outliers souhaité.

### Applications typiques
- **Traitement de données temporelles** : Très utilisé pour lisser les séries temporelles où les valeurs aberrantes peuvent fausser les tendances et les analyses, comme les données de trafic, les relevés météorologiques, ou ici, les données liées au COVID-19.
- **Suppression du bruit dans les capteurs ou les mesures** : Idéal pour corriger les erreurs de mesure dans les données capturées par des capteurs.

En résumé, l'algorithme de Hampel est une méthode puissante et flexible pour nettoyer les ensembles de données, en assurant que les résultats des analyses soient fiables et non biaisés par des données anormales. Cela le rend extrêmement utile dans une multitude de contextes où la précision des données est cruciale.

Nous avons fait des tests en changeant de fenêtre, de 7 jours à 28  <br>
Nous sommes partis sur une fenêtre pour Hampel de 7 jours
`hampel2.py` permet de comparer les différentes fenêtres, les graphiques sont disponibles ici: <br>
<a href="https://github.com/Veynah/MathCovidHMM/tree/main/Projet/Archive/GraphHampel2TestWindowSigma3" target="_blank">Graphiques de comparaison de fenêtres</a>

<br>

### La prochaine étape ### 
est le lissage de la courbe. Pour adresser la présence de potentiels problèmes dans 
notre dataset, comme des données manquantes, des délais dans les rapports et dépistages ou des erreurs
d'encodage. Nous lissons les séquences avec un filtre de moyenne mobile (MA) à poids uniformes. <br>

### Qu'est-ce que la Moyenne Mobile (MA) ? ###
La moyenne mobile est une technique statistique utilisée pour analyser des séries de données en créant une série de moyennes de différents sous-ensembles du jeu de données original. C'est essentiellement une façon de lisser les données pour voir les tendances plus clairement, en réduisant l'impact du bruit ou des fluctuations à court terme.


### Pourquoi combiner MA avec Hampel ?
1. **Réduction du bruit** : La moyenne mobile lisse les séries de données en moyennisant les valeurs, ce qui aide à réduire le bruit et à clarifier les tendances sous-jacentes. Cependant, si des valeurs aberrantes extrêmes sont présentes, elles peuvent toujours influencer la moyenne, en particulier dans le cas de la SMA.

2. **Gestion des valeurs aberrantes** : L'algorithme de Hampel est très efficace pour identifier et remplacer les valeurs aberrantes qui pourraient fausser les résultats de la moyenne mobile. En utilisant Hampel avant d'appliquer la moyenne mobile, on peut s'assurer que les moyennes calculées sont basées sur des données plus fiables et représentatives.

3. **Amélioration de la précision des prévisions** : Dans les applications où les prévisions précises sont critiques, comme la finance ou la météorologie, l'ajout de l'étape de filtration Hampel avant le calcul des moyennes mobiles peut améliorer significativement la qualité des prédictions en éliminant les anomalies avant qu'elles n'affectent la moyenne.

<br>

## Hampel et MA ##

En utilisant `hampelMA.py` nous pouvons voir maintenant comment les données sont plus claires, lisses et utilisables maintenant. Notre choix de prendre une fênetre
de 21 jours vient d'un test précédent où nous avions utilisé une fenêtre de 7 jours et entrainé nos hmm dessus.
Nous pouvons comparer les résultats d'une fenêtre de 7 jours à ceux de 21 jours. Quelques exemples: <br>

<h4>7 jours <br>
<img src="./Projet/Archive/GraphHampelMA/COVID19_MA_Bruxelles.png" width="40%">
<img src="./Projet/Archive/GraphHampelMA/COVID19_MA_Schaerbeek.png" width="40%">
<br>
<h4>21 jours</h4>
<img src="./Projet/Code/HampelMA21J/COVID19_MA_Bruxelles.png" width="40%">
<img src="./Projet/Code/HampelMA21J/COVID19_MA_Schaerbeek.png" width="40%">

<br>

Voici tous les graphiques :

<img src="Projet/Code/HampelMA21J/COVID19_MA_Anderlecht.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Auderghem.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Berchem-Sainte-Agathe.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Bruxelles.png" width="25%">
<br>
<img src="Projet/Code/HampelMA21J/COVID19_MA_Etterbeek.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Evere.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Forest_(Bruxelles-Capitale).png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Ganshoren.png" width="25%">
<br>
<img src="Projet/Code/HampelMA21J/COVID19_MA_Ixelles.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Jette.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Koekelberg.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Molenbeek-Saint-Jean.png" width="25%">
<br>
<img src="Projet/Code/HampelMA21J/COVID19_MA_Saint-Gilles.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Saint-Josse-ten-Noode.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Schaerbeek.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Uccle.png" width="25%">
<br>
<img src="Projet/Code/HampelMA21J/COVID19_MA_Watermael-Boitsfort.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Woluwe-Saint-Lambert.png" width="25%">
<img src="Projet/Code/HampelMA21J/COVID19_MA_Woluwe-Saint-Pierre.png" width="25%">

Il faut ensuite transformer ces données en quelque  chose d'utilisable. Grâce à `df_filtered.py` nous pouvons avoir un fichier csv avec des données sur
lesquelles nous pouvons entrainer nos hmm.

Donc avec une fenêtre coulissante de 7 pour Hampel et une moyenne mobile de 21 jours, nous pouvons obtenir de nouvelles données intitulées `CASES_PER_10K_MA`.
Nous avons fait en sorte de n'avoir que 2 chiffres après la virgule pour encore nous débarrasser du bruit et éviter les variations inutiles.

<h4>Fin des traitements de données.</h4> 

<h3>Entrainement de nos modèles HMM</h3>

Nous avons utilisé la librairie hmmlearn qui implémente les hmm's. Comme dit, HMM est un modèle génératif probabiliste où les séquences d'états observables
X sont générées par une séquence d'états internes cachés Z. Les états cachés ne sont pas directement observé. Les transitions entre les états cachés sont présumées
avoir la forme de chaine de Markov.

Nous utilisons les données stockées dans notre fichier csv (CASES_PER_10K_MA) que nous filtrons par commune pour avoir des modèles prédictionnels par communes.
Nous avons des modèles entraînés sur 70% des données et prédisant les 30% restant. Ceux-ci sont les HMMTEST, en voici quelqu'uns : <br>

<h4>Anderlercht</h4>
<img src="./Projet/Code/30/Anderlecht.png" width="40%">
<img src="./Projet/Code/30/COVID19_Anderlecht.png" width="40%">


Matrice de transition entre les états :


<img src="Projet/Code/30/Matrices/Anderlecht.png" width="40%"> <br>
[[9.35235392e-001 0.00000000e+000 6.17084787e-172 4.27034347e-295 3.23912640e-002 0.00000000e+000 3.23733442e-002] <br>
[0.00000000e+000 3.10940054e-001 0.00000000e+000 0.00000000e+000 3.44530003e-001 3.44529944e-001 0.00000000e+000] <br>
[2.87464725e-199 0.00000000e+000 9.05818880e-001 3.14952874e-002 0.00000000e+000 0.00000000e+000 6.26858329e-002] <br>
[4.32399624e-307 0.00000000e+000 2.34808164e-002 9.76519184e-001 0.00000000e+000 0.00000000e+000 2.00618713e-097] <br>
[3.42462955e-002 3.41100424e-002 0.00000000e+000 0.00000000e+000 9.31643662e-001 1.73569596e-069 1.15613464e-188] <br>
[0.00000000e+000 5.86074151e-002 0.00000000e+000 0.00000000e+000 1.61607110e-058 9.41392585e-001 0.00000000e+000] <br>
[1.23401619e-002 0.00000000e+000 1.23049800e-002 1.56708933e-096 4.02641437e-195 0.00000000e+000 9.75354858e-001]] <br>

Moyennes des états : <br>
[[ 2.71290642] <br>
[12.42034892] <br>
[ 0.42710635] <br>
[ 0.13849262] <br>
[ 7.2303799 ] <br>
[15.10802591] <br>
[ 1.25572061]] <br>



<h4>Bruxelles</h4>
<img src="./Projet/Code/30/Bruxelles.png" width="40%">
<img src="./Projet/Code/30/COVID19_Bruxelles.png" width="40%">


Matrice de transition entre les états : <br>
<img src="./Projet/Code/30/Matrices/Bruxelles.png" width="40%"> <br>
[[1.25672574e-003 9.98743266e-001 0.00000000e+000 0.00000000e+000 8.27251294e-009 1.67992905e-024 0.00000000e+000] <br>
[1.89866716e-011 2.19760506e-008 0.00000000e+000 0.00000000e+000 9.35315617e-001 6.46843606e-002 0.00000000e+000] <br>
[0.00000000e+000 0.00000000e+000 9.56175184e-001 2.19072245e-002 0.00000000e+000 6.49265834e-198 2.19175918e-002] <br>
[0.00000000e+000 0.00000000e+000 3.03076442e-002 9.69692356e-001 0.00000000e+000 1.17511144e-072 7.94900410e-199] <br>
[9.96168522e-001 6.70508067e-013 0.00000000e+000 0.00000000e+000 3.83147792e-003 3.39597001e-022 0.00000000e+000] <br>
[3.97959626e-010 1.35850741e-002 3.18158218e-143 1.35563081e-002 1.53724953e-023 9.72858617e-001 0.00000000e+000] <br>
[0.00000000e+000 0.00000000e+000 2.67253521e-002 3.55140598e-199 0.00000000e+000 0.00000000e+000 9.73274648e-001]] <br>

Moyennes des états : <br>
[[ 0.13385575] <br>
[ 0.13906177] <br>
[ 3.14798448] <br>
[ 1.39340444] <br>
[ 0.1336158 ] <br>
[ 0.69809818] <br>
[11.82342908]] <br>



<h4>Etterbeek</h4>
<img src="./Projet/Code/30/Etterbeek.png" width="40%">
<img src="./Projet/Code/30/COVID19_Etterbeek.png" width="40%">


Matrice de transition entre les états : <br>
<img src="./Projet/Code/30/Matrices/Etterbeek.png" width="40%"> <br>
[[9.56560119e-001 0.00000000e+000 0.00000000e+000 1.82623433e-169 0.00000000e+000 4.34398811e-002 4.08906078e-102] <br>
[0.00000000e+000 0.00000000e+000 7.50637770e-146 8.89318163e-323 1.00000000e+000 0.00000000e+000 0.00000000e+000] <br>
[0.00000000e+000 6.20257935e-002 8.75811581e-001 6.21626252e-002 2.87777734e-111 1.62247417e-124 0.00000000e+000] <br>
[3.49777571e-171 1.06535199e-184 6.93794578e-002 8.61083825e-001 1.19616276e-253 6.95367168e-002 0.00000000e+000] <br>
[0.00000000e+000 3.91453186e-157 5.48214594e-002 1.58370006e-166 9.45178541e-001 0.00000000e+000 0.00000000e+000] <br>
[4.69987549e-002 0.00000000e+000 1.41573853e-130 4.70666846e-002 0.00000000e+000 9.05934561e-001 2.89444015e-275] <br>
[5.41399851e-003 0.00000000e+000 0.00000000e+000 0.00000000e+000 0.00000000e+000 2.17635433e-179 9.94586001e-001]] <br>

Moyennes des états : <br>
[[ 1.18639812] <br>
[10.40999815] <br>
[ 7.37356165] <br>
[ 3.73028944] <br>
[12.56237903] <br>
[ 2.01370916] <br>
[ 0.31965054]] <br>



<h4>Schaerbeek</h4>
<img src="./Projet/Code/30/Schaerbeek.png" width="40%">
<img src="./Projet/Code/30/COVID19_Schaerbeek.png" width="40%">


Matrice de transition entre les états : <br>
<img src="./Projet/Code/30/Matrices/Schaerbeek.png" width="40%"> <br>
[[9.68670073e-001 2.63399242e-227 8.56665027e-159 0.00000000e+000 6.83634581e-041 2.68227125e-249 3.13299268e-002] <br>
[0.00000000e+000 3.41059358e-007 0.00000000e+000 0.00000000e+000 1.89545819e-002 9.81045077e-001 0.00000000e+000] <br>
[1.68685201e-174 0.00000000e+000 8.82952150e-001 5.84641480e-002 0.00000000e+000 0.00000000e+000 5.85837017e-002] <br>
[0.00000000e+000 0.00000000e+000 5.24094791e-002 9.47590521e-001 0.00000000e+000 0.00000000e+000 9.50952803e-130] <br>
[3.01294792e-002 1.18968686e-149 0.00000000e+000 0.00000000e+000 9.69870521e-001 2.86556859e-164 5.23248861e-102] <br>
[0.00000000e+000 4.98403881e-001 0.00000000e+000 0.00000000e+000 1.86048355e-011 5.01596119e-001 0.00000000e+000] <br>
[4.79486026e-002 0.00000000e+000 4.79099651e-002 4.07578878e-133 4.02695830e-149 0.00000000e+000 9.04141432e-001]] <br>

Moyennes des états : <br>
[[ 2.28714681] <br>
[ 0.33100403] <br>
[ 8.99931144] <br>
[14.35436265] <br>
[ 1.30987269] <br>
[ 0.31615846] <br>
[ 4.62860202]] <br>

<br>

Nous avons donc entrainé les modèles sur 70% des données et prédis les 30% restant. 
En utilisant un HMM Gaussien avec une covariance `full` et 420 `random state`

### Explications sur les covariances et random states ###

Lors de l'entraînement d'un HMM, le choix du type de covariance pour les distributions de probabilité associées à chaque
état caché est crucial car il définit la manière dont les variables sont corrélées entre elles.

### Les types de `Covariance`

`spherical` : Chaque composante de l'état a sa propre variance unique mais il est assumé qu'il n'y a pas de corrélation entre les composantes. <br>
Toutes les directions de l'espace des caractéristiques ont la même variance. Cela équivaut à une matrice de covariance où la diagonale est remplie <br>
avec une même valeur et les autres éléments sont 0.<br>

`diag` : Chaque composante de l'état a sa propre variance, mais aucune corrélation entre les composantes n'est modélisée. La matrice de covariance est diagonale, <br> 
ce qui signifie que chaque variable a sa propre variance, mais contrairement à "spherical", les variances peuvent différer. <br>

`full` : La matrice de covariance complète est utilisée, permettant de modéliser les variances de chaque composante ainsi que les <br>
covariances entre chaque paire de composantes. Cela permet une modélisation plus flexible mais augmente considérablement le nombre de paramètres à estimer. <br>

`tied` : Tous les composants partagent la même matrice de covariance globale. Cela signifie qu'une seule matrice de covariance est utilisée pour toutes les <br>
distributions des états, ce qui réduit le nombre de paramètres par rapport à "full", tout en permettant une certaine corrélation entre les variables. <br>

### Signification de `Random State`
Le `random_state` est un paramètre qui contrôle la génération aléatoire de nombres pour l'initialisation des algorithmes qui ont une composante stochastique.
Voici quelques points clés :

- **Reproductibilité** : Fournir un entier à `random_state` permet de s'assurer que les résultats sont reproductibles. Cela signifie que chaque fois que vous exécutez votre code avec le même `random_state`, vous obtiendrez exactement les mêmes résultats.
- **Initialisation** : Dans les HMM, `random_state` peut affecter l'initialisation des paramètres du modèle, comme les probabilités de transition ou les paramètres des distributions de probabilité pour les états cachés.
- **Utilisation pratique** : Fixer le `random_state` est utile pour le débogage et pour assurer que les variations dans les résultats du modèle sont dues à des changements dans les données ou les paramètres du modèle, et non à des différences dans l'initialisation aléatoire.


### Comment interpréter ces résultats 

### Matrice de Transition Entre les États

**Etterbeek** <br>
<img src="./Projet/Code/30/Matrices/Etterbeek.png" width="40%"> <br>

La matrice de transition fournit les probabilités de passer d'un état à un autre. Chaque ligne de la matrice représente un état source, et chaque colonne un état cible. Les éléments de la matrice donnent la probabilité de transition d'un état à l'autre. Voici comment comprendre votre matrice :

- **Diagonale Principale (par exemple, `9.56560119e-001` pour l'état 1)**: Ces valeurs élevées sur la diagonale principale indiquent que chaque état a une forte probabilité de persister au jour suivant. Par exemple, l'état 1 a environ 95.66% de chances de rester dans cet état le jour suivant.

- **Valeurs Hors Diagonale**: Ces valeurs indiquent la probabilité de transitionner d'un état à un autre. Par exemple, l'état 1 a une probabilité de `4.34398811e-002` (environ 4.34%) de passer à l'état 6.

- **Zéros et Valeurs très faibles (comme `1.82623433e-169`)**: Ces valeurs indiquent une probabilité presque nulle de transition entre certains états, montrant qu'il est très peu probable, voire impossible, de passer directement de ces états à d'autres spécifiques.

### Moyennes des États

**Etterbeek** <br>
[[ 1.18639812] <br>
[10.40999815] <br>
[ 7.37356165] <br>
[ 3.73028944] <br>
[12.56237903] <br>
[ 2.01370916] <br>
[ 0.31965054]] <br>

Les moyennes des états indiquent la valeur moyenne observée lorsque le système est dans un état particulier. Ces moyennes peuvent vous aider à comprendre le "comportement" ou les caractéristiques de chaque état :

- **État 1 (`1.18639812`)** : Cet état pourrait représenter des jours avec un faible nombre de cas (si vous analysez des données sur les infections, par exemple).
- **État 2 (`10.40999815`), État 5 (`12.56237903`)** : Ces états avec des moyennes élevées peuvent indiquer des jours avec un nombre élevé de cas.
- **État 7 (`0.31965054`)** : Cet état avec la moyenne la plus basse pourrait indiquer des jours avec très peu ou aucun cas.

### Interprétation Générale

- **Stabilité vs Changement**: Une matrice avec de fortes probabilités sur la diagonale et des valeurs basses hors diagonale suggère un modèle où les états sont assez stables jour après jour, avec occasionnellement des transitions significatives.
- **Dynamique des Transitions**: Les transitions qui sont possibles mais peu probables (valeurs basses mais non nulles) indiquent que certains changements d'état, bien que rares, sont possibles.


<h3>Conclusion</h3>

Ce projet a fourni une analyse amateur de la propagation du Covid19 à Bruxelles à un niveau microscopique (par commune), en utilisant des techniques statistiques avancées
pour décoder les tendances cachées derrière les données brutes. Les résultats, bien que pas tout le temps précis ou correctes, ont montré que certaines communes
présentent des dynamiques de propagation distinctes et que les modèles HMM peuvent être des outils précieux pour prévoir les changements dans les tendances
de la maladie, en supposant que les conditions restent constantes.

Ces analyses et modélisations peuvent aider les professionnels à mieux comprendre et à réagir aux épidémies, en mettant en oeuvre des interventions ciblées
basées sur les prévisions et modèles et analyse des états passés.

<br>

<h4>Travaux et articles sur lesquels nous avons basé notre projet:</h4> <br>
https://hmmlearn.readthedocs.io/en/latest/auto_examples/plot_poisson_hmm.html#sphx-glr-auto-examples-plot-poisson-hmm-py <br>
https://hmmlearn.readthedocs.io/en/latest/tutorial.html#training-hmm-parameters-and-inferring-the-hidden-states <br>
https://medium.com/@natsunoyuki/hidden-markov-models-with-python-c026f778dfa7 <br>
https://kth.diva-portal.org/smash/get/diva2:1428900/FULLTEXT01.pdf <br>
https://www.mathworks.com/help/dsp/ref/hampelfilter.html <br>
https://qiniu.pattern.swarma.org/pdf/arxiv/2008.07609.pdf <br>
https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9543670 <br>
https://www.sciencedirect.com/science/article/pii/S2352864822001067
[14:55] <br>
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7461001/ <br>
