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
        for album in self.albums:
            print(f'Loading tracks for "{album.name}"')
            for track in api.get_tracks(collection_id=album.collection_id):
                album.tracks.append(track)
            print(f'Fetched all tracks for "{album.name}"')
            time.sleep(1)

    # Step 2: display

    def display(self) -> None:
        """Print every album followed by its track listing.

        Format each album heading using its __str__, then for each track
        print a line like:

           1. Rolling in the Deep        3:48

        Hint: use an f-string with padding to align the columns, e.g.
          f"  {track.track_number:>2}. {track.name:<30} {track.duration_formatted}"
        """
        for album in self.albums:
            print(f"\n{str(album)}")
            for track in sorted(album.tracks, key=lambda x: x.track_number):
                print(
                    f"  {track.track_number:>2}. {track.name:<30} {track.duration_formatted}"
                )
