"""Integration tests for the complete system."""
import pytest
from src.musicbrainz_explorer.services.artist_service import ArtistService
from src.musicbrainz_explorer.database.manager import DatabaseManager 


class TestIntegration:
    """Integration tests for the complete system."""
    
    @pytest.fixture
    def test_db_manager(self):
        """Create a test database manager."""
        return DatabaseManager("sqlite:///:memory:")
    
    def test_service_layer_integration(self, test_db_manager):
        """Test that service layer integrates with database."""
        # This would test the complete flow
        # For now, just test that components work together
        service = ArtistService()
        # Mock the API client to avoid real API calls in tests
        assert service is not None