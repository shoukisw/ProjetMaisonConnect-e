import paho.mqtt.client as mqtt
import numpy as np
import pandas as pd
import os
import time
import pytz
from datetime import datetime
from astral import LocationInfo
from astral.sun import sun
from sklearn.linear_model import LinearRegression
import requests

# Configuration du broker MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_LUMENS = "maison/lumens"
TOPIC_COMMANDES = "maison/commande"
TOPIC_PRESENCE = "maison/presence"

# Localisation (modifiable selon la région)
VILLE = "Paris"
PAYS = "France"
LAT = 48.8566
LON = 2.3522
API_KEY = "your_openweathermap_api_key"  # Remplacez par votre propre clé API OpenWeatherMap
TZ = pytz.timezone("Europe/Paris")

# Définition de la localisation
lieu = LocationInfo(VILLE, PAYS, TZ.zone, LAT, LON)

# Initialisation du client MQTT
client = mqtt.Client()

# Chargement ou création du dataset
fichier_donnees = "historique_lumens.csv"
if os.path.exists(fichier_donnees):
    historique = pd.read_csv(fichier_donnees)
else:
    historique = pd.DataFrame(columns=["Heure", "Présence", "Lumens", "Saison"])

# Définir la saison actuelle
def obtenir_saison(date):
    mois = date.month
    if mois in [12, 1, 2]: return "hiver"
    if mois in [3, 4, 5]: return "printemps"
    if mois in [6, 7, 8]: return "été"
    if mois in [9, 10, 11]: return "automne"
    return "inconnu"

# Entraînement du modèle IA
def entrainer_model():
    if len(historique) < 10:
        print("⚙️ Modèle IA - Pas assez de données pour entraîner l'IA...")
        return None
    X = historique[["Heure", "Présence"]].values
    y = historique["Lumens"].values
    model = LinearRegression()
    model.fit(X, y)
    print("🤖 Modèle IA entraîné avec succès !")
    return model

modele_lumens = entrainer_model()

# Fonction pour récupérer les données météo
def get_weather():
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()
        
        # Vérification de la présence de la clé 'clouds' dans la réponse
        if 'clouds' in data:
            cloud_coverage = data['clouds']['all']  # En pourcentage de couverture nuageuse
        else:
            print("⚠️ Données météo manquantes : 'clouds' non trouvé dans la réponse.")
            cloud_coverage = 0  # Par défaut, aucune couverture nuageuse
    except Exception as e:
        print(f"⚠️ Erreur de récupération des données météo : {e}")
        cloud_coverage = 0  # Par défaut, aucune couverture nuageuse
    
    return cloud_coverage

# Gestion de la connexion MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connecté à MQTT Broker !")
        client.subscribe(TOPIC_COMMANDES)
        client.subscribe(TOPIC_PRESENCE)
    else:
        print(f"⚠️ Erreur de connexion MQTT. Code : {rc}")

# Réception des commandes MQTT
def on_message(client, userdata, message):
    global modele_lumens
    commande = message.payload.decode()
    print(f"📩 Commande reçue : {commande}")

    if commande == "entrainement":
        modele_lumens = entrainer_model()
    elif commande.startswith("presence:"):
        _, valeur = commande.split(":")
        presence = int(valeur)
        ajuster_lumens(presence)

# Calcul du niveau de lumière nécessaire en fonction du soleil, saison et météo
def ajuster_lumens(presence):
    now = datetime.now(TZ)
    saison = obtenir_saison(now)

    # Calcul du lever et coucher du soleil
    soleil = sun(lieu.observer, date=now, tzinfo=TZ)
    lever = soleil["sunrise"].hour
    coucher = soleil["sunset"].hour
    heure_actuelle = now.hour

    # Déterminer s'il fait jour ou nuit
    journee = "jour" if lever <= heure_actuelle < coucher else "nuit"

    # Récupérer les données météo
    cloud_coverage = get_weather()

    # Ajustement basé sur la saison, la luminosité extérieure et la couverture nuageuse
    if presence == 0:
        lumens = 0  # Si personne, la lumière est éteinte
    else:
        if modele_lumens:
            lumens = modele_lumens.predict([[heure_actuelle, presence]])[0]
        else:
            lumens = 150  # Valeur par défaut

        # Appliquer des ajustements saisonniers
        if journee == "jour":
            if saison == "été":
                lumens *= 0.3  # Réduction car il fait jour longtemps
            elif saison == "hiver":
                lumens *= 0.8  # Besoin de plus de lumière

        # Appliquer un ajustement basé sur la couverture nuageuse
        lumens = lumens * (1 + (cloud_coverage / 100))  # Augmenter ou diminuer les lumens selon les nuages

        # Éviter des valeurs trop extrêmes
        lumens = max(50, min(200, lumens))

    print(f"💡 Ajustement - Heure : {heure_actuelle}h | Présence : {presence} | Saison : {saison} | Nuages : {cloud_coverage}% 🌥️ | Lumens : {lumens} 💡")
    
    client.publish(TOPIC_LUMENS, lumens)

    # Sauvegarde des données
    nouvelle_donnee = pd.DataFrame([[heure_actuelle, presence, lumens, saison]], columns=["Heure", "Présence", "Lumens", "Saison"])
    historique.loc[len(historique)] = nouvelle_donnee.values[0]
    historique.to_csv(fichier_donnees, index=False)

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Simulation toutes les 5 secondes
while True:
    heure_actuelle = datetime.now(TZ).hour
    presence = np.random.choice([1, 0], p=[0.7, 0.3])  # Simule une présence aléatoire

    ajuster_lumens(presence)
    
    time.sleep(5)
