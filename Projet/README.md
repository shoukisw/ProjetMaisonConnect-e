# Projet Maison Connectée

Ce projet a pour objectif d'ajuster l'éclairage d'une maison en fonction de la météo, de la présence des utilisateurs et de la saison. Il utilise l'API OpenWeather pour récupérer les données météo, ajuste les lumens d'éclairage en fonction de la météo et logue toutes les actions dans un fichier, tout en générant un fichier Excel avec les ajustements effectués.

## Fonctionnalités

- Récupération des données météo depuis l'API OpenWeather.
- Ajustement de l'éclairage en fonction de la météo (nuages, saison) et de la présence des utilisateurs.
- Logging des ajustements d'éclairage et des erreurs éventuelles dans un fichier `app.log`.
- Sauvegarde des ajustements dans un fichier Excel `fichier_output.xlsx`.
- Le projet vérifie les conditions météo toutes les 10 minutes, et si les données sont manquantes ou erronées, des avertissements sont loggés.
- Les fichiers générés par le programme (logs et fichier Excel) sont stockés dans le dossier `generate`.

## Prérequis

- Python 3.8 ou supérieur
- Bibliothèques suivantes (elles seront installées à l'aide du fichier `requirements.txt`)

## Installation

1. Clonez le projet :
   ```bash
   git clone https://votre-url.git
   cd connected_home/Projet

## Utilisation

Créez un environnement virtuel (si ce n'est pas déjà fait) :

python3 -m venv venv
source venv/bin/activate  # sur Linux/macOS
venv\Scripts\activate     # sur Windows


installer les dependances: 

pip install -r requirements.txt

Ajoutez votre clé API OpenWeather dans le fichier config.py :

API_WEATHER_KEY = "votre_clé_api_openweathermap"
METEO_API_URL = "https://api.openweathermap.org/data/2.5/weather"


lancer le projet :

python main.py

