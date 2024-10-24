import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import numpy as np


def load_data():
    # Load both sheets from the Excel file
    distributions = pd.read_excel('data/gdf_eq_response.xlsx', sheet_name='Distributions')
    schools = pd.read_excel('data/gdf_eq_response.xlsx', sheet_name='Temporary Schools')
    wash = pd.read_excel('data/gdf_eq_response.xlsx', sheet_name='WASH')
    medical = pd.read_excel('data/gdf_eq_response.xlsx', sheet_name='Medical caravans') 
    return distributions,schools,wash,medical

def display_map(filtered_november_df, filtered_march_df):
    # Filter out rows with NaN values in location columns (latitude, longitude)
    filtered_november_df = filtered_november_df.dropna(subset=['Latitude', 'Longitude'])
    filtered_march_df = filtered_march_df.dropna(subset=['Latitude', 'Longitude'])

    # Create a Folium map centered around the median of the filtered November data
    if not filtered_november_df.empty:
        lat_center = filtered_november_df['Latitude'].median()
        lon_center = filtered_november_df['Longitude'].median()
    else:
        lat_center = filtered_march_df['Latitude'].median()
        lon_center = filtered_march_df['Longitude'].median()
    
    m = folium.Map(location=[lat_center, lon_center], zoom_start=10)

    # Helper function to create popups, excluding NaN values
    def generate_popup(row):
        popup_content = ""
        for col, value in row.items():
            if pd.notna(value):  # Only include non-NaN values
                popup_content += f"<b>{col}:</b> {value} <br>"
        return popup_content

    # Add markers for November data
    for _, row in filtered_november_df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(generate_popup(row), max_width=300),
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    # Add markers for March data
    for _, row in filtered_march_df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(generate_popup(row), max_width=300),
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(m)

    # Display the map in the Streamlit app
    folium_static(m)

def er():
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

    # Load the data
    distributions,schools,wash,medical = load_data()

    st.markdown('<div class="title">Emergency Response</div>', unsafe_allow_html=True)
    st.markdown('<div class="text">Within two days of the earthquake, the GDF team swiftly transitioned from its usual focus on biodiversity and conservation to becoming a vital part of the disaster relief effort. Leveraging its decade-long relationship with the communities of the High Atlas, quickly mobilised to address the most pressing needs being reported on the ground.Initially, its efforts were concentrated on three critical fronts: providing essential material aid such as food and clothing, ensuring temporary shelter through tents and other necessities, and providing medical and hygiene support to safeguard the health of those affected. In the long term, GDF is committed to long-term recovery, community well-being, and sustainable development.</div>', unsafe_allow_html=True)
       
    
    
    # Strip any leading or trailing spaces from column names
    distributions.columns = distributions.columns.str.strip()
    schools.columns = schools.columns.str.strip()
    wash.columns = wash.columns.str.strip()
    medical.columns = medical.columns.str.strip()

    # Initialize variables to hold the unique village counts for each type of activity
    unique_villages_distributions = distributions['Douar Name'].nunique()
    unique_villages_schools = schools['Douar Name'].nunique()
    unique_villages_wash = wash['Douar Name'].nunique()
    unique_villages_medical = medical['Douar Name'].nunique()

    # Create a container for the stats
    stats_html = f'''
        <div class="stats-container">
            <div class="stat">
                <div class="stat-number">{unique_villages_distributions}</div>
                Villages received various distributions
            </div>
            <div class="stat">
                <div class="stat-number">{unique_villages_schools}</div>
                Villages benefited from temporary schools
            </div>
            <div class="stat">
                <div class="stat-number">{unique_villages_wash}</div>
                Villages benefited from WASH facilities
            </div>
            <div class="stat">
                <div class="stat-number">{unique_villages_medical}</div>
                Villages benefited from medical caravans
            </div>
        </div>
    '''

    # Display stats by default
    st.markdown(stats_html, unsafe_allow_html=True)
    # Multi-select for site types
    selected_sites = st.multiselect("Select Initiative to Display:", 
                                    ["Distributions", "Temporary Schools", "WASH", "Medical Caravans"])

    # Helper function to display project information based on user selection
    def display_project(data, project_name):
        st.markdown(f'<div class="section-title">{project_name}</div>', unsafe_allow_html=True)
        
        # Reorder columns and remove unnecessary ones (adjust columns as needed)
        data = data[['Douar Name', 'Commune', 'Province', 'Latitude', 'Longitude', 'Description', 'Date', 'Partners']]
        
        # Create columns for filters (50% width each)
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            douar_filter = st.text_input(f"Search by Douar", key=f'{project_name}_douar')
        with col2:
            commune_filter = st.text_input(f"Search by Commune", key=f'{project_name}_commune')
        with col3:
            partner_filter = st.text_input(f"Search by Partners", key=f'{project_name}_partner')
        
        col1, col2 = st.columns([1, 1])
        with col1:
            province_filter = st.text_input(f"Search by Province", key=f'{project_name}_province')
        with col2:
            date_filter = st.text_input(f"Search by Date", key=f'{project_name}_date')

        # Apply filters to data
        filtered_data = data.copy()

        if douar_filter:
            filtered_data = filtered_data[filtered_data['Douar Name'].str.contains(douar_filter, case=False, na=False)]
        if commune_filter:
            filtered_data = filtered_data[filtered_data['Commune'].str.contains(commune_filter, case=False, na=False)]
        if partner_filter:
            filtered_data = filtered_data[filtered_data['Partners'].str.contains(partner_filter, case=False, na=False)]
        if province_filter:
            filtered_data = filtered_data[filtered_data['Province'].str.contains(province_filter, case=False, na=False)]
        if date_filter:
            filtered_data = filtered_data[filtered_data['Date'].str.contains(date_filter, case=False, na=False)]

        # Display the filtered data
        st.dataframe(filtered_data, hide_index=True)

        # Display map only for rows with valid coordinates
        valid_coords = filtered_data.dropna(subset=['Latitude', 'Longitude'])

        if not valid_coords.empty:
            # Group by coordinates (Latitude, Longitude) to handle multiple entries at the same location
            grouped_data = valid_coords.groupby(['Latitude', 'Longitude']).size().reset_index(name=f'{project_name} Count')

            # Create the map centered at the average location
            m = folium.Map(location=[valid_coords['Latitude'].mean(), valid_coords['Longitude'].mean()], zoom_start=8)

            # Define a small offset for markers that share the same coordinates
            offset_step = 0.0001  # Adjust as needed for your map scale

            # Add markers to the map for each unique coordinate
            for _, row in grouped_data.iterrows():
                # Filter data at the current coordinate
                projects_at_location = valid_coords[(valid_coords['Latitude'] == row['Latitude']) & (valid_coords['Longitude'] == row['Longitude'])]

                # If multiple projects are at the same coordinates, apply offsets
                num_projects = int(row[f'{project_name} Count'])
                if num_projects > 1:
                    lat_offsets = np.linspace(-offset_step, offset_step, num_projects)
                    lon_offsets = np.linspace(-offset_step, offset_step, num_projects)
                else:
                    lat_offsets = [0]
                    lon_offsets = [0]
                
                # Add each project as a separate marker
                for i, (_, project) in enumerate(projects_at_location.iterrows()):
                   
                    # Create popup content
                    popup_content = (
                        f"<b>Douar:</b> {project['Douar Name']}<br>"
                        f"<b>Commune:</b> {project['Commune']}<br>"
                        f"<b>Province:</b> {project['Province']}<br>"
                        f"<b>Description:</b> {project['Description']}<br>"
                        f"<b>Date:</b> {project['Date']}<br>"
                        
                    )
                    # Only add the 'Partners' section if it's not None
                    if pd.notna(project['Partners']):
                        popup_content += f"<b>Partners:</b> {project['Partners']}<br>"

                    # Apply offset
                    latitude = project['Latitude'] + lat_offsets[i]
                    longitude = project['Longitude'] + lon_offsets[i]

                    # Add marker to map
                    folium.Marker(
                        location=[latitude, longitude],
                        popup=folium.Popup(popup_content, max_width=300),
                    ).add_to(m)

            # Display the map
            folium_static(m)
        else:
            st.write(f"No valid coordinates available for {project_name} with the selected filters.")


    # Display corresponding sections based on user selection
    if "Distributions" in selected_sites:
        display_project(distributions, "Distributions")

    if "Temporary Schools" in selected_sites:
        display_project(schools, "Temporary Schools")

    if "WASH" in selected_sites:
        display_project(wash, "WASH")

    if "Medical Caravans" in selected_sites:
        display_project(medical, "Medical Caravans")
