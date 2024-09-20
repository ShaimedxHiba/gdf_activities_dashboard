import streamlit as st
from programs.eq_response.chp import chp
from programs.eq_response.er import er
from programs.regenerative_approaches.seed_distribution import seed_distribution
from programs.regenerative_approaches.nurseries_animal_shelters import nurseries_animal_shelters
from programs.regenerative_approaches.plant_distribution import plant_distribution
from programs.regenerative_approaches.its import its
from programs.regenerative_approaches.pastoralists import pastoralists
from programs.harvest_festival import harvest_festival
from programs.sustainable_livelihoods.global_overview import global_overview
from programs.sustainable_livelihoods.cooperatives import cooperatives
from programs.sustainable_livelihoods.action_coop import action_coop

# Sidebar navigation
st.sidebar.title("GDF/MBLA Activities Dashboard")
program_selection = st.sidebar.radio("Select Program", [
    "EQ Response",
    "Regenerative Approaches",
    "Harvest Festival",
    "Sustainable Livelihoods Program"
])

# Conditional page loading
if program_selection == "EQ Response":
    # Sub-program selection for EQ response
    sub_program_selection = st.sidebar.radio("Select Sub-Program", [
        "Cultural Heritage Preservation",
        "Emergency Response"
       
        
        
    ])

    if sub_program_selection == "Cultural Heritage Preservation":
        chp()
    
    elif sub_program_selection == "Emergency Response":
        er()

elif program_selection == "Regenerative Approaches":
    # Sub-program selection for Regenerative Approaches
    sub_program_selection = st.sidebar.radio("Select Sub-Program", [
        "Seed Distribution",
        "Nurseries and Animal Shelters",
        "Plant Distribution",
        "Irrigation, Terracing and Soil Fertility",
        "Transhuman Pastoralists"

        
    ])

    if sub_program_selection == "Seed Distribution":
        seed_distribution()
    
    elif sub_program_selection == "Nurseries and Animal Shelters":
        nurseries_animal_shelters()

    elif sub_program_selection == "Plant Distribution":
        plant_distribution()

    elif sub_program_selection == "Irrigation, Terracing and Soil Fertility":
        its()

    elif sub_program_selection == "Transhuman Pastoralists":
        pastoralists()            
    
    

elif program_selection == "Harvest Festival":
    harvest_festival()

elif program_selection == "Sustainable Livelihoods Program":
    sub_program_selection = st.sidebar.radio("Select Sub-Section", [
        "Global Overview",
        "Cooperatives",
        "Actions Done"       
    ])
    if sub_program_selection == "Global Overview":
        global_overview()
    
    elif sub_program_selection == "Cooperatives":
        cooperatives()

    elif sub_program_selection == "Actions Done":
        action_coop()    
