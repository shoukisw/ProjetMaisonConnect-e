import paho.mqtt.client as mqtt
from config import BROKER_ADDRESS
from utils.logs import log_info

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    log_info("✅ Connecté à MQTT Broker !")

client.on_connect = on_connect
client.connect(BROKER_ADDRESS)
client.loop_start()
