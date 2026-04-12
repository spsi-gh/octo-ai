from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #cross origin resource sharing
from spotify import get_auth_manager
import spotipy
from fastapi.responses import RedirectResponse
import os
from models import TrackModel, TopTrackResponse, MoodMapping, MoodMappingResponse
from google import genai
from mood_engine import search_mood
from recommendations import get_mood_recommendations
from fastapi import Body

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #replace "*" with streamlit link
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get-auth-link")
def get_auth_link():
    auth_manager = get_auth_manager()
    url = auth_manager.get_authorize_url()
    return {"auth_url": url}    

#redirect with access code to frontend
@app.get("/callback")
def callback(code:str):
    auth_manager = get_auth_manager()
    token_info = auth_manager.get_access_token(code=code)
    access_token = token_info["access_token"]

    return RedirectResponse(url=f"http://127.0.0.1:8501/?token={access_token}")


#check if the token is valid
@app.get("/check-user")
def check_user(token:str):
    try:    
        sp = spotipy.Spotify(auth=token)
        user_info = sp.current_user()

        return {
            "status": "success",
            "user": user_info["display_name"],
            "image": user_info["images"][0]["url"] if user_info["images"] else None
        }
    except Exception as e:
        print(f"Error in check_user{e}")
        return {"status":"error", "message": "Invalid token"}
    

#add cache to save token
@app.get("/check-cache")
def check_cache():
    auth_manager = get_auth_manager()
    token_info = auth_manager.get_cached_token()

    if token_info:
        #check if it is not expired
        if not auth_manager.is_token_expired(token_info=token_info):
            return{
                "status":"success",
                "token":token_info['access_token']
            }
    return {
        "status":"error",
        "message":"No cache found"
    }

#logout to clear cache
@app.get("/logout")
def logout():
    cache_path = ".cache"
    if os.path.exists(cache_path):
        os.remove(cache_path)
        return {
            "status":"success",
            "message":"Logged out Successfully."
        }
        
    return{
        "status":"error",
        "message":"No cache found."
    }


# # creating end point for top-tracks
# @app.get("/top-tracks", response_model=TopTrackResponse)
# def get_top_tracks(token:str, limit: int = 10, time_range:str = "long_term"):
#     try:
#         sp = spotipy.Spotify(auth=token)
#         results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
#         items = results.get('items', [])

#         track_list=[]
#         for item in items:
#             # Inside your loop in main.py
#             track_data = TrackModel(
#                 id=item['id'],
#                 name=item['name'],
#                 artist=item['artists'][0]['name'],
#                 album_name=item['album']['name'],
#                 image_url=item['album']['images'][0]['url'] if item['album']['images'] else None,
#                 preview_url=item.get('preview_url'),  #preview is unsupported now
#                 uri=item['uri']
#             )   
#             track_list.append(track_data)
#         return {
#             "status":"success",
#             "tracks":track_list
#         }
#     except Exception as e:
#         print("DETAILED ERROR")
#         print(f"Error Type: {type(e).__name__}")
#         print(f"Error Message: {e}")
        
#         return {
#             "status": "error",
#             "message": str(e) if str(e) else "Check Backend Terminal for details",
#             "tracks": []
#         }   


@app.get("/map-mood", response_model=MoodMappingResponse)
def map_mood(mood_text: str):
    ai_result = search_mood(mood_text=mood_text)
    
    if ai_result: 
        return {"status":"success", **ai_result.model_dump()}
    else:
        return{
            "status":"error",
            "valence":0.5,
            "energy":0.5,
            "seed_genre":"indie",
            "reason":"AI unavailable."
        }
    

@app.get("/get-vibe-tracks", response_model=TopTrackResponse)
def get_vibe_tracks(token: str, seed_genre: str, offset:int = 0):
    tracks = get_mood_recommendations(token, seed_genre, offset=offset)
    if tracks:
        return {
            "status":"success",
            "tracks":tracks
        }
    return {
        "status":"error",
        "tracks":[]
    }


@app.post("/save-playlist")
def save_playlist(token: str, mood_name: str, track_uris: list = Body(...)):
    try:
        sp = spotipy.Spotify(auth=token)
        # user_id = sp.me()['id']

        playlist_name = f"Octo AI: {mood_name.title()} Vibe"
        playlist = sp.current_user_playlist_create(
            # user=user_id,
            name=playlist_name,
            public=True,    
            description="Created by Octo AI"
        )
        
        print(playlist['id'])
        sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)

        return{
            "status":"success", 
            "playlist_url":playlist['external_urls']['spotify']
        }

    except Exception as e:
        print(f"Error saving playlist: {e}")
        return {"status": "error", "message":str(e)}