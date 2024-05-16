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


df = pd.read_csv('Folium Map FINAL - Feuille 1.csv')

def create_map():
    m = folium.Map(location=[4.74851, -6.6363], zoom_start=12)
    
    # Create a MarkerCluster layer
    marker_cluster = MarkerCluster().add_to(m)
    
    for index, row in df.iterrows():
        iframe_content = (
            f"<b>Entreprenant:</b> {row['Entreprenant/Display Name']} <br><br>"
            f"<b>Contact:</b> {row['Bon numéro de téléphone']} <br><br>"
            f"<b>Nom de l'activité:</b> {row['Denomination_ou_raison_sociale']} <br>"
            f"<b>Date de naissance:</b> {row['Entreprenant/Date de naissance']} <br>"
            f"<b>Nature de l'activité:</b> {row['Type_activite']} <br><br>"
            f"<b>Chiffre d'affaire:</b> {row['chiffre_affaire']} <br>"
            f"<b>Taille de l'activité:</b> {row['taille_activite']} <br>"
        )

        popup = folium.Popup(iframe_content, min_width=300, max_width=300)

        if row['Etat'] == "Annulé/Rejeté":
            marker_color = 'red'
        elif row['Etat'] == "Confirmé":
            marker_color = 'orange'
        elif row['Etat'] == "Validé":
            marker_color = 'green'
        else:
            marker_color = 'gray'

        # Add the marker to the MarkerCluster layer
        folium.Marker(location=[row['Géolatitude'], row['Géolongitude']], icon=folium.Icon(color=marker_color, icon='map-marker', prefix='fa'), popup=popup).add_to(marker_cluster)

    return m

map = create_map()   
folium_static(map, width=750)

