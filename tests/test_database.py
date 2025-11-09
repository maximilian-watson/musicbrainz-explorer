"""Database integration tests."""
import pytest
from src.musicbrainz_explorer.models.database import Base, ArtistDB, TagDB
from src.musicbrainz_explorer.database.repositories import ArtistRepository
from src.musicbrainz_explorer.models.domain import Artist
from src.musicbrainz_explorer.database.manager import DatabaseManager

class TestDatabaseIntegration:
    """Integration tests for database operations."""
    
    @pytest.fixture
    def test_db_manager(self):
        """Create a test database manager."""
        return DatabaseManager("sqlite:///:memory:")
    
    @pytest.fixture
    def test_session(self, test_db_manager):
        """Create a test database session."""
        test_db_manager.create_tables()
        with test_db_manager.get_session() as session:
            yield session
    
    def test_artist_creation(self, test_session):
        """Test creating an artist in the database."""
        repo = ArtistRepository(test_session)
        
        artist = Artist(
            mbid="test-mbid-123",
            name="Test Artist",
            country="US",
            type="Person",
            tags=["rock", "alternative"]
        )
        
        db_artist = repo.create(artist)
        test_session.commit()
        
        # Verify artist was created
        retrieved = repo.get_by_mbid("test-mbid-123")
        assert retrieved is not None
        assert retrieved.name == "Test Artist"
        assert len(retrieved.tags) == 2
    
    def test_artist_duplicate_handling(self, test_session):
        """Test that duplicate artists are handled gracefully."""
        repo = ArtistRepository(test_session)
        
        artist = Artist(
            mbid="duplicate-mbid",
            name="Duplicate Artist"
        )
        
        # Create twice
        db_artist1 = repo.create(artist)
        db_artist2 = repo.create(artist)
        
        # Should return the same instance
        assert db_artist1 is db_artist2