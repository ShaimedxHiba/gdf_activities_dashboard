import streamlit as st


def lpcl():
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


     
     st.markdown('<div class="title">Local Product Certification and Labelling</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">High Atlas Harvest brand and label registration</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Participatory guarantee system establishment (100 cooperatives)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Cooperatives certification support (100 cooperatives)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Improve cooperatives’ visual identity and packaging (200 cooperatives)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Local products label designation (200 products)</div>', unsafe_allow_html=True)
