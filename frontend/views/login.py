import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"


st.markdown("<br><br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<h1 style='text-align: center; color: #EC5800;'>Octo AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Connect your Spotify account to begin.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    try:
        # Fetch the link from backend   
        response = requests.get(f"{BACKEND_URL}/get-auth-link")
        auth_link = response.json()["auth_url"]

        # 3. The Streamlit Tool: st.link_button
        # use_container_width=True makes it fill the center column perfectly
        st.link_button(
            label="Connect your Spotify", 
            url=auth_link, 
            use_container_width=True,
            type="primary" # Makes it the solid green/primary color
        )

    except Exception as e:  
        st.error(f"Failed to get auth link: {e}")


