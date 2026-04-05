import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("OCTO-AI")

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

if "token" in st.session_state: 
    try:
        response = requests.get(f"{BACKEND_URL}/check-user", params={"token": st.session_state.token})
        result = response.json()

        if result.get("status") == "success":
            st.success(f"Verified as {result['user']}")
            # st.image(result["image"])

            #-----------------------------------------#

            st.divider()
            st.header("You Top Tracks")
            limit = st.slider("Number of tracks", 5, 50, 10)

            if st.button("Fetch Top Tracks"):   
                with st.spinner("Analyzing your music DNA..."):
                    track_res = requests.get(f"{BACKEND_URL}/top-tracks",
                                             params={"token": st.session_state.token, "limit":limit})
                    
                    data = track_res.json()

                    if data.get("status") == "success":
                        tracks = data.get("tracks", [])
                        
                        if not tracks:
                            st.warning("No")

                        for track in tracks:
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                if track['image_url']:
                                    st.image(track['image_url'])
                            with col2:
                                st.subheader(track['name'])
                                st.caption(f"Artist: {track['artist']} | Album: {track['album_name']}")
                                track_url = f"https://open.spotify.com/track/{track['id']}"
                                st.link_button("Play on Spotify", track_url)
                    else:   
                        st.error(f"Error : {data.get('message')}")

            #-----------------------------------------#

            #log out
            if st.button("LogOut"):
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

