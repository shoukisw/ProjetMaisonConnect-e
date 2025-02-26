import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

data_path = os.path.join("data", "fichier_output.xlsx")  # Chemin des données
output_dir = os.path.join("generate")  # Chemin où enregistrer le modèle et les fichiers générés
os.makedirs(output_dir, exist_ok=True)  # Créer le dossier 'generate' s'il n'existe pas

model_path = os.path.join(output_dir, "modele_lumens.pkl")  # Chemin où sauvegarder le modèle
output_file = os.path.join(output_dir, "fichier_output_with_predictions.xlsx")  # Chemin du fichier Excel

df = pd.read_excel(data_path)
expected_columns = {'presence', 'saison', 'lumens'}
if not expected_columns.issubset(df.columns):
    raise ValueError(f"Colonnes trouvées : {df.columns.tolist()}. Attendu : {expected_columns}")

df["saison"] = df["saison"].astype("category").cat.codes  # Encode les saisons en chiffres

X = df[['presence', 'saison']]
y = df['lumens']

modele_lumens = LinearRegression()
modele_lumens.fit(X, y)

joblib.dump(modele_lumens, model_path)
print(f"✅ Modèle enregistré dans {model_path}")

df['predicted_lumens'] = modele_lumens.predict(X)

df.to_excel(output_file, index=False)
print(f"✅ Données mises à jour enregistrées dans {output_file}")
