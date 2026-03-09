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
        # TODO: implement this method
        ...

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
        # TODO: implement this method
        ...

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
        # TODO: implement this method
        ...
