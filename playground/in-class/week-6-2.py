from abc import ABC, abstractmethod
from datetime import datetime
import random


class Song:
    def __init__(self, title: str, artist: str, rating: float):
        self.title = title
        self.artist = artist
        self.rating = rating

    def __repr__(self):
        return f"{self.title} - {self.artist} (rating: {self.rating})"

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, songs: list[Song]) -> list[Song]:
        pass
        
class SortByTitle(SortStrategy):
    def sort(self, songs: list[Song]) -> list[Song]:
        return sorted(songs, key=lambda s: s.title)
    
               
class Logger:
    def log(func):
        def wrapper(self, *args, **kwargs):
            try: 
                print(f'Added new song \'{args[0].title}\' at {datetime.now()}')
            except IndexError:
                print(f'Added new song at {datetime.now()}')
            except Exception as e:
                raise e
            return func(self, *args, **kwargs)
        return wrapper

        
class Playlist:
    def __init__(self, name: str, strategy: SortStrategy):
        self.name = name
        self.strategy = strategy
        self.songs: list[Song] = []

    @Logger.log
    def add(self, song: Song) -> None:
        self.songs.append(song)

    def sort(self) -> None:
        self.songs = self.strategy.sort(self.songs)

    def display(self) -> None:
        print(f"Playlist: {self.name}")
        for i, song in enumerate(self.songs, 1):
            print(f"  {i}. {song}")
            
 

class SortByRating(SortStrategy):
    def sort(self, songs: list[Song]) -> list[Song]:
        return sorted(songs, key=lambda s: s.rating, reverse=True)
        
class ShuffleSort(SortStrategy):
    def sort(self, songs: list[Song]) -> list[Song]:
        shuffled = songs.copy()
        random.shuffle(shuffled)
        return shuffled
    
    
if __name__ == "__main__":
    playlist = Playlist("Island Tunes", SortByTitle())

    playlist.add(Song("K.K. Bossa", "K.K. Slider", 4.5))
    playlist.add(Song("Bubblegum K.K.", "K.K. Slider", 4.9))
    playlist.add(Song("K.K. Cruisin'", "K.K. Slider", 4.2))
    playlist.add(Song("Stale Cupcakes", "K.K. Slider", 4.7))
    playlist.add(Song("K.K. Disco", "K.K. Slider", 3.8))

    # Sort and display the playlist
    playlist.sort()
    playlist.display() 
    
    # Change sort strategy to SortByRating
    playlist.strategy = SortByRating()
    playlist.sort()
    playlist.display()

    # Change sort strategy to ShuffleSort
    playlist.strategy = ShuffleSort()
    playlist.sort()
    playlist.display()
    