import requests
from config import METEO_API_URL, API_WEATHER_KEY
from utils.logs import log_error, log_info

def obtenir_meteo(ville="Paris"):
    try:
        response = requests.get(f"{METEO_API_URL}?q={ville}&appid={API_WEATHER_KEY}&units=metric")
        response.raise_for_status()
        data = response.json()
        log_info(f"Météo récupérée avec succès : {data}")
        return data
    except requests.exceptions.RequestException as e:
        log_error(f"Erreur météo : {e}")
        return None
