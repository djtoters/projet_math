import json
from datetime import datetime, timedelta

# Nom du fichier source
filename = "Covid19CleanChanged3.json"
# Nom du fichier de sortie
output_filename = "Updated_Covid19_Data.json"

# Lire les données depuis le fichier
with open(filename, 'r') as file:
    data = json.load(file)

# Liste des communes de Bruxelles
communes = [
    "Anderlecht", "Auderghem", "Berchem-Sainte-Agathe", "Bruxelles", "Etterbeek",
    "Evere", "Forest (Bruxelles-Capitale)", "Ganshoren", "Ixelles", "Jette",
    "Koekelberg", "Molenbeek-Saint-Jean", "Saint-Gilles", "Saint-Josse-ten-Noode",
    "Schaerbeek", "Uccle", "Watermael-Boitsfort", "Woluwe-Saint-Lambert", "Woluwe-Saint-Pierre"
]

# Convertir les dates en objets datetime
for item in data:
    item["DATE"] = datetime.strptime(item["DATE"], "%Y-%m-%d")

# Trouver la plage de dates
dates = [item["DATE"] for item in data]
start_date = min(dates)
end_date = max(dates)

# Générer les dates manquantes pour chaque commune
updated_data = []
for single_date in (start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)):
    for commune in communes:
        if not any(item["DATE"] == single_date and item["TX_DESCR_FR"] == commune for item in data):
            updated_data.append({"NIS5": "", "DATE": single_date, "TX_DESCR_FR": commune, "CASES": "0"})
        else:
            # Ajouter les données existantes pour cette date et cette commune
            existing_entry = next((item for item in data if item["DATE"] == single_date and item["TX_DESCR_FR"] == commune), None)
            if existing_entry:
                updated_data.append(existing_entry)

# Trier les données mises à jour par date
updated_data.sort(key=lambda x: x["DATE"])

# Convertir les dates en chaînes de caractères pour le format JSON
for item in updated_data:
    item["DATE"] = item["DATE"].strftime("%Y-%m-%d")

# Enregistrer les données mises à jour dans un nouveau fichier JSON
with open(output_filename, 'w') as file:
    json.dump(updated_data, file, indent=4)

# Confirmation de la fin du processus
print(f"Les données ont été mises à jour et enregistrées dans le fichier '{output_filename}'.")
