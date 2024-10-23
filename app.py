import streamlit as st

from programs.regenerative_approaches.seed_distribution import seed_distribution
from programs.regenerative_approaches.nurseries import nurseries
from programs.regenerative_approaches.plant_distribution import plant_distribution
from programs.regenerative_approaches.its import its
from programs.regenerative_approaches.animal_shelters import animal_shelters
from programs.regenerative_approaches.ffs import ffs

from programs.sustainable_livelihoods.digital import digital
from programs.sustainable_livelihoods.ings import ings
from programs.sustainable_livelihoods.resb import resb
from programs.sustainable_livelihoods.lpcl import lpcl

from programs.eq_response.er import er
from programs.eq_response.chp import chp

# Sidebar for navigation
st.sidebar.title("GDF/MBLA Activities Dashboard")

# Main program selectbox to ensure only one program runs at a time
program_type = st.sidebar.selectbox("Select Program Type", [
    "Regenerative Approaches", 
    "Sustainable Livelihoods Program",
    "EQ Response",
    "Cultural Heritage Preservation"
])

# Only show options based on the selected program type
if program_type == "Regenerative Approaches":
    with st.sidebar.expander("Regenerative Approaches", expanded=True):
        sub_program = st.selectbox("Select Sub-Program", [
            "Plant nurseries",
            "Plant distribution",
            "Seed exchange",
            "Agroecosystem parcels enhancement",
            "Transhumant pastoralists"
        ])

    # Display corresponding content based on the selected sub-program
    if sub_program == "Plant nurseries":
        nurseries()

    elif sub_program == "Plant distribution":
        plant_distribution()

    elif sub_program == "Seed exchange":
        sub_seed_program = st.selectbox("Select Sub-Category", ["Seed distribution"])
        if sub_seed_program == "Seed distribution":
            seed_distribution()

    elif sub_program == "Agroecosystem parcels enhancement":
        sub_agro_program = st.selectbox("Select Sub-Category", ["Farmers field school", "Irrigation, Terracing and Soil Fertility"])
        if sub_agro_program == "Farmers field school":
            ffs()
        elif sub_agro_program == "Irrigation, Terracing and Soil Fertility":
            its()

    elif sub_program == "Transhumant pastoralists":
        sub_pastoral_program = st.selectbox("Select Sub-Category", ["Animal shelters"])
        if sub_pastoral_program == "Animal shelters":
            animal_shelters()

elif program_type == "Sustainable Livelihoods Program":
    with st.sidebar.expander("Sustainable Livelihoods Program", expanded=True):
        sub_program_slp = st.selectbox("Select Sub-Program", [
            "Local product certification and labelling",
            "Rural entrepreneurship skill building",
            "Innovation of novel goods and services",
            "Digital entrepreneurship and platforms for local product marketing"
        ])

    # Display corresponding content based on the selected sub-program
    if sub_program_slp == "Local product certification and labelling":
        lpcl()

    elif sub_program_slp == "Rural entrepreneurship skill building":
        resb()

    elif sub_program_slp == "Innovation of novel goods and services":
        ings()

    elif sub_program_slp == "Digital entrepreneurship and platforms for local product marketing":
        digital()

elif program_type == "EQ Response":
    with st.sidebar.expander("EQ Response", expanded=True):
        sub_program_eq = st.selectbox("Select Sub-Program", [
            "Emergency response",
            "Seed distribution",
            "Cultural heritage restoration"
        ])

    # Display corresponding content based on the selected sub-program
    if sub_program_eq == "Emergency response":
        er()

    elif sub_program_eq == "Seed distribution":
        seed_distribution()

    elif sub_program_eq == "Cultural heritage restoration":
        chp()

elif program_type ==  "Cultural Heritage Preservation":
        chp()        
