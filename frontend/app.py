import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("OCTO-AI")

if st.button("Request Login Link from Backend"):
    try:
        response = requests.get(f"{BACKEND_URL}/get-auth-link")
        response.raise_for_status()
        data = response.json()

        auth_link = data["auth_url"]
        st.markdown(f"[Click here to authenticate]({auth_link})")

    except Exception as e:
        st.error(f"Failed to get auth link: {e}")

st.divider()

st.subheader("Verify Token")
user_token = st.text_input("Enter token")

if st.button("Verify Token"):
    response = requests.get(f"{BACKEND_URL}/check-user", params={"token": user_token})
    response.raise_for_status()

    result = response.json()
    if result["status"] == "success":
        st.success(f"Backend verified user: {result['user']}")
    else:
        st.error(result["message"])