import joblib
import sys
import os
from utils.logger import log_info, log_error

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Charger le modèle
model_path = os.path.join("generate", "modele_lumens.pkl")
if not os.path.exists(model_path):
    log_error(f"Le fichier {model_path} est introuvable. Lance `training.py` pour l'entraîner.")
    raise FileNotFoundError(f"Le fichier {model_path} est introuvable. Lance `training.py` pour l'entraîner.")

modele_lumens = joblib.load(model_path)
log_info("Modèle chargé avec succès.")

def ajuster_lumens(presence, saison):
    """ Prédit la luminosité idéale en fonction de la présence et de la saison. """
    try:
        saison_encoded = ["hiver", "printemps", "été", "automne"].index(saison)  # Encode la saison
        prediction = modele_lumens.predict([[presence, saison_encoded]])[0]
        lumens = max(0, int(prediction))  # Évite les valeurs négatives
        
        log_info(f"Prédiction : Présence={presence}, Saison={saison}, Lumens={lumens}")
        return lumens
    except Exception as e:
        log_error(f"Erreur dans ajuster_lumens : {e}")
        return 0
