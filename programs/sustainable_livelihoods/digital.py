import streamlit as st


def digital():
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


     
     st.markdown('<div class="title">Digital Entrepreneurship and Platforms for Local Product Marketing</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">E-com websites and social media (150 cooperatives)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Digital Tiwizi (1000 products, 200 cooperatives)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Harvest festival (10)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Graphic design interns (50)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Communications campaign</div>', unsafe_allow_html=True)