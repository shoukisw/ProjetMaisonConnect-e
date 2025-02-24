import logging

def get_weather(city="Paris"):
    url = f"{config.METEO_API_URL}?q={city}&appid={config.API_WEATHER_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        if weather_data.get("cod") == 200:
            logging.debug(f"Données météo récupérées pour {city}: {weather_data}")
            return weather_data
        else:
            logging.debug(f"Erreur dans la réponse de l'API météo pour {city}.")
            return None
    except requests.exceptions.RequestException as e:
        logging.debug(f"Erreur lors de la récupération des données météo: {e}")
        return None
