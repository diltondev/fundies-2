#!/usr/bin/env python3

"""Artist Discography Explorer."""

from discography import Discography
from itunes_api import ITunesAPI


def main() -> None:
    api = ITunesAPI()

    term = input("Enter artist name: ").strip()
    if not term:
        print("No search term entered.")
        return

    artists = api.search_artist(term)
    if not artists:
        print(f'No artists found matching "{term}".')
        return

    print("\nSearch results:")
    for i, artist in enumerate(artists, 1):
        print(f"  {i}. {artist}")

    choice = input(f"\nSelect an artist [1-{len(artists)}]: ").strip()
    try:
        artist = artists[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    albums = api.get_albums(artist.artist_id)
    if not albums:
        print(f"No albums found for {artist.name}.")
        return

    print(f"\nAlbums for {artist.name}:")
    for i, album in enumerate(albums, 1):
        print(f"  {i}. {album}")

    disco = Discography(artist, albums)

    print("\nLoading tracks for all albums...")
    disco.load_all_tracks(api)

    print()
    disco.display()


if __name__ == "__main__":
    main()
