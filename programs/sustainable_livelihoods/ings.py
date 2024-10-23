import streamlit as st


def ings():
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
     
     st.markdown('<div class="title">Innovation of Novel Goods and Services</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Novel goods and services (200)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Digital ambassadors training (200)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Rural digital marketing agencies (7 hubs)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Mobile and other payment services</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Distribution and transport services (7 hubs)</div>', unsafe_allow_html=True)