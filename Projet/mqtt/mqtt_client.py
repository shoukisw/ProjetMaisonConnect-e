import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

def on_connect(client, userdata, flags, rc):
    print(f"Connexion au broker MQTT : Code de retour {rc}")
    client.subscribe("home/lights")

def on_message(client, userdata, msg):
    print(f"Message reçu sur {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER, PORT, 60)
    print("Connecté à MQTT avec succès.")
except Exception as e:
    print(f"Erreur de connexion à MQTT : {e}")

client.loop_start()
