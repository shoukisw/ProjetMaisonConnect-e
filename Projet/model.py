import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

df = pd.read_excel('ton_fichier.xlsx')

# Préparer les données (X = features, y = variable cible)
X = df[['presence', 'saison']]  # Exemple de colonnes à utiliser
y = df['lumens']  # La colonne cible (luminosité)

# Entraîner le modèle
modele_lumens = LinearRegression()
modele_lumens.fit(X, y)

joblib.dump(modele_lumens, 'modele_lumens.pkl')

df['predicted_lumens'] = modele_lumens.predict(X)

df.to_excel('fichier_mis_a_jour.xlsx', index=False)
