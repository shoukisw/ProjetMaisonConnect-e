import time
import logging
from datetime import datetime, timedelta
import pandas as pd
import config
from gestion_lumens import ajuster_lumens  # Import de la fonction depuis gestion_lumens
from simulation.simulation import simulate_weather, simulate_presence  # Import de simulate_presence et simulate_weather

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Log dans un fichier
log_file = "generate/app.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)  # Enregistre les logs à partir du niveau INFO
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Log dans la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Log uniquement les messages WARNING et plus importants dans la console
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Ajouter les handlers au logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

excel_file = "generate/fichier_output.xlsx"

def main():
    last_fetch_date = datetime.today().date() - timedelta(days=1)  # Initialisation
    weather_data = None

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        logger.debug(f"Heure actuelle avant traitement : {current_time}")

        if should_fetch_weather(last_fetch_date):
            weather_data = simulate_weather()  # Utilisation de simulate_weather pour récupérer la météo
            last_fetch_date = datetime.today().date()

        # Appel à la fonction pour simuler la présence
        presence = simulate_presence()
        
        # Appel de la fonction ajuster_lumens avec la présence simulée
        lumens = ajuster_lumens(presence, None)  # Remplacer 'None' par ton modèle si nécessaire
        logger.info(f"💡 Luminosité ajustée : {lumens}")

        data = {"Date": [datetime.now()], "Présence": [presence], "Lumens": [lumens]}
        df = pd.DataFrame(data)
        df.to_excel(excel_file, index=False)
        logger.info(f"Fichier Excel mis à jour : {excel_file}")

        logger.info(f"--------Fin de l'ajustement--------")

        time.sleep(6) 

def should_fetch_weather(last_fetch_date):
    today = datetime.today().date()
    return last_fetch_date != today

if __name__ == "__main__":
    main()
