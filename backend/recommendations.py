import spotipy
from models import TrackModel
import random

def get_mood_recommendations(token: str, seed_genre: str, limit: int = 9, offset:int = 0):
    try:
        sp = spotipy.Spotify(auth=token)
        query = f"genre:{seed_genre.lower().strip()}"
        
        results = sp.search(q=query, type='track', offset=offset)
        
        tracks_list = results.get('tracks', {}).get('items', [])
        
        if not tracks_list:
            print(f"Warning: No tracks found for query: {query}")
            return []

        random.shuffle(tracks_list)
        
        final_tracks = []

        for item in tracks_list[:limit]:
            final_tracks.append(TrackModel(
                id=item['id'],
                name=item['name'],
                artist=item['artists'][0]['name'],
                album_name=item['album']['name'],
                image_url=item['album']['images'][0]['url'] if item['album']['images'] else None,
                uri=item['uri']
            ))
            
        return final_tracks

    except Exception as e:
        print(f"Error in Search-based Recommendations: {e}")
        return []