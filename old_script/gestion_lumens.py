import paho.mqtt.client as mqtt
import numpy as np
import pandas as pd
import os
import time
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Configuration du broker MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_LUMENS = "maison/lumens"
TOPIC_COMMANDES = "maison/commande"
TOPIC_PRESENCE = "maison/presence"

# Initialisation du client MQTT
client = mqtt.Client()

# Chargement ou création du dataset
fichier_donnees = "historique_lumens.csv"
if os.path.exists(fichier_donnees):
    historique = pd.read_csv(fichier_donnees)
else:
    historique = pd.DataFrame(columns=["Heure", "Présence", "Lumens"])

# Entraînement du modèle IA si on a assez de données
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
        print(f"⚠ Erreur de connexion MQTT. Code : {rc}")

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

# Ajuste la luminosité en fonction de la présence avec des transitions douces
def ajuster_lumens(presence):
    heure_actuelle = datetime.now().hour

    if presence == 0:
        lumens = 0  # Si personne, la lumière est éteinte
    else:
        if modele_lumens:
            lumens = modele_lumens.predict([[heure_actuelle, presence]])[0]
        else:
            lumens = 250  # Valeur par défaut plus réaliste

        # Limiter la variation brutale des lumens
        lumens = max(100, min(300, lumens))

    print(f"💡 Ajustement - Heure : {heure_actuelle}h | Présence : {presence} | Lumens : {lumens}")
    
    client.publish(TOPIC_LUMENS, lumens)

    # Sauvegarde des données
    nouvelle_donnee = pd.DataFrame([[heure_actuelle, presence, lumens]], columns=["Heure", "Présence", "Lumens"])
    historique.loc[len(historique)] = nouvelle_donnee.values[0]
    historique.to_csv(fichier_donnees, index=False)

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Simulation de l'ajout de données toutes les 5 secondes
while True:
    heure_actuelle = datetime.now().hour
    presence = np.random.choice([1, 0], p=[0.7, 0.3])  # Simule une présence aléatoire

    ajuster_lumens(presence)
    
    time.sleep(5)
