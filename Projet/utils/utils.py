from datetime import datetime

def obtenir_saison(date=None):
    if date is None:
        date = datetime.now()
    mois = date.month
    if mois in [12, 1, 2]:
        return "hiver"
    elif mois in [3, 4, 5]:
        return "printemps"
    elif mois in [6, 7, 8]:
        return "été"
    else:
        return "automne"
