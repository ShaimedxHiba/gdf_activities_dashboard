import streamlit as st
from programs.chp import chp
from programs.pp import pp


# Sidebar navigation
st.sidebar.title("Cultural Heritage Preservation")
program_selection = st.sidebar.radio("Select Program", [
    "Overview",
    "Pilot Project"
])

# Conditional page loading
if program_selection == "Overview":
    chp()

elif program_selection == "Pilot Project":
    pp()
