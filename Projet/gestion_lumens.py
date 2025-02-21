import pandas as pd
import os
from utils.utils import obtenir_saison
from utils.logs import log_info

fichier_donnees = "historique_lumens.csv"
historique = pd.read_csv(fichier_donnees) if os.path.exists(fichier_donnees) else pd.DataFrame(columns=["Heure", "Présence", "Lumens", "Saison"])


def ajuster_lumens(presence, modele_lumens):
    saison = obtenir_saison()
    
    if isinstance(saison, str):
        saison_mapping = {"hiver": 0, "printemps": 1, "été": 2, "automne": 3}
        saison = saison_mapping.get(saison, 0)  # Assigner une valeur numérique à la saison

        data = pd.DataFrame([[presence, saison]], columns=["Présence", "Saison"])
    
    lumens = modele_lumens.predict(data) if modele_lumens else 0
    log_info(f"Ajustement lumière : {lumens} lumens pour {saison}")
    return lumens
