import json

# Chemin vers le fichier JSON original
chemin_original = "Updated_Covid19_Data.json"

# Chemin vers le nouveau fichier JSON
chemin_nouveau = "oneLineCovidData.json"

# Lire les données du fichier original
with open(chemin_original, "r") as fichier:
    data = json.load(fichier)

# Écrire les données dans le nouveau fichier, avec chaque objet sur une ligne
with open(chemin_nouveau, "w") as nouveau_fichier:
    for element in data:
        # Écrire chaque objet JSON sur une seule ligne
        json.dump(element, nouveau_fichier)
        nouveau_fichier.write(
            "\n"
        )  # Nouvelle ligne après chaque objet pour la lisibilité
