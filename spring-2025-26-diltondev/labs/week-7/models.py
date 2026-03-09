"""Model classes for iTunes Search API results."""


class Track:
    """A single track from an album."""

    def __init__(
        self,
        track_id: int,
        name: str,
        track_number: int,
        duration_ms: int,
        preview_url: str,
    ) -> None:
        self.track_id = track_id
        self.name = name
        self.track_number = track_number
        self.duration_ms = duration_ms
        self.preview_url = preview_url

    @classmethod
    def from_dict(cls, data: dict) -> "Track":
        return cls(
            track_id=data["trackId"],
            name=data["trackName"],
            track_number=data.get("trackNumber", 0),
            duration_ms=data.get("trackTimeMillis", 0),
            preview_url=data.get("previewUrl", ""),
        )

    @property
    def duration_formatted(self) -> str:
        """Convert milliseconds to M:SS format."""
        total_seconds = self.duration_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"

    def __str__(self) -> str:
        return f"{self.name} ({self.duration_formatted})"

    def __repr__(self) -> str:
        return f"Artist(artist_id={self.artist_id}, name='{self.name}', genre='{self.genre}')"


# Step 1: Implement Artist

class Artist:
    """An artist returned by the search endpoint.

    Attributes:
        artist_id (int): unique iTunes artist ID
        name (str): display name
        genre (str): primary genre
    """

    
    def __init__(self, artist_id: int, name: str, genre: str) -> None:
        self.artist_id = artist_id
        self.name = name
        self.genre = genre

    @classmethod
    def from_dict(cls, data: dict) -> "Artist":
        return cls(
            artist_id=data.get("artistId"),
            name=data.get("artistName", "Unknown"),
            genre=data.get("primaryGenreName", "Unknown")
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.genre})"

    def __repr__(self) -> str:
        return f"Artist(artist_id={self.artist_id}, name='{self.name}')"



# Step 2: Implement Album

class Album:
    """An album returned by the lookup endpoint.

    Attributes:
        collection_id (int): unique iTunes collection ID
        name (str): album title
        artist_name (str): artist display name
        track_count (int): number of tracks
        release_year (int): four-digit year e.g. 2011
        genre (str): primary genre
        artwork_url (str): URL to 100x100 artwork
        tracks (list[Track]): populated later by the API client
    """

    def __init__(
        self, 
        collection_id: int, 
        name: str, 
        artist_name: str, 
        track_count: str, 
        release_year: int,
        genre: str,
        artwork_url: str
    ) -> None:
        self.collection_id = collection_id
        self.name = name
        self.artist_name = artist_name
        self.track_count = track_count
        self.release_year = release_year
        self.genre = genre
        self.artwork_url = artwork_url
        self.tracks: list[Track] = []

    @classmethod
    def from_dict(cls, data: dict) -> "Album":
        return cls(
            collection_id=data.get("collectionId"),
            name=data.get("collectionName"),
            artist_name=data.get("artistName"),
            track_count=data.get("trackCount"),
            release_year=str(data.get("releaseDate")).strip()[:4],
            genre=data.get("primaryGenreName"),
            artwork_url=data.get("artworkUrl100")
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.release_year}) - {self.track_count} tracks"

    def __repr__(self) -> str:
        return f"Album(collection_id={self.collection_id}, name='{self.name}')"
