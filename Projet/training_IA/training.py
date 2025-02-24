import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import joblib

# Charger le fichier de données
df = pd.read_excel('fichier_output.xlsx')

# Initialiser le LabelEncoder pour encoder la saison
encoder = LabelEncoder()
df['saison'] = encoder.fit_transform(df['saison'])  # Convertir les saisons en nombres

# Préparer les données (X = features, y = variable cible)
X = df[['presence', 'saison']]  # Variables indépendantes
y = df['lumens']  # Variable cible (luminosité)

# Créer et entraîner le modèle
modele_lumens = LinearRegression()
modele_lumens.fit(X, y)

# Sauvegarder le modèle dans un fichier .pkl
joblib.dump(modele_lumens, 'modele_lumens.pkl')

# (Optionnel) Prédire les lumens avec le modèle et enregistrer les résultats dans un nouveau fichier
df['predicted_lumens'] = modele_lumens.predict(X)
df.to_excel('fichier_mis_a_jour.xlsx', index=False)

print("Modèle entraîné et sauvegardé dans 'modele_lumens.pkl'")
