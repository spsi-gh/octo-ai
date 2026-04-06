from google import genai
import os
from models import MoodMapping

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def search_mood(mood_text: str):
    try:
        prompt = f"""
        Analyze the following user mood or situation: "{mood_text}"
        
        Your task:
        1. Map this feeling to a musical 'Valence' (0.0=sad/angry, 1.0=happy/cheerful).
        2. Map it to an 'Energy' level (0.0=chill/sleepy, 1.0=intense/workout).
        3. Pick ONE Spotify seed genre (e.g., pop, acoustic, electro, chill, indie, classical, dance).
        4. Provide a 1-sentence reason for your choice.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config={
                "response_mime_type":"application/json",    
                "response_schema": MoodMapping,
            }
        )
        return response.parsed
    
    except Exception as e:
        print(f"Error in Map Mood: {e}")
        return None

