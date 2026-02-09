#!/usr/bin/env python3


from typing import Generator, Self


class Item:
    """A collectible item in the game."""

    def __init__(self, name: str, value: int, quantity: int = 1) -> None:
        self.name = name
        self.value = value
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"Item('{self.name}', value={self.value}, qty={self.quantity})"

    def __ne__(self, other: Self) -> bool:
        if not isinstance(other, Item):
            return True
        return self.name != other.name

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Item):
            return False
        return self.name == other.name

    def __hash__(self) -> str:
        return hash((self.name))


class Weapon:
    """A weapon that can be equipped."""

    def __init__(self, name: str, damage: int, durability: int = 100) -> None:
        self.name = name
        self.damage = damage
        self.durability = durability

    def attack(self) -> str:
        """Perform an attack with this weapon."""
        if self.durability <= 0:
            return f"{self.name} is broken!"
        self.durability -= 10
        return f"Attacked with {self.name} for {self.damage} damage!"

    def __repr__(self) -> str:
        return f"Weapon('{self.name}', dmg={self.damage}, dur={self.durability})"

    def __eq__(self, value: Self):
        return self.name == value.name

    def __hash__(self):
        return hash((self.name))


class Enemy:
    """An enemy that Link can encounter."""

    def __init__(self, name: str, health: int, strength: int) -> None:
        self.name = name
        self.health = health
        self.strength = strength

    def attack(self) -> str:
        """Enemy performs an attack."""
        return f"{self.name} attacks for {self.strength} damage!"

    def __repr__(self) -> str:
        return f"Enemy('{self.name}', hp={self.health}, str={self.strength})"

    def __hash__(self) -> str:
        return hash((self.name, self.health, self.strength))

    def __eq__(self, other: Self):
        return self.name == other.name

    def __ne__(self, other: Self):
        return self.name != other.name

    def __lt__(self, other: Self):
        return self.strength < other.strength

    def __gt__(self, other: Self):
        return self.strength > other.strength

    def __le__(self, other: Self):
        return self.strength <= other.strength

    def __ge__(self, other: Self):
        return self.strength >= other.strength


class Inventory:
    """Link's inventory."""

    def __init__(self) -> None:
        self._items: list[Item] = []

    def add_item(self, item: Item) -> None:
        """Add an item to the inventory."""
        self._items.append(item)

    def iter_valuable(self, value: int) -> Generator[Item, None, None]:
        for item in self._items:
            if item.value > value:
                yield item

    def __getitem__(self, index: int | slice) -> Item | list[Item]:
        return self._items[index]

    def __setitem__(self, index: int, item: Item) -> None:
        if index < 0:
            index += len(self._items)
        if index < 0 or index >= len(self._items):
            raise IndexError("Inventory index out of range")
        self._items[index] = item

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Generator[Item, None, None]:
        for item in self._items:
            yield item

    def __contains__(self, target: Item | str) -> bool:
        if isinstance(target, Item):
            for item in self._items:
                if item == target:
                    return True
        elif isinstance(target, str):
            for item in self._items:
                if item.name == target:
                    return True
        else:
            raise TypeError(
                "Cannot try __contains__ on Inventory with that type. Must be <str> or <Item>"
            )
        return False


class Dungeon:
    """A dungeon containing rooms."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._rooms: list[Self] = []

    def add_room(self, room: Self) -> None:
        """Add a room to the dungeon."""
        self._rooms.append(room)

    def iter_uncleared(self) -> Generator[Self, None, None]:
        for room in self._rooms:
            if not room.cleared:
                yield room

    def __getitem__(self, index: int | slice) -> Self | list[Self]:
        return self._rooms[index]

    def __len__(self) -> int:
        return len(self._rooms)

    def __iter__(self) -> Generator[Self, None, None]:
        for room in self._rooms:
            yield room

    def __contains__(self, target: str | Self) -> bool:
        if isinstance(target, str):
            for room in self._rooms:
                if room.name == target:
                    return True
        elif isinstance(target, Self):
            for room in self._rooms:
                if room.name == target.name:
                    return True
        else:
            raise TypeError(
                "Cannot try __contains__ on Dungeon with that type. Must be <str> or <Room>"
            )
        return False


class Room:
    """A room in a dungeon."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._enemies: list[Enemy] = []
        self._items: list[Item] = []
        self.cleared = False

    def __repr__(self) -> str:
        return (
            f"Room('{self.name}', enemies={len(self._enemies)}, cleared={self.cleared})"
        )

    def add_enemy(self, enemy: Enemy) -> None:
        """Add an enemy to the room."""
        self._enemies.append(enemy)

    def add_item(self, item: Item) -> None:
        """Add an item to the room."""
        self._items.append(item)

    def __bool__(self) -> bool:
        return not self.cleared and len(self._enemies) > 0


if __name__ == "__main__":
    print("Zelda Protocols!")
