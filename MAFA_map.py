import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Load data
df = pd.read_csv('Folium Map FINAL - Feuille 1.csv')

# Initial map creation
@st.cache
def create_map():
    m = folium.Map(location=[4.74851, -6.6363], zoom_start=12)
    return m

def add_markers(map_obj, data):
    for _, row in data.iterrows():
        # Create marker
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
        
        folium.Marker(location=[row['Géolatitude'], row['Géolongitude']], icon=folium.Icon(color=marker_color, icon='map-marker', prefix='fa'), popup=popup).add_to(map_obj)

# Get map object
map = create_map()

# Initial data for map
data = df.iloc[:100]
add_markers(map, data)

# Display map
folium_static(map, width=750)

# JavaScript code to detect map movement and send new bounds to the server
st.write("""
    <script>
        const map = document.getElementsByClassName('leaflet-map')[0];
        map.addEventListener('moveend', function() {
            const bounds = map.getBounds();
            const params = {
                'north': bounds.getNorth(),
                'south': bounds.getSouth(),
                'east': bounds.getEast(),
                'west': bounds.getWest()
            };
            // Send parameters to server
            google.colab.kernel.invokeFunction('update_map', [params], {});
        });
    </script>
""")

# Server-side function to update the map
@st.cache(allow_output_mutation=True)
def update_map(params):
    north = params['north']
    south = params['south']
    east = params['east']
    west = params['west']
    # Fetch data based on new bounds (north, south, east, west)
    # Update map with new data
    # Clear previous map
    map.clear_layers()
    # Add new markers to the map based on the new bounds
    new_data = df[(df['Géolatitude'] >= south) & (df['Géolatitude'] <= north) & (df['Géolongitude'] >= west) & (df['Géolongitude'] <= east)]
    add_markers(map, new_data)
    # Display updated map
    folium_static(map, width=750)

# Invoke server-side function to update map when JavaScript sends new bounds
if 'update_map' in st.session_state:
    update_map(st.session_state.update_map)
