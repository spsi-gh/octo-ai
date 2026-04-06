import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.markdown("<h1 style='text-align: center; color: #EC5800;'>Octo AI</h1>", unsafe_allow_html=True)

try:
    response = requests.get(f"{BACKEND_URL}/check-user", params={"token": st.session_state.token})
    result = response.json()

    if result.get("status") == "success":
        st.success(f"Verified as {result['user']}")
        st.header("Mood Discovery")
        user_mood_ip = st.chat_input("How are you feelin browski UwU")

        if user_mood_ip:
            with st.spinner("Getting my paws up there ..."):
                try:
                    params = {"mood_text": user_mood_ip}
                    mood_res = requests.get(f"{BACKEND_URL}/map-mood", params=params)
                    mood_data = mood_res.json()
                    # st.write(mood_data) 
                    if(mood_data.get("status") == "success"):
                        st.subheader("Found your DNA")

                        m1, m2, m3 = st.columns(3)
                        m1.metric("Valence ", mood_data["valence"])
                        m2.metric("Energy", mood_data["energy"])
                        m3.metric("Genre Seed", mood_data["seed_genre"].title())

                        st.info(f"Octo : {mood_data["reason"]} !")
                    else:
                        st.error("AI mapping failed.")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
        
        
        with st.sidebar:
        # log out
            if st.button("LogOut", key="logout_btn"):
                try:
                    requests.get(f"{BACKEND_URL}/logout")  #remove cache
                except:
                    pass
            
                del st.session_state.token #remove from session state
                st.rerun()
    else:
        st.error("You session has expired. Pls login again.")
        try:
            requests.get(f"{BACKEND_URL}/logout")  #remove cache
        except:
            pass

        del st.session_state.token
        st.rerun()

except Exception as e:
    st.error(f"Could not connect to backend {e}")