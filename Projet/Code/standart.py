import json

# Chemin du fichier d'entrée et de sortie
input_file = "Updated_Covid19_data.json"
output_file = "Standardized_Covid19_data10K.json"

# Données de population pour chaque commune
population_data = {
    "Anderlecht": 121723,
    "Auderghem": 34543,
    "Berchem-Sainte-Agathe": 24113,
    "Bruxelles": 186784,
    "Etterbeek": 48672,
    "Evere": 42693,
    "Forest (Bruxelles-Capitale)": 56866,
    "Ganshoren": 25206,
    "Ixelles": 87517,
    "Jette": 52952,
    "Koekelberg": 22168,
    "Molenbeek-Saint-Jean": 97637,
    "Saint-Gilles": 49662,
    "Saint-Josse-ten-Noode": 27050,
    "Schaerbeek": 131892,
    "Uccle": 84188,
    "Watermael-Boitsfort": 25202,
    "Woluwe-Saint-Lambert": 58040,
    "Woluwe-Saint-Pierre": 42038,
}

# Chargement des données JSON depuis le fichier d'entrée
with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Préparation de la liste pour les données standardisées
standardized_data = []

# Calcul du nombre de cas pour 10 000 habitants pour chaque enregistrement
for record in data:
    commune_name = record["TX_DESCR_FR"]
    if commune_name in population_data:
        population = population_data[commune_name]
        # Calcul des cas par 10k habitants
        cases_per_10k = (int(record["CASES"]) / population) * 10000
        # Création d'un nouveau dictionnaire pour les données standardisées
        standardized_record = record.copy()
        standardized_record["CASES_PER_10K"] = cases_per_10k
        standardized_data.append(standardized_record)

# Sauvegarde des données standardisées dans le fichier de sortie
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(standardized_data, file, ensure_ascii=False, indent=4)

# Message de confirmation
print(f"Les données ont été standardisées et enregistrées dans '{output_file}'.")
