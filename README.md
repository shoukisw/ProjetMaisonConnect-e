# Projet Maison Connectée

## Description

Ce projet permet de gérer l'éclairage d'une maison en ajustant les lumens des ampoules en fonction de la présence des utilisateurs et des saisons. Il utilise un modèle d'apprentissage automatique pour ajuster la luminosité en fonction de ces paramètres.

Le programme offre deux modes d'utilisation :

- **Mode API** : Utilise l'API OpenWeather pour récupérer les données météo en temps réel et ajuste les lumens en fonction de la météo.
- **Mode Test** : Permet de tester le programme localement en simulant la présence et la saison.

## Fonctionnalités

- **Récupération des données météo** : En mode API, le programme récupère les informations météo actuelles pour Paris via l'API OpenWeather et ajuste les lumens en fonction de la météo.
- **Simulation de la saison et de la présence** : En mode test, l'utilisateur peut entrer manuellement la saison et la présence pour ajuster la luminosité.
- **Modèle d'apprentissage automatique** : Utilise un modèle de régression linéaire pour prédire la luminosité idéale en fonction de la saison et de la présence.

## Prérequis

Assurez-vous que les packages suivants sont installés :

- `requests` : pour interagir avec l'API météo.
- `sklearn` : pour l'apprentissage automatique.
- `joblib` : pour charger et sauvegarder le modèle d'apprentissage.
- `pandas` : pour manipuler les données.

## Installation

Clonez ce repository et installez les dépendances :

```bash 
git clone <url_du_repertoire>
cd <nom_du_repertoire>
```

Créez un environnement virtuel 

Il est recommandé de créer un environnement virtuel pour isoler les dépendances du projet. Pour ce faire, utilisez les commandes suivantes :

Si vous utilisez venv :

```bash 
python3 -m venv venv
```

Ensuite, activez l'environnement virtuel :

```bash 
source venv/bin/activate
```
Cela permet de travailler dans un environnement isolé, garantissant que les dépendances n'entrent pas en conflit avec d'autres projets.

```bash 
pip install -r requirements.txt
```

## Utilisation

# Lancer le programme

Il est important d'entrainer le modéle IA avant de lancer main.py : 

```bash
python3 training.py
```

Ensuite exécutez le fichier main.py : 

```bash
python3 main.py
```

## Choisir un mode
Lors du lancement du programme, vous pouvez choisir entre deux modes :

Mode API : Le programme récupère les données météo en temps réel depuis l'API OpenWeather.

Mode Test : Le programme vous permet de simuler la présence et la saison pour ajuster les lumens.
Mode API
En mode API, le programme détermine la saison en fonction de la description de la météo (par exemple, si le temps est clair, il considère que c'est l'été). Vous pouvez ajuster la luminosité en fonction de la météo réelle à Paris.

# Mode Test
En mode test, vous entrez manuellement la saison et la présence pour simuler l'ajustement des lumens.

Exemple d'exécution en mode API

```bash
Souhaitez-vous utiliser l'API météo ou un mode test (API/test) ? api
Saison déterminée par l'API : été
Présence (0/1) : 1
Lumens recommandés : 500
```
Exemple d'exécution en mode Test

```bash
Souhaitez-vous utiliser l'API météo ou un mode test (API/test) ? test
Présence (0/1) : 1
Saison (hiver/printemps/été/automne) : été
Lumens recommandés : 500
```

## Modèle d'Apprentissage
Le modèle d'apprentissage est basé sur un modèle de régression linéaire qui prédit les lumens en fonction de la saison et de la présence. Le modèle est formé à l'aide des données disponibles dans le fichier fichier_output.xlsx et est enregistré sous le nom modele_lumens.pkl.

# Fichiers Générés

modele_lumens.pkl : Le modèle d'apprentissage prédit les valeurs de luminosité.

fichier_output_with_predictions.xlsx : Le fichier Excel mis à jour avec les prédictions de luminosité pour chaque combinaison de présence et saison.

generate/log/log.txt : Le fichier log où toutes les informations et erreurs sont enregistrées.

generate/app.log : Le fichier log détaillant l'exécution du programme.

