import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

# Load the Excel data
@st.cache_data
def load_data():
    

    # Load both sheets from the Excel file
    watermills = pd.read_excel('data/chp.xlsx', sheet_name='Watermills')
    irrigation = pd.read_excel('data/chp.xlsx', sheet_name='Irrigation basins and canals')
    springs = pd.read_excel('data/chp.xlsx', sheet_name='Springs')
    terraces = pd.read_excel('data/chp.xlsx', sheet_name='Agricultural terraces')
    shelters= pd.read_excel('data/chp.xlsx', sheet_name='Nomadic shelters')
    granaries = pd.read_excel('data/chp.xlsx', sheet_name='Granaries')  
    return  watermills,irrigation,springs,terraces,shelters,granaries

    
   
def chp():
    # Insert custom CSS for styling
    st.markdown(
        """
        <style>
        /* Custom style for the title */
        .title {
            color: #FF6347; /* Tomato color */
            font-size: 32px; /* Custom font size */
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }

        /* Custom style for section titles */
        .section-title {
            font-size: 28px;
            color: #4CAF50; /* Green */
            font-weight: bold;
            margin-top: 40px;
            margin-bottom: 10px;
        }

        /* Custom style for introduction text */
        .intro-text {
            font-size: 20px;
            color: #555555;
            margin-bottom: 30px;
            text-align: center;
        }
        .text {
            font-size: 18px;
            color: #555555;
            margin-bottom: 30px;
            
        }
        /* Adjust the padding around the content */
        .block-container {
            padding: 2rem 1rem;
        }
        /* Custom style for stats */
        .stats-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 30px;
        }
        .stat {
            text-align: center;
            font-size: 20px;
            color: #333;
            margin: 10px;
            flex: 1 1 200px;
            max-width: 200px;
        }
        .stat-number {
            font-size: 36px;
            font-weight: bold;
            color: #FF6347;
        }
        </style>
        """, unsafe_allow_html=True
    )
    # Load data
    watermills, irrigation, springs, terraces, shelters, granaries = load_data()
#Introduction
    st.markdown('<div class="title">Cultural Heritage Sites</div>', unsafe_allow_html=True)
   # st.markdown('<div class="intro-text">Intro to cultural heritage sites importance in the High Atlas</div>', unsafe_allow_html=True)
    # Display the number of sites for each category
    total_watermills = watermills.shape[0]
    total_irrigation = irrigation.shape[0]
    total_springs = springs.shape[0]
    total_terraces = terraces.shape[0]
    total_shelters = shelters.shape[0]
    total_granaries = granaries.shape[0]

    # Create a container for the stats
    stats_html = f'''
    <div class="stats-container">
        <div class="stat">
            <div class="stat-number">{total_watermills}</div>
            Watermills
        </div>
        <div class="stat">
            <div class="stat-number">{total_irrigation}</div>
            Irrigation Systems
        </div>
        <div class="stat">
            <div class="stat-number">{total_springs}</div>
            Springs
        </div>
        <div class="stat">
            <div class="stat-number">{total_terraces}</div>
            Terraces
        </div>
        <div class="stat">
            <div class="stat-number">{total_shelters}</div>
            Nomadic Shelters
        </div>
        <div class="stat">
            <div class="stat-number">{total_granaries}</div>
            Granaries
        </div>
    </div>
    '''

    st.markdown(stats_html, unsafe_allow_html=True)
#Watermills
    # Section for watermills
    st.markdown('<div class="section-title">Watermills</div>', unsafe_allow_html=True)
    st.markdown('<div class="text">Importance of watermills</div>', unsafe_allow_html=True)

    # Reorder columns to place 'Douar' first and remove 'Name', 'Douar_ID', and 'Pictures'
    watermills = watermills[['Douar', 'Latitude', 'Longitude', 'Commune', 'Ownership Status', 'Water Source', 
                             'Water Flow', 'Structural Integrity', 'Douars Benefiting', 'Estimated Cost', 'Notes']]
    
    
    # Create columns for filters (50% width each)
    col1, col2, col3 = st.columns([1, 1, 1])  

    with col1:
        douar_filter = st.text_input("Search by Douar", key='watermill_douar')
    with col2:
        commune_filter = st.text_input("Search by Commune", key='watermill_commune')
    with col3:
        benefiting_filter = st.text_input("Search by Douars Benefiting", key='watermill_benefiting')
       
    col1, col2 = st.columns([1, 1])  
    with col1:
        ownership_filter = st.text_input("Search by Ownership Status", key='watermill_ownership')
    with col2:    
        structural_filter = st.text_input("Search by Structural Integrity", key='watermill_structural')

    
    # Apply filters to watermills data
    filtered_watermills = watermills.copy()

    if douar_filter:
         filtered_watermills = filtered_watermills[filtered_watermills['Douar'].str.contains(douar_filter, case=False, na=False)]
    if commune_filter:
        filtered_watermills = filtered_watermills[filtered_watermills['Commune'].str.contains(commune_filter, case=False, na=False)]
    if ownership_filter:
        filtered_watermills = filtered_watermills[filtered_watermills['Ownership Status'].str.contains(ownership_filter, case=False, na=False)]
    if benefiting_filter:
        filtered_watermills = filtered_watermills[filtered_watermills['Douars Benefiting'].str.contains(benefiting_filter, case=False, na=False)]
    if structural_filter:
        filtered_watermills = filtered_watermills[filtered_watermills['Structural Integrity'].str.contains(structural_filter, case=False, na=False)]

    # Display the filtered data
    st.dataframe(filtered_watermills, hide_index=True)

    # Display map only for rows with valid coordinates
    valid_coords = filtered_watermills.dropna(subset=['Latitude', 'Longitude'])
    
    if not valid_coords.empty:
        # Create the map centered at the average location of the watermills
        m = folium.Map(location=[valid_coords['Latitude'].mean(), valid_coords['Longitude'].mean()], zoom_start=8)

        # Add markers to the map for each watermill
        for _, row in valid_coords.iterrows():
            popup_content = (
                f"<b>Douar:</b> {row['Douar']}<br>"
                f"<b>Commune:</b> {row['Commune']}<br>"
                f"<b>Ownership:</b> {row['Ownership Status']}<br>"
                f"<b>Structural Integrity:</b> {row['Structural Integrity']}<br>"
            )
        
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_content, max_width=300),
            ).add_to(m)
        
        # Display the map
        folium_static(m)
    else:
        st.write("No valid coordinates available for the selected filters.")
#Irrigation bains and canals
    # Section for irrigation systems
    st.markdown('<div class="section-title">Irrigation basins and canals</div>', unsafe_allow_html=True)
    st.markdown('<div class="text">Importance of irrigation basins and canals</div>', unsafe_allow_html=True)
    
    # Reorder columns to place 'Douar' after 'Type' and remove 'Pictures'
    irrigation = irrigation[['Type', 'Douar', 'Latitude', 'Longitude', 'Commune', 'Douars Benefiting', 
                             'Terraces/Hectares Covered', 'Reservoir Water Capacity', 'Water Source', 
                             'Estimated Cost', 'Structural Integrity', 'Notes']]
    
    # Create columns for filters (50% width each)
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        douar_filter = st.text_input("Search by Douar", key='irrigation_douar')       
    with col2:
        commune_filter = st.text_input("Search by Commune", key='irrigation_commune')      
    with col3:
        benefiting_filter = st.text_input("Search by Douars Benefiting", key='irrigation_benefiting')
       
    col1, col2 = st.columns([1, 1])  
    with col1:
        type_filter = st.text_input("Search by Type", key='irrigation_type')
    with col2:
        structural_filter = st.text_input("Search by Structural Integrity", key='irrigation_structural')

    # Apply filters to irrigation data
    filtered_irrigation = irrigation

    # Apply each filter only if the corresponding input is not empty
    if type_filter:
         filtered_irrigation = filtered_irrigation[filtered_irrigation['Type'].str.contains(type_filter, case=False, na=False)]

    if douar_filter:
         filtered_irrigation = filtered_irrigation[filtered_irrigation['Douar'].str.contains(douar_filter, case=False, na=False)]

    if commune_filter:
        filtered_irrigation = filtered_irrigation[filtered_irrigation['Commune'].str.contains(commune_filter, case=False, na=False)]

    if benefiting_filter:
        filtered_irrigation = filtered_irrigation[filtered_irrigation['Douars Benefiting'].str.contains(benefiting_filter, case=False, na=False)]

    if structural_filter:
        filtered_irrigation = filtered_irrigation[filtered_irrigation['Structural Integrity'].str.contains(structural_filter, case=False, na=False)]
 
    
    # Display the filtered data
    st.dataframe(filtered_irrigation, hide_index=True)

    # Display map only for rows with valid coordinates
    valid_coords = filtered_irrigation.dropna(subset=['Latitude', 'Longitude'])
    
    if not valid_coords.empty:
        # Create the map centered at the average location of the irrigation systems
        m = folium.Map(location=[valid_coords['Latitude'].mean(), valid_coords['Longitude'].mean()], zoom_start=8)

        # Add markers to the map for each irrigation system
        for _, row in valid_coords.iterrows():
            popup_content = (
                f"<b>Douar:</b> {row['Douar']}<br>"
                f"<b>Commune:</b> {row['Commune']}<br>"
                f"<b>Type:</b> {row['Type']}<br>"
            )

            # Only add 'Structural Integrity' if it's not NaN
            if pd.notna(row['Structural Integrity']):
                popup_content += f"<b>Structural Integrity:</b> {row['Structural Integrity']}<br>"

            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_content, max_width=300),
            ).add_to(m)

        # Display the map
        folium_static(m)
    else:
        st.write("No valid coordinates available for the selected filters.")
#Springs
    # Section for springs
    st.markdown('<div class="section-title">Springs</div>', unsafe_allow_html=True)
    st.markdown('<div class="text">Importance of springs</div>', unsafe_allow_html=True)
    
    # Reorder columns to place 'Douar' after 'Type' and remove 'Pictures'
    springs = springs[['Douar', 'Latitude', 'Longitude', 'Commune', 'Douars Benefiting',  
                       'Estimated Cost', 'Structural Integrity', 'Notes']]
    
    # Create columns for filters (50% width each)
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        douar_filter = st.text_input("Search by Douar", key='springs_douar')       
    with col2:
        commune_filter = st.text_input("Search by Commune", key='springs_commune')      
    with col3:
        benefiting_filter = st.text_input("Search by Douars Benefiting", key='springs_benefiting')
       
    col1, col2 = st.columns([1, 1])  
   
    with col1:
        structural_filter = st.text_input("Search by Structural Integrity", key='springs_structural')

    # Apply filters to irrigation data
    filtered_springs = springs

    # Apply each filter only if the corresponding input is not empty
    
    if douar_filter:
         filtered_springs = filtered_springs[filtered_springs['Douar'].str.contains(douar_filter, case=False, na=False)]

    if commune_filter:
        filtered_springs = filtered_springs[filtered_springs['Commune'].str.contains(commune_filter, case=False, na=False)]

    if benefiting_filter:
        filtered_springs = filtered_springs[filtered_springs['Douars Benefiting'].str.contains(benefiting_filter, case=False, na=False)]

    if structural_filter:
        filtered_springs = filtered_springs[filtered_springs['Structural Integrity'].str.contains(structural_filter, case=False, na=False)]
 
    
    # Display the filtered data
    st.dataframe(filtered_springs, hide_index=True)

    # Display map only for rows with valid coordinates
    valid_coords = filtered_springs.dropna(subset=['Latitude', 'Longitude'])
    
    if not valid_coords.empty:
        # Create the map centered at the average location of the irrigation systems
        m = folium.Map(location=[valid_coords['Latitude'].mean(), valid_coords['Longitude'].mean()], zoom_start=8)

        # Add markers to the map for each irrigation system
        for _, row in valid_coords.iterrows():
            popup_content = (
                f"<b>Douar:</b> {row['Douar']}<br>"
                f"<b>Commune:</b> {row['Commune']}<br>"
                
            )

            # Only add 'Structural Integrity' if it's not NaN
            if pd.notna(row['Structural Integrity']):
                popup_content += f"<b>Structural Integrity:</b> {row['Structural Integrity']}<br>"

            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_content, max_width=300),
            ).add_to(m)

        # Display the map
        folium_static(m)
    else:
        st.write("No valid coordinates available for the selected filters.")
#Nomadic Shelters

    # Section for azibs
    st.markdown('<div class="section-title">Nomadic Shelters</div>', unsafe_allow_html=True)
    st.markdown('<div class="text">Importance of azibs</div>', unsafe_allow_html=True)
    
    # Reorder columns to place 'Douar' after 'Type' and remove 'Pictures'
    shelters = shelters[['Name','Douar', 'Latitude', 'Longitude', 'Commune', 'Douars Benefiting','Number of herders',  
                       'Estimated Cost', 'Structural Integrity', 'Notes']]
    
    # Create columns for filters (50% width each)
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        douar_filter = st.text_input("Search by Douar", key='shelters_douar')       
    with col2:
        commune_filter = st.text_input("Search by Commune", key='shelters_commune')      
    with col3:
        benefiting_filter = st.text_input("Search by Douars Benefiting", key='shelters_benefiting')
       
    col1, col2 = st.columns([1, 1])  
   
    with col1:
        structural_filter = st.text_input("Search by Structural Integrity", key='shelters_structural')

    # Apply filters to irrigation data
    filtered_shelters = shelters

    # Apply each filter only if the corresponding input is not empty
    
    if douar_filter:
         filtered_shelters = filtered_shelters[filtered_shelters['Douar'].str.contains(douar_filter, case=False, na=False)]

    if commune_filter:
        filtered_shelters = filtered_shelters[filtered_shelters['Commune'].str.contains(commune_filter, case=False, na=False)]

    if benefiting_filter:
        filtered_shelters = filtered_shelters[filtered_shelters['Douars Benefiting'].str.contains(benefiting_filter, case=False, na=False)]

    if structural_filter:
        filtered_shelters = filtered_shelters[filtered_shelters['Structural Integrity'].str.contains(structural_filter, case=False, na=False)]
 
    
    # Display the filtered data
    st.dataframe(filtered_shelters, hide_index=True)

    # Display map only for rows with valid coordinates
    valid_coords = filtered_shelters.dropna(subset=['Latitude', 'Longitude'])
    
    if not valid_coords.empty:
        # Create the map centered at the average location of the azibs
        m = folium.Map(location=[valid_coords['Latitude'].mean(), valid_coords['Longitude'].mean()], zoom_start=8)

        # Add markers to the map for each irrigation system
        for _, row in valid_coords.iterrows():
            popup_content = (
                f"<b>Douar:</b> {row['Douar']}<br>"
                f"<b>Commune:</b> {row['Commune']}<br>"
                
            )

            # Only add 'Structural Integrity' if it's not NaN
            if pd.notna(row['Structural Integrity']):
                popup_content += f"<b>Structural Integrity:</b> {row['Structural Integrity']}<br>"

            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_content, max_width=300),
            ).add_to(m)

        # Display the map
        folium_static(m)
    else:
        st.write("No valid coordinates available for the selected filters.")
#Agricultural terraces
    # Section for agricultural terraces
    st.markdown('<div class="section-title">Agricultural Terraces</div>', unsafe_allow_html=True)
    st.markdown('<div class="text">Importance of agricultural terraces</div>', unsafe_allow_html=True)
    
    # Reorder columns to place 'Douar' after 'Type' and remove 'Pictures'
    terraces = terraces[['Douar', 'Latitude', 'Longitude', 'Commune', 'Douars Benefiting',
                       'Estimated Cost', 'Structural Integrity', 'Notes']]
    
    # Create columns for filters (50% width each)
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        douar_filter = st.text_input("Search by Douar", key='terraces_douar')       
    with col2:
        commune_filter = st.text_input("Search by Commune", key='terraces_commune')      
    with col3:
        benefiting_filter = st.text_input("Search by Douars Benefiting", key='terraces_benefiting')
       
    col1, col2 = st.columns([1, 1])  
   
    with col1:
        structural_filter = st.text_input("Search by Structural Integrity", key='terraces_structural')

    # Apply filters to irrigation data
    filtered_terraces = terraces

    # Apply each filter only if the corresponding input is not empty
    
    if douar_filter:
         filtered_terraces = filtered_terraces[filtered_terraces['Douar'].str.contains(douar_filter, case=False, na=False)]

    if commune_filter:
        filtered_terraces = filtered_terraces[filtered_terraces['Commune'].str.contains(commune_filter, case=False, na=False)]

    if benefiting_filter:
        filtered_terraces = filtered_terraces[filtered_terraces['Douars Benefiting'].str.contains(benefiting_filter, case=False, na=False)]

    if structural_filter:
        filtered_terraces = filtered_terraces[filtered_terraces['Structural Integrity'].str.contains(structural_filter, case=False, na=False)]
 
    
    # Display the filtered data
    st.dataframe(filtered_terraces, hide_index=True)

    # Display map only for rows with valid coordinates
    valid_coords = filtered_terraces.dropna(subset=['Latitude', 'Longitude'])
    
    if not valid_coords.empty:
        # Create the map centered at the average location of the azibs
        m = folium.Map(location=[valid_coords['Latitude'].mean(), valid_coords['Longitude'].mean()], zoom_start=8)

        # Add markers to the map for each irrigation system
        for _, row in valid_coords.iterrows():
            popup_content = (
                f"<b>Douar:</b> {row['Douar']}<br>"
                f"<b>Commune:</b> {row['Commune']}<br>"
                
            )

            # Only add 'Structural Integrity' if it's not NaN
            if pd.notna(row['Structural Integrity']):
                popup_content += f"<b>Structural Integrity:</b> {row['Structural Integrity']}<br>"

            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_content, max_width=300),
            ).add_to(m)

        # Display the map
        folium_static(m)
    else:
        st.write("No valid coordinates available for the selected filters.")
#Granaries
    # Section for granaries
    st.markdown('<div class="section-title">Granaries</div>', unsafe_allow_html=True)
    st.markdown('<div class="text">Importance of granaries</div>', unsafe_allow_html=True)
    
    # Reorder columns to place 'Douar' after 'Type' and remove 'Pictures'
    granaries = granaries[['Douar', 'Latitude', 'Longitude', 'Commune', 'Douars Benefiting',
                       'Estimated Cost', 'Structural Integrity', 'Notes']]
    
    # Create columns for filters (50% width each)
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        douar_filter = st.text_input("Search by Douar", key='granaries_douar')       
    with col2:
        commune_filter = st.text_input("Search by Commune", key='granaries_commune')      
    with col3:
        benefiting_filter = st.text_input("Search by Douars Benefiting", key='granaries_benefiting')
       
    col1, col2 = st.columns([1, 1])  
   
    with col1:
        structural_filter = st.text_input("Search by Structural Integrity", key='granaries_structural')

    # Apply filters to irrigation data
    filtered_granaries = granaries

    # Apply each filter only if the corresponding input is not empty
    
    if douar_filter:
         filtered_granaries = filtered_granaries[filtered_granaries['Douar'].str.contains(douar_filter, case=False, na=False)]

    if commune_filter:
        filtered_granaries = filtered_granaries[filtered_granaries['Commune'].str.contains(commune_filter, case=False, na=False)]

    if benefiting_filter:
        filtered_granaries = filtered_granaries[filtered_granaries['Douars Benefiting'].str.contains(benefiting_filter, case=False, na=False)]

    if structural_filter:
        filtered_granaries = filtered_granaries[filtered_granaries['Structural Integrity'].str.contains(structural_filter, case=False, na=False)]
 
    
    # Display the filtered data
    st.dataframe(filtered_granaries, hide_index=True)

    # Display map only for rows with valid coordinates
    valid_coords = filtered_granaries.dropna(subset=['Latitude', 'Longitude'])
    
    if not valid_coords.empty:
        # Create the map centered at the average location of the azibs
        m = folium.Map(location=[valid_coords['Latitude'].mean(), valid_coords['Longitude'].mean()], zoom_start=8)

        # Add markers to the map for each irrigation system
        for _, row in valid_coords.iterrows():
            popup_content = (
                f"<b>Douar:</b> {row['Douar']}<br>"
                f"<b>Commune:</b> {row['Commune']}<br>"
                
            )

            # Only add 'Structural Integrity' if it's not NaN
            if pd.notna(row['Structural Integrity']):
                popup_content += f"<b>Structural Integrity:</b> {row['Structural Integrity']}<br>"

            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_content, max_width=300),
            ).add_to(m)

        # Display the map
        folium_static(m)
    else:
        st.write("No valid coordinates available for the selected filters.")
    

    st.markdown('<div class="section-title">Pilot Project</div>', unsafe_allow_html=True)
    st.markdown('<div class="text">Progress report on the pilot project / Sites already repared ...</div>', unsafe_allow_html=True)
