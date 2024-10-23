import streamlit as st
import numpy as np  # for generating random progress values

def global_overview():
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
        .text {
            font-size: 18px;
            color: #555555;
            margin-bottom: 30px;
            
        /* Adjust the padding around the content */
        .block-container {
            padding: 2rem 1rem;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Title
    st.markdown("<div class='title'>Sustainable Livelihoods</div>", unsafe_allow_html=True)
    
    # Introduction text
    st.markdown("<div class='intro-text'>This page contains data and visualizations for the sustainable livelihoods program.</div>", unsafe_allow_html=True)

    # Define the action data with goals and progress
    actions = {
        "Local Product Certification": {
            "Register High Atlas Harvest": {"goal": 1, "progress": np.random.randint(0, 1)},
            "Support certification of 100 additional cooperatives": {"goal": 100, "progress": np.random.randint(20, 70)},
            "Designate 200 local products": {"goal": 200, "progress": np.random.randint(100, 200)}
        },
        "Rural Entrepreneurship": {
            "Provide business boot-camp training": {"goal": 200, "progress": np.random.randint(50, 100)},
            "Train 15 enterprise coordinators": {"goal": 15, "progress": np.random.randint(10, 15)},
            "Capacity building in consumer research": {"goal": 50, "progress": np.random.randint(30, 50)}
        },
        "Innovation of Goods and Services": {
            "Identify and market 200 novel goods": {"goal": 200, "progress": np.random.randint(10, 60)},
            "Develop mobile and other payment service provider options": {"goal": 5, "progress": np.random.randint(1, 4)},
            "Establishment of transport services": {"goal": 7, "progress": np.random.randint(3, 6)}
        },
        "Digital Entrepreneurship": {
            "Create E-commerce websites": {"goal": 150, "progress": np.random.randint(70, 150)},
            "Support operations of the Digital Tiliwizi marketplace": {"goal": 1000, "progress": np.random.randint(300, 750)},
            "Organize 15-day editions of Harvest Festival": {"goal": 10, "progress": np.random.randint(5, 9)}
        }
    }

    # Displaying the data with progress bars and comments
    for axis, action_items in actions.items():
        st.markdown(f"<div class='summary-title'>{axis}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='text'>{'Include data about the actions done'}</div>", unsafe_allow_html=True)
        for action, data in action_items.items():
            progress_percentage = int((data['progress'] / data['goal']) * 100)
            st.write(f"{action} (Goal: {data['goal']}, Progress: {data['progress']})")
            st.progress(progress_percentage / 100)
            
            # Comment to provide feedback on progress
            if data['progress'] >= data['goal']:
                st.write("✅ Action completed.")
            else:
                st.write(f"Progress: {data['progress']} out of {data['goal']}. Keep going!")

            st.write("")  # Add space between progress bars for clarity
