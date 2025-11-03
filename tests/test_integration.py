#!/usr/bin/env python3
"""Test API client and database integration."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.database import db_manager
from src.musicbrainz_explorer.models.database import ArtistDB
from src.musicbrainz_explorer.api.client import MusicBrainzClient

def test_integration():
    print("🧪 Testing API + Database Integration...")
    
    # Create tables
    db_manager.create_tables()
    print("✅ Database tables ready")
    
    # Create API client
    client = MusicBrainzClient("MusicBrainzExplorer", "test@example.com")
    print("✅ API client created")
    
    # Test with a real MusicBrainz ID (The Beatles)
    beatles_mbid = "b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d"
    
    try:
        # Fetch from API
        print("📡 Fetching artist from MusicBrainz API...")
        artist = client.get_artist(beatles_mbid)
        
        if artist:
            print(f"✅ API returned: {artist.name}")
            
            # Save to database
            with db_manager.get_session() as session:
                db_artist = ArtistDB(
                    mbid=artist.mbid,
                    name=artist.name,
                    country=artist.country,
                    type=artist.type
                )
                session.add(db_artist)
                print("💾 Saved to database!")
            
            # Verify it's in database
            with db_manager.get_session() as session:
                saved_artist = session.query(ArtistDB).filter_by(mbid=beatles_mbid).first()
                if saved_artist:
                    print(f"✅ Database has: {saved_artist.name} ({saved_artist.country})")
                else:
                    print("❌ Not found in database")
        else:
            print("❌ API returned no artist data")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("🎉 Integration test completed!")

if __name__ == "__main__":
    test_integration()