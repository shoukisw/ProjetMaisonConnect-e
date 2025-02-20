from sklearn.linear_model import LinearRegression
import pandas as pd

def entrainer_model(historique):
    if len(historique) < 10:
        print("📊 Pas assez de données pour entraîner l'IA...")
        return None
    X = historique[["Heure", "Présence"]].values
    y = historique["Lumens"].values
    model = LinearRegression()
    model.fit(X, y)
    print("🤖 Modèle IA entraîné avec succès !")
    return model
