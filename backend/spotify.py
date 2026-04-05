import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

def get_auth_manager():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-read-private user-top-read",
        cache_path=".spotify_cache"
    )