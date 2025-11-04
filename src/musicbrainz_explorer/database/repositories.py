"""Repository layer for database operations."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from ..models.database import ArtistDB, TagDB
from ..models.domain import Artist

class ArtistRepository:
    """Repository for artist database operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_mbid(self, mbid: str) -> Optional[ArtistDB]:
        """Get artist by MusicBrainz ID."""
        return self.session.query(ArtistDB).filter(ArtistDB.mbid == mbid).first()
    
    def create(self, artist: Artist) -> ArtistDB:
        """Create a new artist from domain model."""
        # Check if artist already exists
        existing = self.get_by_mbid(artist.mbid)
        if existing:
            return existing
        
        # Create database artist
        db_artist = ArtistDB(
            mbid=artist.mbid,
            name=artist.name,
            country=artist.country,
            type=artist.type
        )
        
        # Add tags
        for tag_name in artist.tags:
            tag = self.session.query(TagDB).filter(TagDB.name == tag_name).first()
            if not tag:
                tag = TagDB(name=tag_name)
            db_artist.tags.append(tag)
        
        self.session.add(db_artist)
        return db_artist
    
    def list_artists(self, skip: int = 0, limit: int = 100) -> List[ArtistDB]:
        """List artists with pagination."""
        return self.session.query(ArtistDB).offset(skip).limit(limit).all()
    
    def get_artists_by_country(self, country: str) -> List[ArtistDB]:
        """Get artists by country."""
        return self.session.query(ArtistDB).filter(ArtistDB.country == country).all()
    
    def get_popular_tags(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular tags across all artists."""
        result = self.session.query(
            TagDB.name, 
            func.count(TagDB.name).label('count')
        ).group_by(TagDB.name).order_by(desc('count')).limit(limit).all()
        
        return [{"name": name, "count": count} for name, count in result]