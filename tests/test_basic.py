"""Basic tests for MusicBrainz Explorer."""
from musicbrainz_explorer import __version__

def test_version():
    assert __version__ == "0.1.0"

def test_imports():
    # Test that we can import main components
    from musicbrainz_explorer import MusicBrainzClient, Artist
    assert MusicBrainzClient is not None
    assert Artist is not None