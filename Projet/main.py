from gestion_lumens import ajuster_lumens
from utils.logger import log_info, log_warning, log_error
import requests
from config import METEO_API_URL, API_WEATHER_KEY

def get_weather_data():
    """Récupérer les données météo depuis l'API OpenWeather."""
    try:
        response = requests.get(METEO_API_URL, params={"q": "Paris", "appid": API_WEATHER_KEY, "units": "metric"})
        response.raise_for_status()
        data = response.json()
        # Extraire les informations utiles : température et météo
        temperature = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        log_info(f"Données météo récupérées : Température = {temperature}°C, Météo = {weather}")
        return temperature, weather
    except requests.exceptions.RequestException as e:
        log_error(f"Erreur lors de la récupération des données météo : {e}")
        return None, None

def main():
    log_info("Lancement du programme.")
    
    while True:
        # Demander à l'utilisateur s'il veut utiliser l'API ou un mode test
        mode = input("Souhaitez-vous utiliser l'API météo ou un mode test (API/test) ? ").strip().lower()
        
        if mode == "api":
            temperature, weather = get_weather_data()
            if temperature is None or weather is None:
                print("Erreur lors de la récupération des données météo. Veuillez vérifier les logs.")
                return
            # Utilisation de la température et de la météo pour ajuster les lumens (ici en fonction de la météo)
            saison = "été" if "clear" in weather else "hiver"  # Exemple de logique simple pour déterminer la saison
            print(f"Saison déterminée par l'API : {saison}")
            presence = int(input("Présence (0/1) : "))
        elif mode == "test":
            # Mode test
            presence = int(input("Présence (0/1) : "))
            saison = input("Saison (hiver/printemps/été/automne) : ").strip().lower()
        else:
            print("Mode non reconnu. Veuillez entrer 'API' ou 'test'.")
            continue

        # Ajuster les lumens
        lumens = ajuster_lumens(presence, saison)
        print(f"Lumens recommandés : {lumens}")
        log_info(f"Présence: {presence}, Saison: {saison}, Lumens recommandés: {lumens}")

if __name__ == "__main__":
    main()
