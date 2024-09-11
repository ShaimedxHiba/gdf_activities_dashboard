import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from streamlit_folium import st_folium
import folium

# Read Excel file
@st.cache_data
def load_data():
    data = pd.read_csv('data/seed_distribution.csv')
    return data

   

# Function to display charts and map
def seed_distribution():
    st.title("Seed Distribution Program")
    data = load_data()

    st.write("### Data Preview:")
    st.dataframe(data.head())
    
    
    data.columns = data.columns.str.strip()
    # Visualize data (e.g. Bar plot for different crops)
    st.write("### Crop Distribution Chart")
    fig, ax = plt.subplots(figsize=(10, 6))
    data.groupby('Douar').sum()[['Barley', 'Faba Beans', 'Peas', 'Carrots', 'Turnip']].plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # Filter out rows with missing coordinates
    filtered_data = data.dropna(subset=['Latitude', 'Longitude'])

    # Leaflet Map
    st.write("### Seed Distribution Map")
    map_center = [filtered_data['Latitude'].mean(), filtered_data['Longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=8)

    # Add markers for each village
    for _, row in filtered_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Douar']} - Farmers Benefited: {row['Farmers Benefited']}"
        ).add_to(m)

    # Display the map
    st_data = st_folium(m, width=700, height=500)



