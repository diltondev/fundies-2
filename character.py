from abc import ABC, abstractmethod
from exceptions import InvalidLivesError, InvalidCoinsError, CharacterDeadError

class Character(ABC):
    total_characters = 0

    def __init__(self, name: str, lives: int = 3, speed: float = 1.0) -> None:
        pass
