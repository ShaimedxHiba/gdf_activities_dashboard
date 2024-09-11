import streamlit as st
from programs.eq_response import eq_response
from programs.regenerative_approaches.seed_distribution import seed_distribution
from programs.regenerative_approaches.nurseries_animal_shelters import nurseries_animal_shelters
from programs.harvest_festival import harvest_festival
from programs.sustainable_livelihoods import sustainable_livelihoods

# Sidebar navigation
st.sidebar.title("GDF Activities Dashboard")
program_selection = st.sidebar.radio("Select Program", [
    "EQ Response",
    "Regenerative Approaches",
    "Harvest Festival",
    "Sustainable Livelihoods Program"
])

# Conditional page loading
if program_selection == "EQ Response":
    eq_response()

elif program_selection == "Regenerative Approaches":
    # Sub-program selection for Regenerative Approaches
    sub_program_selection = st.sidebar.radio("Select Sub-Program", [
        "Seed Distribution",
        "Nurseries and Animal Shelters"
        
    ])

    if sub_program_selection == "Seed Distribution":
        seed_distribution()
    
    elif sub_program_selection == "Nurseries and Animal Shelters":
        nurseries_animal_shelters()
    
    

elif program_selection == "Harvest Festival":
    harvest_festival()

elif program_selection == "Sustainable Livelihoods Program":
    sustainable_livelihoods()
