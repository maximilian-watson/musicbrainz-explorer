"""MusicBrainz API client."""
import requests
import time
from typing import Optional
from ..models.domain import Artist

class MusicBrainzClient:
    """Simple MusicBrainz API client."""
    
    def __init__(self, user_agent: str, email: str):
        self.base_url = "https://musicbrainz.org/ws/2"
        self.headers = {
            'User-Agent': f'{user_agent} ({email})',
            'Accept': 'application/json'
        }
    
    def get_artist(self, mbid: str) -> Optional[Artist]:
        """Get basic artist information."""
        try:
            # Rate limiting
            time.sleep(5.0)
            
            url = f"{self.base_url}/artist/{mbid}"
            params = {
                'fmt': 'json',
                'inc': 'tags'  
            }
            
            response = requests.get(
                url, 
                headers=self.headers, 
                params=params, 
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            return self._parse_artist(data)
            
        except Exception as e:
            print(f"Error fetching artist {mbid}: {e}")
            return None
    
    def _parse_artist(self, data: dict) -> Artist:
        """Parse API response into Artist domain model."""
        tags = []
        if 'tags' in data:
            tags = [tag['name'] for tag in data['tags'] if 'name' in tag]
        
        return Artist(
            mbid=data['id'],
            name=data['name'],
            country=data.get('country'),
            type=data.get('type'),
            tags=tags 
        )
