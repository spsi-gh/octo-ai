from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware #cross origin resource sharing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #replace "*" with streamlit link
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-auth-link")
def get_auth_link():
    #dummy url
    return {"auth_url":"https://www.google.com"}    

@app.get("/check-user")
def check_user(token:str):
    #check if the token is valid

    if(token == "token-123"):
        return {"status": "success", "user":"You"}
    return {"status": "error", "message":"Invalid token"}