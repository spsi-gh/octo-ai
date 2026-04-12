import streamlit as st
import requests
import random

BACKEND_URL = "http://127.0.0.1:8000"

st.markdown("<h1 style='text-align: center; color: #EC5800;'>Octo AI</h1>", unsafe_allow_html=True)

def get_tracks(dna, offset=0):
    """Fetch tracks from backend without rendering yet"""
    params = {
        "token": st.session_state.token,
        "seed_genre": dna["seed_genre"],
        "offset": offset,
        "limit": 9
    }
    try:
        res = requests.get(f"{BACKEND_URL}/get-vibe-tracks", params=params)
        data = res.json()
        if data.get("status") == "success":
            return data["tracks"]
    except Exception as e:
        st.error(f"Error fetching tracks: {e}")
    return []

def display_tracks(tracks):
    """Render the track grid"""
    if not tracks:
        st.warning("The Octopus couldn't find any songs for this vibe.")
        return
    
    cols = st.columns(3)
    for idx, track in enumerate(tracks):
        with cols[idx % 3]:
            
            st.image(track['image_url'], use_container_width=True)
            st.markdown(f"**{track['name']}**")
            st.caption(f"{track['artist']}")
            
            st.link_button("Play", f"https://open.spotify.com/track/{track['id']}", use_container_width=True)

try:
    response = requests.get(f"{BACKEND_URL}/check-user", params={"token": st.session_state.token})
    result = response.json()

    if result.get("status") == "success":
        st.sidebar.success(f"Logged in as: {result['user']}")
        
        st.header("Mood Discovery")
        user_mood_ip = st.chat_input("How are you feelin browski UwU")

        if user_mood_ip:
            with st.spinner("Octo is analyzing your vibe..."):
                params = {"mood_text": user_mood_ip}
                mood_res = requests.get(f"{BACKEND_URL}/map-mood", params=params)
                mood_data = mood_res.json()
                
                if mood_data.get("status") == "success":
                    # store everything in session state
                    st.session_state.mood_dna = mood_data
                    st.session_state.current_tracks = get_tracks(mood_data, offset=0)
                else:
                    st.error("AI mapping failed.")

        if "mood_dna" in st.session_state and "current_tracks" in st.session_state:
            dna = st.session_state.mood_dna
            
            st.subheader("Found your DNA")
            m1, m2, m3 = st.columns(3)
            m1.metric("Valence", dna["valence"])
            m2.metric("Energy", dna["energy"])
            m3.metric("Genre Seed", dna["seed_genre"].title())
            st.info(f"Octo says: {dna['reason']}")

            st.divider()
            st.subheader("Your Personalized Playlist")

            if st.button("Regenerate Vibe 🐙", use_container_width=True):
                with st.spinner("Shuffling tracks..."):
                    random_offset = random.randint(1,80)
                    st.session_state.current_tracks = get_tracks(dna, offset=random_offset)
                    st.rerun()

            display_tracks(st.session_state.current_tracks)
            
            st.divider()
            if st.button("Save this Playlist to Spotify 💚", use_container_width=True):
                track_uris = [track['uri'] for track in st.session_state.current_tracks]
                mood_name = st.session_state.mood_dna['seed_genre'] 

                with st.spinner("Creating you playlist.."):
                    save_params = {
                        "token":st.session_state.token,
                        "mood_name":mood_name
                    }
                    save_res = requests.post(
                        f"{BACKEND_URL}/save-playlist",
                        params=save_params,
                        json=track_uris
                    )

                    save_data = save_res.json()
                    
                    if save_data.get("status") == "success":
                        st.balloons()
                        st.success("Playlist saved succesfully!")
                        st.link_button("Open in Spotify", save_data["playlist_url"], use_container_width=True)
                    else:
                        st.error(f"Failed to save: {save_data.get('message')}")
                        
        with st.sidebar:
            st.divider()
            st.write("### Controls")
            
            # just reset the app view
            if st.button("New Vibe", use_container_width=True, help="Clear the current mood and start fresh"):
                if "mood_dna" in st.session_state:
                    del st.session_state.mood_dna
                if "current_tracks" in st.session_state:
                    del st.session_state.current_tracks
                st.rerun()

            # session termination
            if st.button("Log Out", key="logout_btn", use_container_width=True, type="secondary"):
                with st.spinner("Logging out..."):
                    try:
                        requests.get(f"{BACKEND_URL}/logout") 
                    except:
                        pass
                    
                    keys_to_clear = ["token", "mood_dna", "current_tracks"]
                    for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]
                    
                    st.rerun()

    else:
        st.error("Session expired.")
        requests.get(f"{BACKEND_URL}/logout")
        del st.session_state.token
        st.rerun()

except Exception as e:
    st.error(f"Could not connect to backend: {e}")