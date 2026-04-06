from pydantic import BaseModel, Field
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

class MoodMapping(BaseModel):
    valence: float = Field(..., ge=0, le=1)
    energy: float = Field(...,  ge=0, le=1)
    seed_genre: str
    reason: str

class MoodMappingResponse(MoodMapping):
    status: str