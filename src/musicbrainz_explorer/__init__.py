"""MusicBrainz Explorer - A toolkit for music data analysis."""

__version__ = "0.1.0"

from .api.client import MusicBrainzClient
from .models.domain import Artist

# Export main from CLI for the poetry script
from .cli import main