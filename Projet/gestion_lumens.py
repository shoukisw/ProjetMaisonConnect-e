import pandas as pd
import os
import joblib  # Import de joblib pour charger le modèle
from utils.utils import obtenir_saison
from utils.logs import log_info

fichier_donnees = "historique_lumens.csv"
historique = pd.read_csv(fichier_donnees) if os.path.exists(fichier_donnees) else pd.DataFrame(columns=["Heure", "Présence", "Lumens", "Saison"])

# Charger le modèle
modele_lumens = joblib.load('modele_lumens.pkl')

def ajuster_lumens(presence, modele_lumens):
    """
    Ajuste les lumens en fonction de la présence, de la saison et du modèle de prédiction.

    Args:
        presence (int): 1 si une personne est présente, 0 sinon.
        modele_lumens: Le modèle de prédiction des lumens.

    Returns:
        int: La valeur des lumens ajustée.
    """
    saison = obtenir_saison()

    if isinstance(saison, str):
        saison_mapping = {"hiver": 0, "printemps": 1, "été": 2, "automne": 3}
        saison = saison_mapping.get(saison, 0)  # On attribue une valeur numérique à la saison
        data = pd.DataFrame([[presence, saison]], columns=["Présence", "Saison"])
    
    # Utilisation du modèle pour prédire les lumens
    if modele_lumens:
        lumens = modele_lumens.predict(data)[0]  # Récupérer la première prédiction (modèle de régression)
    else:
        lumens = 0  # Valeur par défaut si pas de modèle

    # Log de l'ajustement des lumens
    log_info(f"Ajustement des lumières: {lumens} lumens pour la saison {saison}")

    # Enregistrer dans l'historique
    historique.loc[len(historique)] = [pd.Timestamp.now(), presence, lumens, saison]
    historique.to_csv(fichier_donnees, index=False)

    return lumens
