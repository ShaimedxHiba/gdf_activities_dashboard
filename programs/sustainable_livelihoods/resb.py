import streamlit as st


def resb():
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
     
     st.markdown('<div class="title">Rural Entrepreneurship Skill Building</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Boot-camps (200 cooperative members)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Mentorship programme (200 rural entrepreneurs)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">High Atlas trade markets (15)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Rural enterprise coordinators training (7)</div>', unsafe_allow_html=True)
     st.markdown('<div class="summary-title">Consumer research capacity building (7 rural enterprise coordinators and 50 cooperatives managers)</div>', unsafe_allow_html=True)