import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Charger le modèle
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# Charger le scaler (si disponible)
try:
    with open("scaler.pkl", "rb") as file:
        scaler = pickle.load(file)
except FileNotFoundError:
    scaler = None

# 📌 Définition des catégories
categories = ["Veste Homme", "Meches", "Soulier", "Parfums", "Chemise", "Creme de beauté"]
mois_list = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
             "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
jours_list = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
evenements_list = ["Aucun", "Noel", "Vacance", "Rentrée scolaire", "Fêtes"]

# 📌 Interface utilisateur Streamlit
st.title("🛒 Prédiction des Ventes 📈")

# 📌 Entrée des données utilisateur
categorie_produit = st.selectbox("Catégorie du produit", categories)
prix = st.number_input("Prix du produit (en GNF)", min_value=0, value=150000, step=1000)
promotion = st.radio("Produit en promotion ?", ["Non", "Oui"])
evenement_special = st.selectbox("Événement spécial", evenements_list)
jour_semaine = st.selectbox("Jour de la semaine", jours_list)
mois = st.selectbox("Mois", mois_list)
trafic_site = st.number_input("Trafic sur le site web", min_value=0, value=45453, step=100)

# 📌 Conversion des valeurs en indices pour le modèle
categorie_produit_index = categories.index(categorie_produit)
jour_semaine_index = jours_list.index(jour_semaine)
mois_index = mois_list.index(mois)
evenement_special_index = evenements_list.index(evenement_special)
promotion_value = 1 if promotion == "Oui" else 0

# 📌 Création du DataFrame pour la prédiction
data = pd.DataFrame([{
    "categorie_produit": categorie_produit_index,
    "prix": prix,
    "promotion": promotion_value,
    "evenement_special": evenement_special_index,
    "jour_semaine": jour_semaine_index,
    "mois": mois_index,
    "trafic_site": trafic_site
}])

# 📌 Normalisation (si un scaler est disponible)
if scaler:
    data_scaled = scaler.transform(data)
else:
    data_scaled = data  # Utiliser les données non normalisées si pas de scaler

# 📌 Bouton de prédiction
if st.button("📊 Prédire les ventes"):
    prediction = model.predict(data_scaled)
    st.subheader(f"📢 Prédiction des ventes : {int(prediction[0])} unités")
