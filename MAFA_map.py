import pandas as pd
import mysql.connector as connection
from operator import attrgetter
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import folium
from streamlit_folium import st_folium
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster


df = pd.read_csv('COPIE ID30 - Feuille 1.csv')

df['Géolatitude'] = pd.to_numeric(df['Géolatitude'], errors='coerce')
df['Géolongitude'] = pd.to_numeric(df['Géolongitude'], errors='coerce')

# Filter out rows where either 'Géolatitude' or 'Géolongitude' is NaN
df = df.dropna(subset=['Géolatitude', 'Géolongitude'])

unique_activities = df['Quelle est votre activité principale actuelle?'].unique()

selected_activities = st.multiselect('Sélectionnez un type d'activité:', unique_activities)

if selected_activities:
    df = df[df['Quelle est votre activité principale actuelle?'].isin(selected_activities)]
else:
    df = df  # If no activity is selected, display the entire DataFrame


def create_map():
    m = folium.Map(location=[4.74851, -6.6363], zoom_start=12)
    
    # Create a MarkerCluster layer
    marker_cluster = MarkerCluster(maxClusterRadius=1).add_to(m)

    color_map = {
    "VENTE SUR ETAL": 'green',
    "RESTAURANT/MAQUIS/BAR/BUVETTE/CAVE": 'orange',
    "COUTURE": 'red',
    "VENTE DE VETEMENTS / CHAUSSURES / ACCESSOIRES DE MODE": 'blue',
    "COIFFURE / COSMETIQUES / BEAUTE": 'purple',
    "VENTE D'ARTICLES DIVERS": 'pink',
    "MECANIQUE / GARAGE AUTO": 'brown',
    "VIRIERS / LOGODOUGOU": 'yellow',
    "DEFAULT": 'gray'  # Couleur par défaut
    }
    
    for index, row in df.iterrows():
        iframe_content = (
            f"<b>Entreprenant:</b> {row['Entreprenant/Display Name']} <br><br>"
            f"<b>Contact:</b> {row['Bon numéro de téléphone']} <br><br>"
            f"<b>Nom de l'activité:</b> {row['Dénomination ou raison sociale']} <br>"
            f"<b>Nature de l'activité:</b> {row['Quelle est votre activité principale actuelle?']} <br><br>"
            f"<b>Chiffre d'affaire:</b> {row['Unp bon CA']} <br>"
        )

        popup = folium.Popup(iframe_content, min_width=300, max_width=300)

        activity = row['Quelle est votre activité principale actuelle?']
        marker_color = color_map.get(activity, color_map['DEFAULT'])
        
        # Add the marker to the MarkerCluster layer
        folium.Marker(location=[row['Géolatitude'], row['Géolongitude']], 
                      icon=folium.Icon(color= marker_color, icon='map-marker', prefix='fa'), 
                      popup=popup).add_to(marker_cluster)

    return m

map = create_map()   
folium_static(map, width=750)

