"""Discography display."""

import time

from itunes_api import ITunesAPI
from models import Album, Artist


class Discography:
    """Holds an artist and their albums and displays the full track listing."""

    def __init__(self, artist: Artist, albums: list[Album]) -> None:
        self.artist = artist
        self.albums = albums

    # Step 1: load_all_tracks

    def load_all_tracks(self, api: ITunesAPI) -> None:
        """Fetch tracks for every album via the API.

        For each album:
        1. Print: Loading tracks for "<album name>"...
        2. Call api.get_tracks() with the album's collection_id
        3. Assign the result to album.tracks
        4. Sleep 3 seconds to respect the rate limit (use time.sleep)
        """
        # TODO
        ...

    # Step 2: display

    def display(self) -> None:
        """Print every album followed by its track listing.

        Format each album heading using its __str__, then for each track
        print a line like:

           1. Rolling in the Deep        3:48

        Hint: use an f-string with padding to align the columns, e.g.
          f"  {track.track_number:>2}. {track.name:<30} {track.duration_formatted}"
        """
        # TODO
        ...
