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

# Configuration du broker MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_LUMENS = "maison/lumens"
TOPIC_COMMANDES = "maison/commande"
TOPIC_PRESENCE = "maison/presence"

# Localisation (modifiable selon la région)
VILLE = "Paris"
PAYS = "France"
TZ = pytz.timezone("Europe/Paris")

# Définition de la localisation
lieu = LocationInfo(VILLE, PAYS, TZ.zone, 48.8566, 2.3522)

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
    if mois in [12, 1, 2]: 
        return "hiver"
    elif mois in [3, 4, 5]: 
        return "printemps"
    elif mois in [6, 7, 8]: 
        return "été"
    elif mois in [9, 10, 11]: 
        return "automne"
    else:
        return "inconnu"

# Entraînement du modèle IA
def entrainer_model():
    if len(historique) < 10:
        print("📊 Pas assez de données pour entraîner l'IA...")
        return None
    X = historique[["Heure", "Présence"]].values
    y = historique["Lumens"].values
    model = LinearRegression()
    model.fit(X, y)
    print("🤖 Modèle IA entraîné avec succès !")
    return model

modele_lumens = entrainer_model()

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

# Calcul du niveau de lumière nécessaire en fonction du soleil et de la saison
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

    # Ajustement basé sur la saison et la luminosité extérieure
    if presence == 0:
        lumens = 0  # Si personne, la lumière est éteinte
    else:
        if modele_lumens:
            lumens = modele_lumens.predict([[heure_actuelle, presence]])[0]
        else:
            lumens = 250  # Valeur par défaut

        # Appliquer des ajustements saisonniers
        if journee == "jour":
            if saison == "été":
                lumens *= 0.3  # Réduction car il fait jour longtemps
            elif saison == "hiver":
                lumens *= 0.8  # Besoin de plus de lumière

        # Éviter des valeurs trop extrêmes
        lumens = max(50, min(300, lumens))

    print(f"💡 Ajustement - Heure : {heure_actuelle}h | Présence : {presence} | Saison : {saison} | Lumens : {lumens}")
    
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
    presence = np.random.choice([1, 0], p=[0.7, 0.3])  # Simule une présence aléatoire
    ajuster_lumens(presence)
    time.sleep(5)
