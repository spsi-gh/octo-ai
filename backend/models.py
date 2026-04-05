from pydantic import BaseModel
from typing import List, Optional

class TrackModel(BaseModel):
    id: str
    name: str
    artist: str
    album_name: str
    image_url: Optional[str] = None
    preview_url: Optional[str] = None
    uri: str    

class TopTrackResponse(BaseModel):
    status: str
    tracks: List[TrackModel]