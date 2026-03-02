from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

from decorator import log_spawn

Rarity = Literal["common", "uncommon", "rare"]


@dataclass
class Spawn:
    name: str
    cp: int
    rarity: Rarity
    distance_km: float


class Observer(ABC):
    @abstractmethod
    def update(self, spawn: Spawn) -> None:
        ...


class SpawnPoint:
    """Subject that records nearby Pokémon spawns and notifies observers.

    Args:
        name: the name of this spawn point location.
    """

    def __init__(self, name: str) -> None:
        pass  # TODO

    def subscribe(self, observer: Observer) -> None:
        """Add an observer to the notification list."""
        pass  # TODO

    def unsubscribe(self, observer: Observer) -> None:
        """Remove an observer from the notification list."""
        pass  # TODO

    def spawn(self, name: str, cp: int, rarity: Rarity, distance_km: float) -> None:
        """Record a new spawn and notify all subscribed observers."""
        pass  # TODO

    def get_all(self) -> list[Spawn]:
        """Return a list of all recorded spawns."""
        pass  # TODO


class PlayerAlert(Observer):
    """Notifies a named player whenever any Pokémon spawns nearby.

    Args:
        player_name: the name of the player to alert.
    """

    def __init__(self, player_name: str) -> None:
        pass  # TODO

    def update(self, spawn: Spawn) -> None:
        pass  # TODO


class RareBroadcast(Observer):
    """Broadcasts a message when a rare Pokémon spawns.

    Prints nothing for common or uncommon spawns.
    """

    def update(self, spawn: Spawn) -> None:
        pass  # TODO
