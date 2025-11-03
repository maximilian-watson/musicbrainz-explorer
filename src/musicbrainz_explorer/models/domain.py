"""Domain models for MusicBrainz Explorer."""
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Artist:
    """Artist domain model."""
    mbid: str
    name: str
    country: Optional[str] = None
    type: Optional[str] = None
    tags: List[str] = None
    wikipedia_extract: Optional[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
