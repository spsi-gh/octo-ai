import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("OCTO-AI")

#check for token in url
query_params = st.query_params 

if "token" in query_params:
    st.session_state.token = query_params["token"]
    st.query_params.clear()

if "token" in st.session_state: 
    try:
        response = requests.get(f"{BACKEND_URL}/check-user", params={"token": st.session_state.token})
        result = response.json()

        if result["status"] == "success":
            st.success(f"Verified as {result['user']}")
            st.image(result["image"])
            if st.button("LogOut"):
                del st.session_state.token
                st.rerun()
        else:
            st.error("You session has expired. Pls login again.")
            del st.session_state.token
            st.rerun()
    except Exception as e:
        st.error(f"Could not connect to backend {e}")

    
else:
    st.subheader("Connect you Spotify Account")
    
    if st.button("Connect"):
        try:
            response = requests.get(f"{BACKEND_URL}/get-auth-link")
            response.raise_for_status()
            data = response.json()

            auth_link = data["auth_url"]
            st.markdown(f"[Click here to authenticate]({auth_link})")

        except Exception as e:
            st.error(f"Failed to get auth link: {e}")

