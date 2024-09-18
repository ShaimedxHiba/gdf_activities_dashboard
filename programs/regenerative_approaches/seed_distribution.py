import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static


# Load the Excel data
@st.cache_data
def load_data():
    # Load both sheets from the Excel file
    november_df = pd.read_excel('data/seed_distribution_consolidated.xlsx', sheet_name='November 2023')
    march_df = pd.read_excel('data/seed_distribution_consolidated.xlsx', sheet_name='March 2024')
    return november_df, march_df

# Function to create a folium map with seed distribution data
# Filtered map display function
def display_map(filtered_november_df, filtered_march_df):
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
# Function to display seed distribution dashboard
def seed_distribution():
    
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

        /* Custom style for introduction text */
        .intro-text {
            font-size: 20px;
            color: #555555;
            margin-bottom: 30px;
            text-align: center;
        }

        /* Custom style for summary section titles */
        .summary-title {
            font-size: 24px;
            color: #4CAF50; /* Green */
            font-weight: bold;
            margin-top: 40px;
            margin-bottom: 10px;
        }

        /* Adjust the padding around the content */
        .block-container {
            padding: 2rem 1rem;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Load the data
    november_df, march_df = load_data()
    
    # Strip any leading or trailing spaces from column names
    november_df.columns = november_df.columns.str.strip()
    march_df.columns = march_df.columns.str.strip()

    # Displaying the title and introduction
    st.markdown('<div class="title">Seed Distribution Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="intro-text">This dashboard provides insights on the seed distribution conducted in several villages across four communes in November 2023 and March 2024.</div>', unsafe_allow_html=True)

    # Summary statistics for November and March
    st.markdown('<div class="summary-title">Global Overview</div>', unsafe_allow_html=True)

    # Calculate total number of each seed distributed, number of villages, and number of farmers for November
    november_seed_totals = november_df.drop(columns=['Latitude', 'Longitude', 'Douar', 'Commune', 'Farmers Benefited']).sum().astype(int)
    november_total_seeds_distributed = november_seed_totals.sum()

    # Calculate total number of each seed distributed, number of villages, and number of farmers for March
    march_seed_totals = march_df.drop(columns=['Latitude', 'Longitude', 'Douar', 'Commune', 'Farmers Benefited']).sum().astype(int)
    march_total_seeds_distributed = march_seed_totals.sum()

    # Number of villages and farmers
    november_totals = {
        'Total Villages': int(november_df['Douar'].nunique()),
        'Total Farmers': int(november_df['Farmers Benefited'].sum())
    }

    march_totals = {
        'Total Villages': int(march_df['Douar'].nunique()),
        'Total Farmers': int(march_df['Farmers Benefited'].sum())
    }

    # Combine seed types from both November and March, ensuring all unique seeds are included
    all_seed_types = list(set(november_seed_totals.index.tolist() + march_seed_totals.index.tolist()))

    # Reindex both November and March seed totals to ensure they have the same seeds
    november_seed_totals = november_seed_totals.reindex(all_seed_types, fill_value='-')
    march_seed_totals = march_seed_totals.reindex(all_seed_types, fill_value='-')

    # Add the 'Total Seeds Distributed' row at the end of both lists
    all_seed_types.append('Total Seeds Distributed')

    # Create the summary DataFrame with seed totals for both November and March
    summary_df = pd.DataFrame({
        'Seed Variety': [seed + " (kg)" for seed in all_seed_types],
        'November 2023': november_seed_totals.tolist() + [november_total_seeds_distributed],
        'March 2024': march_seed_totals.tolist() + [march_total_seeds_distributed]
    })

    # Add the village and farmer counts at the bottom of the table
    village_farmers_df = pd.DataFrame({
        'Seed Variety': ['Total Villages', 'Total Farmers'],
        'November 2023': [november_totals['Total Villages'], november_totals['Total Farmers']],
        'March 2024': [march_totals['Total Villages'], march_totals['Total Farmers']]
    })

    # Concatenate the summary_df and village_farmers_df
    summary_df = pd.concat([summary_df, village_farmers_df], ignore_index=True)

    # Display summary statistics as a table
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    # Display seed distribution stats by seed type
    st.markdown('<div class="summary-title">Seed Distribution by Commune</div>', unsafe_allow_html=True)

    # Grouping data by Commune and calculating sums for both periods
    november_seed_stats = november_df.groupby(['Commune']).sum()
    march_seed_stats = march_df.groupby(['Commune']).sum()

    # November Seed Distribution - Customizing axis labels
    fig_nov = px.bar(november_seed_stats.reset_index(), 
                     x='Commune', 
                     y=['Barley', 'Faba Beans', 'Peas', 'Carrots', 'Turnip'], 
                     barmode='group', 
                     title='November Seed Distribution',
                     labels={'value': 'Number of Kilos (kg)', 'variable': 'Seed Type'})

    # Applying log scale to y-axis to deal with large differences
    fig_nov.update_layout(yaxis_type="log")

    # March Seed Distribution - Customizing axis labels
    fig_march = px.bar(march_seed_stats.reset_index(), 
                       x='Commune', 
                       y=['Corn', 'Courgette', 'Red Ball', 'Long Green Pumpkin'], 
                       barmode='group', 
                       title='March Seed Distribution',
                       labels={'value': 'Number of Kilos (kg)', 'variable': 'Seed Type'})

    # Applying log scale to y-axis
    fig_march.update_layout(yaxis_type="log")

    # Create two equal columns for side-by-side display of charts
    col1, col2 = st.columns([1, 1])  # Equal width

    # Display November chart in the first column
    with col1:
        st.plotly_chart(fig_nov)

    # Display March chart in the second column
    with col2:
        st.plotly_chart(fig_march)

    # Compare benefiting farmers in each commune
    st.markdown('<div class="summary-title">Comparison of Benefiting Farmers</div>', unsafe_allow_html=True)

    # Merging data for comparison
    combined_df = pd.merge(november_seed_stats.reset_index(), march_seed_stats.reset_index(), on='Commune', suffixes=('_November', '_March'))

    fig_combined = px.bar(combined_df, 
                          x='Commune', 
                          y=['Farmers Benefited_November', 'Farmers Benefited_March'], 
                          barmode='group',
                          title='Comparison of Benefiting Farmers in November vs March',
                          labels={'value': 'Number of farmers', 'variable': 'Number of farmers'})
    st.plotly_chart(fig_combined)

    # Display seed distribution stats by village
    st.markdown('<div class="summary-title">Seed Distribution by Douar</div>', unsafe_allow_html=True)

    # Search bar
    search_query = st.text_input('Search by douar, commune, or seed variety to display only relevant data:')

    # Convert search query to lowercase for case-insensitive comparison
    search_query = search_query.lower()

    # Filter data based on search query for Douar, Commune, or any Seed Type
    def filter_dataframe(df):
        return df[
            df.apply(lambda row: search_query in str(row['Douar']).lower() or 
                                 search_query in str(row['Commune']).lower() or 
                                 any(search_query in str(seed).lower() for seed in row.index if seed not in ['Douar', 'Commune', 'Latitude', 'Longitude']),
                                 axis=1)
        ]

    # Apply filter to both November and March data
    filtered_november_df = filter_dataframe(november_df)
    filtered_march_df = filter_dataframe(march_df)

    # Create two equal columns for side-by-side display
    col1, col2 = st.columns([1, 1])  # Equal width

    # Display filtered November data in the first column
    with col1:
        st.subheader('November 2023')
        st.dataframe(filtered_november_df, use_container_width=True,hide_index=True)

    # Display filtered March data in the second column
    with col2:
        st.subheader('March 2024')
        st.dataframe(filtered_march_df, use_container_width=True,hide_index=True)

    # Check if the filtered dataframes have any data
    if not filtered_november_df.empty:
        # November chart
        fig_nov = px.bar(filtered_november_df, 
                         x='Douar', 
                         y=filtered_november_df.columns.difference(['Douar', 'Commune', 'Latitude', 'Longitude', 'Farmers Benefited']),
                         title='Seed Distribution in November 2023 by Douar',
                         labels={'value': 'Number of Kilos (kg)', 'variable': 'Seed Type'},
                         barmode='group')
        fig_nov.update_layout(yaxis_type="log")             
        st.plotly_chart(fig_nov)

    if not filtered_march_df.empty:
        # March chart
        fig_march = px.bar(filtered_march_df, 
                           x='Douar', 
                           y=filtered_march_df.columns.difference(['Douar', 'Commune', 'Latitude', 'Longitude', 'Farmers Benefited']),
                           title='Seed Distribution in March 2024 by Douar',
                           labels={'value': 'Number of Kilos (kg)', 'variable': 'Seed Type'},
                           barmode='group')
        fig_march.update_layout(yaxis_type="log")
        st.plotly_chart(fig_march)

    if not filtered_november_df.empty or not filtered_march_df.empty:
    # Add the map below the data
        st.subheader("Map of Douars with Seed Distribution")
        display_map(filtered_november_df, filtered_march_df)    
