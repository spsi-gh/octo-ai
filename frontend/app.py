import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="OCTO AI", layout="wide")
st.logo("assets/octo.png", icon_image="assets/octo.png", size="large")
#check for token in url
if "token" in st.query_params:
    st.session_state.token = st.query_params["token"]
    st.query_params.clear()

#check for token in cache
if "token" not in st.session_state:
    try:
        cache_res = requests.get(f"{BACKEND_URL}/check-cache").json()
        if cache_res.get("status") == "success":
            st.session_state.token = cache_res["token"]
    except:
        pass

if "token" not in st.session_state: 
    login_page = st.Page("views/login.py", title="Login (^///^)")
    pg = st.navigation([login_page])

else:
    mood_page = st.Page("views/mood_discovery.py", title="Mood Discovery (*/ω＼*)")
    pg = st.navigation({"Main":[mood_page]})

pg.run()


#             st.divider()
#             # st.header("You Top Tracks")
#             # limit = st.slider("Number of tracks", 5, 50, 10)

#             # if st.button("Fetch Top Tracks"):   
#             #     with st.spinner("Analyzing your music DNA..."):
#             #         track_res = requests.get(f"{BACKEND_URL}/top-tracks",
#             #                                  params={"token": st.session_state.token, "limit":limit})
                    
#             #         data = track_res.json()

#             #         if data.get("status") == "success":
#             #             tracks = data.get("tracks", [])
                        
#             #             if not tracks:
#             #                 st.warning("No")

#             #             for track in tracks:
#             #                 col1, col2 = st.columns([1, 4])
#             #                 with col1:
#             #                     if track['image_url']:
#             #                         st.image(track['image_url'])
#             #                 with col2:
#             #                     st.subheader(track['name'])
#             #                     st.caption(f"Artist: {track['artist']} | Album: {track['album_name']}")
#             #                     track_url = f"https://open.spotify.com/track/{track['id']}"
#             #                     st.link_button("Play on Spotify", track_url)
#             #         else:   
#             #             st.error(f"Error : {data.get('message')}")

