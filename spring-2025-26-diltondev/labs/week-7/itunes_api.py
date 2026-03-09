"""Client for the iTunes Search API."""

import requests

from models import Album, Artist, Track

SEARCH_URL = "https://itunes.apple.com/search"
LOOKUP_URL = "https://itunes.apple.com/lookup"
COUNTRY = "GB"


class ITunesAPI:
    """Wraps all HTTP interaction with the iTunes Search API.

    Every method in this class should:
    - use requests.get() with a timeout of 10 seconds
    - call response.raise_for_status() to catch HTTP errors
    - parse the JSON with response.json()
    - return model objects, never raw dictionaries
    """

    # Step 1: search_artist

    def search_artist(self, term: str, limit: int = 5) -> list[Artist]:
        """Search for artists matching *term*.

        Send a GET request to the search endpoint with these parameters:
            term   = term
            entity = musicArtist
            country = GB
            limit  = limit

        Return a list of Artist objects built with Artist.from_dict().
        """
        response = requests.get(SEARCH_URL, params = {
            "term": term,
            "entity": "musicArtist",
            "country": COUNTRY,
            "limit": limit,
        }, timeout=10)
        response.raise_for_status()
        data = response.json()
        artists: list[Artist] = []
        for artist in data["results"]:
            artists.append(Artist.from_dict(artist))
        return artists
            

    # Step 2: get_albums

    def get_albums(self, artist_id: int) -> list[Album]:
        """Fetch albums for the given artist ID.

        Send a GET request to the lookup endpoint with:
            id      = artist_id
            entity  = album
            country = GB

        The first result is the artist. Filter it out by keeping only
        items where wrapperType == "collection".

        Return a list of Album objects.
        """
        response = requests.get(LOOKUP_URL,
                                params={
                                    "id": artist_id,
                                    "entity": "album",
                                    "country": COUNTRY,
                                })
        response.raise_for_status()
        data = response.json()
        albums: list[Album] = []
        if "results" not in data:
            raise ValueError("Results not found in get_albums() call")
        for item in data["results"]:
            if not "wrapperType" in item or item["wrapperType"] != "collection":
                continue
            albums.append(Album.from_dict(item))
        return albums
            

    # Step 3: get_tracks

    def get_tracks(self, collection_id: int) -> list[Track]:
        """Fetch tracks for the given album (collection) ID.

        Send a GET request to the lookup endpoint with:
            id      = collection_id
            entity  = song
            country = GB

        The first result is the album. Filter it out by keeping only
        items where wrapperType == "track".

        Return a list of Track objects.
        """
        response = requests.get(LOOKUP_URL,
                                params={
                                    "id": collection_id,
                                    "entity": "song",
                                    "country": COUNTRY,
                                })
        response.raise_for_status()
        data = response.json()
        tracks: list[Track] = []
        if "results" not in data:
            raise ValueError("Results not found in get_tracks() call")
        for item in data["results"]:
            if not "wrapperType" in item or item["wrapperType"] != "track":
                continue
            tracks.append(Track.from_dict(item))
        return tracks