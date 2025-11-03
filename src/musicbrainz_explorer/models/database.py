"""SQLAlchemy database models."""
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

# Association table for many-to-many relationship
artist_tags = Table(
    'artist_tags',
    Base.metadata,
    Column('artist_id', String, ForeignKey('artists.mbid')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class ArtistDB(Base):
    """Database model for artists."""
    __tablename__ = "artists"
    
    mbid = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    sort_name = Column(String)
    type = Column(String)  # Person, Group, Orchestra, etc.
    country = Column(String)
    area = Column(String)
    gender = Column(String)
    disambiguation = Column(Text)
    
    # Metadata
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    tags = relationship("TagDB", secondary=artist_tags, back_populates="artists")

class TagDB(Base):
    """Database model for tags."""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    count = Column(Integer, default=1)
    
    # Relationships
    artists = relationship("ArtistDB", secondary=artist_tags, back_populates="tags")
