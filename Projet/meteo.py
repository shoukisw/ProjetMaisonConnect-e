import requests

# Remplace par ton API clé et URL
API_KEY = "ta_cle_api"
CITY = "Paris"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        cloud_coverage = data['clouds']['all']  # En pourcentage de couverture nuageuse
        return temperature, cloud_coverage
    else:
        print("⚠️ Erreur de récupération des données météo")
        return None, None
