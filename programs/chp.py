import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import numpy as np

# Load the Excel data
@st.cache_data
def load_data():
    # Load both sheets from the Excel file
    watermills = pd.read_excel('data/chp.xlsx', sheet_name='Watermills')
    irrigation = pd.read_excel('data/chp.xlsx', sheet_name='Irrigation basins and canals')
    springs = pd.read_excel('data/chp.xlsx', sheet_name='Springs')
    terraces = pd.read_excel('data/chp.xlsx', sheet_name='Agricultural terraces')
    shelters = pd.read_excel('data/chp.xlsx', sheet_name='Nomadic shelters')
    granaries = pd.read_excel('data/chp.xlsx', sheet_name='Granaries')
    return watermills, irrigation, springs, terraces, shelters, granaries

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

    # Introduction
    st.markdown('<div class="title">Cultural Heritage Sites</div>', unsafe_allow_html=True)

    # Initialize variables to hold the totals for each site type
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
    
    # Display stats by default
    st.markdown(stats_html, unsafe_allow_html=True)
    st.markdown('<div class="text">Cultural heritage structures – many of which were damaged in the September 8th 2023 earthquake – are linked in High Atlas cultural landscapes: springs (Aghbalou) feed reservoirs (Afraw) and canals (Targua) that irrigate agricultural terraces (Igrane) and drive water mills Azarg). Nomadic shelters (Azib) used in the summertime are important to maintaining high elevation communal pastures (Agdal).These cultural landscapes have also been called socio-ecological production landscapes. These are dynamic mosaics of habitats and land uses shaped over the years by interactions between people and nature in ways that maintain biodiversity and provide humans with goods and services needed for their wellbeing.</div>', unsafe_allow_html=True)

    # Multi-select for site types
    selected_sites = st.multiselect("Select Cultural Heritage Sites to display:", 
                                      ["Watermills", "Irrigation Systems", "Springs", "Terraces", 
                                       "Nomadic Shelters", "Granaries"])

    # Display corresponding sections based on user selection
    if "Watermills" in selected_sites:
        st.markdown('<div class="section-title">Watermills</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">High Atlas traditional water mills – called Azarg in the local Tachelhit language – have been used for centuries to grind grains such as barley, maize and wheat. Scattered in remote villages throughout the mountains, they are situated near irrigation canals, rivers and streams to harness the power of flowing water for milling. Their structure is simple and effective. A waterwheel – traditionally made of wood, which can last for 10 to 15 years – is turned by the force of the flowing water. It is connected to a shaft that rotates a grindstone inside the mill. The flow of water through a dam or sluice gate is sometimes regulated manually by the miller to control the speed of the waterwheel and at which the grindstone turns. Seeds are fed into a hopper above the grindstone, which crushes the grain between its surface and a stationary stone, turning it into flour which is collected in a container. The flour is used for baking bread, a staple and symbolic food in the region. The mill is also used to grind zemmita – a blend of almonds barley, chickpeas, and fennel, flax, millet and sesame seeds – or salt to be mixed with cattle feed. Beyond this functional role, the traditional water mills are culturally significant as they are accompanied by traditional knowledge and know-how. This intangible cultural heritage is maintained by a few elderly traditional craftsmen, who have expertise in building water mills, from millstone fetching and sculpting to calculating the exact angle and dimensions of the canal bringing water to the wheel.</div>', unsafe_allow_html=True)
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
                # Group watermills by coordinates (Latitude, Longitude)
                grouped_watermills = valid_coords.groupby(['Latitude', 'Longitude']).size().reset_index(name='Watermill Count')

                # Create the map centered at the average location of the watermills
                m = folium.Map(location=[valid_coords['Latitude'].mean(), valid_coords['Longitude'].mean()], zoom_start=8)

                # Define a small offset (in degrees) for markers that share the same coordinates
                offset_step = 0.0001  # Adjust this as needed for the map scale

                # Add markers to the map for each unique coordinate
                for _, row in grouped_watermills.iterrows():
                    # Filter the watermills at the current coordinate
                    watermills_at_location = valid_coords[(valid_coords['Latitude'] == row['Latitude']) & (valid_coords['Longitude'] == row['Longitude'])]

                    # If multiple watermills are at the same coordinates, apply offsets
                    num_watermills = int(row['Watermill Count'])
                    if num_watermills > 1:
                            lat_offsets = np.linspace(-offset_step, offset_step, num_watermills)
                            lon_offsets = np.linspace(-offset_step, offset_step, num_watermills)
                    else:
                            lat_offsets = [0]
                            lon_offsets = [0]

                    # Add each watermill as a separate marker, slightly offset if needed
                    for i, (_, watermill) in enumerate(watermills_at_location.iterrows()):
                            # Create popup content for the current watermill
                            popup_content = (
                            f"<b>Douar:</b> {watermill['Douar']}<br>"
                            f"<b>Commune:</b> {watermill['Commune']}<br>"
                            f"<b>Ownership:</b> {watermill['Ownership Status']}<br>"
                            f"<b>Structural Integrity:</b> {watermill['Structural Integrity']}<br>"
                    )

                            # Apply the offset for markers at the same location
                            latitude = watermill['Latitude'] + lat_offsets[i]
                            longitude = watermill['Longitude'] + lon_offsets[i]

                            # Add a marker to the map
                            folium.Marker(
                            location=[latitude, longitude],
                            popup=folium.Popup(popup_content, max_width=300),
                            ).add_to(m)
            
                # Display the map
                folium_static(m)
        else:
                st.write("No valid coordinates available for the selected filters.")
               

    if "Irrigation Systems" in selected_sites:
        st.markdown('<div class="section-title">Irrigation Systems</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">Traditional reservoirs (Afraw) and canals (Targua) are High Atlas communal water management systems that have sustained agriculture and livelihoods for centuries. As cisterns or reservoirs that capture water from springs and streams, afraw serve as local water storage facilities, especially in arid zones. Using local materials such as clay and stone, they are often built in depressions or hollows in the landscape to maximize rainwater and snowmelt collection. The stored water is used for irrigation of agricultural fields and terraces, watering livestock and household consumption. The reservoirs are connected to targua, irrigation canals used for transporting water across the landscape and distributing it to agricultural fields and orchards. The targua are traditionally built with earthwork and stone masonry, which is gradually being replaced by concrete, iron bar and other modern materials. The canals snake through the natural contours of the landscape, often traversing steep slopes and rocky terrain, before branching out to reach individual fields and orchards. The distribution of water is managed collectively by the community, providing equitable access and efficient use of water resources. Since the earthquake, community members have been collaborating – following their traditional practice of tiwizi or communal labor – to clear debris, reinforce canal walls to and repair leaks and breaches.</div>', unsafe_allow_html=True)
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

    if "Springs" in selected_sites:
        st.markdown('<div class="section-title">Springs</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">Abundant springs – called Aghbalou in the High Atlas – play an important role in regional livelihoods and ecology, sustaining biodiversity and local livelihoods. Traditionally revered as sacred sites, they can be found at various elevations, from high mountain peaks to lower valleys, depending on geological factors such as rock permeability and hydrological processes. They are fed by rainfall, snowmelt and underground aquifers, making them essential sources of freshwater used for agriculture, livestock and people. Community members have traditional ways of assessing the springs’ flow rate, volume and water quality, which can be further evaluated through hydraulic studies. Communal agreements and customary laws govern access to the springs and the distribution of water that flows from them. Communal labor is used to build and maintain stonework enclosures that protect the springs, and the canals that bring the water to agricultural fields and villages. These practices sustain small wetland habitats that harbor a rich diversity of plant and animal species, including endemic and rare taxa. The earthquake destroyed some of the structures while at least temporarily increased water flow in some areas and decreased it in others.</div>', unsafe_allow_html=True)
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

    if "Terraces" in selected_sites:
        st.markdown('<div class="section-title">Terraces</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">High Atlas agricultural terraces – called Igrane in the Tachelhit language spoken in the area – are a remarkable example of human ingenuity and adaptation to steep mountain slopes across Algeria, Morocco and Tunisia. The terraces have a dual role in helping communities maintain their livelihoods while preserving the fragile mountain ecosystem. Established in valleys and foothills where arable land is scarce, they enhance soil fertility, manage water runoff, maximize exposure to sun and optimize land use. The construction of these agricultural terraces requires significant expertise, knowledge and labor. Stone walls, typically built without mortar, reinforce the contours of mountain slopes to create the level platforms. Depending on factors such as altitude, climate and soil quality, local farmers cultivate a diversity of subsistence crops – including barley, carrots, fava beans, maize, peas, turnips and wheat – on the flat surfaces of the terraces, along with fruit trees like figs and olives, and medicinal plants. The plots are irrigated by diverting water from natural springs or streams through an intricate system of canals. The water is allocated among the farmers through a communal process, and is carefully distributed over the different levels of terraces to ensure optimal irrigation. These traditional farming practices are an example of intangible cultural heritage passed down through generations.</div>', unsafe_allow_html=True)
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

    if "Nomadic Shelters" in selected_sites:
        st.markdown('<div class="section-title">Nomadic Shelters</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">Nomadic shelters, which are called Azib in Tachelhit, are temporary dwellings used by pastoralists in the High Atlas. Built with stones, wood and other locally available materials, they provide shelter for both humans and livestock during summertime high-elevation grazing. The Azib are typically arranged in clusters, with multiple families or households sharing communal spaces for cooking, socializing and tending livestock. Some are more complex shelters (Issguane) comprising three areas: an ⁠indoor animal enclosure (Agrour), an outdoor space for animals (Adaghass), and a herder’s room (Tahanout), which can double as a grain and hay storage room. The shelters facilitate transhumance – the seasonal movement of camels, goats and sheep between highland and lowland pastures – which is an important part of the livelihoods of many High Atlas communities. Some nomadic shelters are located in Agdal, communally managed pastures used by several tribes.</div>', unsafe_allow_html=True)
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

    if "Granaries" in selected_sites:
        st.markdown('<div class="section-title">Granaries</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">Granaries, known as Ighrem, are communal storage facilities for barley, maize, wheat and other grains situated within or near villages. As storehouses of seed and surplus grain harvested by local communities, these fortified structures were important for food security. They helped protect grains from moisture, insect pests and rodents, conserving them for future consumption or cultivation. In addition, they were a safeguard against food shortages during periods of conflict, drought and famine. Typically built from locally sourced materials – including earth, stone and wood – they feature thick walls and small windows to defend against theft and unauthorized access. Traditionally, each household would contribute a portion of its harvest to the granary, ensuring a collective reserve of grain to sustain the community in times of need. Decisions regarding its allocation and distribution were made democratically by community leaders or councils. The granaries, many of which have fallen into disrepair, were owned and managed by the local community. Despite high profile efforts to restore some of the more monumental ighrem, many smaller structures await rehabilitation.</div>', unsafe_allow_html=True)
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

if __name__ == "__main__":
    chp()

