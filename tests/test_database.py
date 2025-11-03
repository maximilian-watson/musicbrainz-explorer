#!/usr/bin/env python3
"""Test the database setup."""
import sys
import os

# Add your project to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import from the correct location
from config.database import db_manager
from src.musicbrainz_explorer.models.database import ArtistDB

def test_database():
    print("🧪 Testing database setup...")
    
    # Create tables
    db_manager.create_tables()
    print("✅ Tables created successfully!")

    # Use a UNIQUE MBID each time
    import uuid
    unique_mbid = f"test-{uuid.uuid4()}"  # Random unique ID
    
    # Test adding an artist
    with db_manager.get_session() as session:
        artist = ArtistDB(
            mbid=unique_mbid, 
            name="Test Artist",
            country="US",
            type="Group"
        )
        session.add(artist)
        print("✅ Artist added to database!")
    
    # Test reading the artist back
    with db_manager.get_session() as session:
        artist = session.query(ArtistDB).filter_by(mbid=unique_mbid).first()
        if artist:
            print(f"✅ Found artist: {artist.name} from {artist.country}")
        else:
            print("❌ Could not find artist")
    
    print("🎉 Database test completed!")

if __name__ == "__main__":
    test_database()