from datetime import datetime
import logging

logger = logging.getLogger()

def obtenir_saison(date=None):
    if date is None:
        date = datetime.now()
    
    logger.debug(f"📅 Date analysée : {date}")  # Debug
    mois = date.month
    
    if mois in [12, 1, 2]:
        saison = "hiver"
    elif mois in [3, 4, 5]:
        saison = "printemps"
    elif mois in [6, 7, 8]:
        saison = "été"
    else:
        saison = "automne"
    
    logger.debug(f"🌍 Saison détectée : {saison}")  # Debug
    return saison
