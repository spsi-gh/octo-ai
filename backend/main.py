from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware #cross origin resource sharing
from spotify import get_auth_manager
import spotipy
from fastapi.responses import RedirectResponse
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #replace "*" with streamlit link
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_manager = get_auth_manager()

@app.get("/get-auth-link")
def get_auth_link():
    url = auth_manager.get_authorize_url()
    return {"auth_url": url}    

#redirect with access code to frontend
@app.get("/callback")
def callback(code:str):
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
        return {"status":"error", "message": "Invalid token"}
    

#add cache to save token
@app.get("/check-cache")
def check_cache():
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
    cache_path = ".spotify_cache"
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
