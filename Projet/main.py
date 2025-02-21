import time
import os
import logging
import requests
import json
from datetime import datetime, timedelta
import config
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

log_file = "generate/app.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

excel_file = "generate/fichier_output.xlsx"

def get_weather():
    try:
        url = f"{config.METEO_API_URL}?q=Paris&appid={config.API_WEATHER_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        # Vérification de la présence des données météo nécessaires
        if 'clouds' not in weather_data:
            logger.warning("Données météo manquantes : 'clouds' non trouvé dans la réponse.")
            weather_data['clouds'] = {'all': 0} 

        logger.info(f"Météo récupérée avec succès : {weather_data}")
        return weather_data
    except requests.exceptions.HTTPError as err:
        logger.error(f"Erreur météo : {err}")
        return None

# Fonction pour ajuster l'éclairage (dépend de la météo)
def adjust_lighting(presence, model, weather_data):
    saison = datetime.now().month  
    nuages = weather_data['clouds']['all']  
    lumens = model.predict([[presence, saison, nuages]]) if model else 200 
    current_hour = datetime.now().hour  
    logger.info(f"Ajustement lumière - Heure : {current_hour}h | Présence : {presence} | Saison : {'hiver' if saison in range(12, 3) else 'été'} | Nuages : {nuages}% | Lumens : {lumens}")
    return lumens

def main():
    last_fetch_date = datetime.today().date() - timedelta(days=1)  # Définir initialement à un jour précédent
    weather_data = None

    while True:
        # Log de l'heure avant chaque boucle pour vérifier que l'heure change
        current_time = datetime.now().strftime("%H:%M:%S")
        logger.info(f"Heure actuelle avant traitement : {current_time}")

        if should_fetch_weather(last_fetch_date):
            weather_data = get_weather()
            last_fetch_date = datetime.today().date()

        presence = 1  
        lumens = adjust_lighting(presence, None, weather_data)

        # Affichage de l'ajustement de la lumière
        logger.info(f"💡 Luminosité ajustée : {lumens}")

        data = {"Date": [datetime.now()], "Présence": [presence], "Lumens": [lumens]}
        df = pd.DataFrame(data)
        df.to_excel(excel_file, index=False)
        logger.info(f"Fichier Excel mis à jour : {excel_file}")

        time.sleep(600)  # Attente (en secondes)

# Vérifie si la météo a déjà été récupérée aujourd'hui
def should_fetch_weather(last_fetch_date):
    today = datetime.today().date()
    return last_fetch_date != today

if __name__ == "__main__":
    main()
