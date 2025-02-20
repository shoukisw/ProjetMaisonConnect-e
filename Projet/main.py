import time
import gestion_lumens
import mqtt_client
import model
import os
import pandas as pd
 
historique = pd.read_csv("historique_lumens.csv") if os.path.exists("historique_lumens.csv") else pd.DataFrame(columns=["Heure", "Présence", "Lumens", "Saison"])

modele_lumens = model.entrainer_model(historique)

mqtt_client.client.loop_start()

# Simulation toutes les 5 secondes
while True:
    presence = 1  # Simule une présence
    lumens = gestion_lumens.ajuster_lumens(presence, modele_lumens)
    time.sleep(5)
