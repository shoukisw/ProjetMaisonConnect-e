from simulation.meteo import get_weather  # Ajout de l'import de get_weather
import sys
import os
import requests
import config 
import logging
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))  # Ajoute le dossier 'Projet' au chemin

# Configuration du logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_weather():
    """
    Cette fonction récupère les données météorologiques via l'API OpenWeather.
    """
    try:
        city = "Paris"  # Ou une autre ville
        url = f"{config.METEO_API_URL}?q={city}&appid={config.API_WEATHER_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            logger.info(f"Données météo récupérées pour {city}: {weather_data}")
            return weather_data
        else:
            logger.error(f"Erreur API météo : {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Impossible de récupérer les données météorologiques : {e}")
        return None

def simulate_weather():
    """
    Cette fonction appelle get_weather pour récupérer les données de l'API météo.
    """
    weather_data = get_weather()
    if weather_data:
        logger.info("Météo récupérée avec succès.")
        return weather_data
    else:
        logger.error("Impossible de récupérer la météo.")
        return None

def simulate_presence():
    """
    Fonction pour simuler la présence d'une personne.
    Retourne 1 pour présence et 0 pour absence.
    """
    presence = random.choice([0, 1])  # Retourne 0 (absence) ou 1 (présence) aléatoirement
    logger.info(f"Présence simulée : {'Présence' if presence else 'Absence'}")
    return presence
