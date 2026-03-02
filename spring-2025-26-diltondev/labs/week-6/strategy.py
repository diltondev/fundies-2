from abc import ABC, abstractmethod

from observer import Spawn


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, spawns: list[Spawn]) -> list[Spawn]: ...


class SortByName(SortStrategy):
    """Sorts spawns alphabetically by name. Provided as an example."""

    def sort(self, spawns: list[Spawn]) -> list[Spawn]:
        return sorted(spawns, key=lambda s: s.name)


class SortByDistance(SortStrategy):
    """Sorts spawns ascending by distance (closest first)."""

    def sort(self, spawns: list[Spawn]) -> list[Spawn]:
        return sorted(spawns, key=lambda s: s.distance_km)


class SortByCP(SortStrategy):
    """Sorts spawns descending by CP (highest first)."""

    def sort(self, spawns: list[Spawn]) -> list[Spawn]:
        return sorted(spawns, key=lambda s: s.cp, reverse=True)


class NearbyList:
    """Context class that delegates sorting to a strategy.

    The strategy can be swapped at runtime using `set_strategy`.
    """

    _strategy: SortStrategy

    def __init__(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def generate(self, spawns: list[Spawn]) -> list[Spawn]:
        """Return spawns sorted according to the current strategy."""
        return self._strategy.sort(spawns)
