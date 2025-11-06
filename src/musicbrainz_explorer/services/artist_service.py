"""Service layer for artist operations."""
from typing import List, Optional
import logging

from ..database.repositories import ArtistRepository
from ..models.domain import Artist
from ..api.client import MusicBrainzClient
from ..database.manager import db_manager

class ArtistService:
    """Service for artist-related business logic."""
    
    def __init__(self):
        self.api_client = MusicBrainzClient("MusicBrainzExplorer", "admin@example.com")
        self.logger = logging.getLogger(__name__)
    
    def fetch_and_store_artist(self, mbid: str) -> Optional[Artist]:
        """Fetch artist from API and store in database."""
        try:
            with db_manager.get_session() as session:
                repo = ArtistRepository(session)
                
                # Check if already in database
                existing = repo.get_by_mbid(mbid)
                if existing:
                    self.logger.info(f"Artist {mbid} already exists in database")
                    return self._db_to_domain(existing)
                
                # Fetch from API
                api_artist = self.api_client.get_artist(mbid)
                if not api_artist:
                    self.logger.error(f"Artist {mbid} not found in MusicBrainz")
                    return None
                
                # Store in database
                db_artist = repo.create(api_artist)
                self.logger.info(f"Successfully stored artist {mbid} in database")
                return self._db_to_domain(db_artist)
                
        except Exception as e:
            self.logger.error(f"Error in fetch_and_store_artist for {mbid}: {e}")
            return None
    
    def get_stored_artists(self) -> List[Artist]:
        """Get all artists stored in the database."""
        with db_manager.get_session() as session:
            repo = ArtistRepository(session)
            db_artists = repo.list_artists()
            return [self._db_to_domain(artist) for artist in db_artists]
    
    def get_artists_by_country(self, country: str) -> List[Artist]:
        """Get artists by country from database."""
        with db_manager.get_session() as session:
            repo = ArtistRepository(session)
            db_artists = repo.get_artists_by_country(country)
            return [self._db_to_domain(artist) for artist in db_artists]
    
    def get_popular_tags(self, limit: int = 10) -> List[dict]:
        """Get most popular tags from database."""
        with db_manager.get_session() as session:
            repo = ArtistRepository(session)
            return repo.get_popular_tags(limit)
    
    def _db_to_domain(self, db_artist) -> Artist:
        """Convert database model to domain model."""
        return Artist(
            mbid=db_artist.mbid,
            name=db_artist.name,
            country=db_artist.country,
            type=db_artist.type,
            tags=[tag.name for tag in db_artist.tags]
        )