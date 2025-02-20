import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_LUMENS = "maison/lumens"
TOPIC_COMMANDES = "maison/commande"
TOPIC_PRESENCE = "maison/presence"

client = mqtt.Client()

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
    print(f"📩 Commande reçue : {message.payload.decode()}")

def publish_lumens(lumens):
    client.publish(TOPIC_LUMENS, lumens)

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
