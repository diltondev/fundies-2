#!/usr/bin/env python3


class Item:
    """A collectible item in the game."""

    def __init__(self, name: str, value: int, quantity: int = 1) -> None:
        self.name = name
        self.value = value
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"Item('{self.name}', value={self.value}, qty={self.quantity})"


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


class Inventory:
    """Link's inventory."""

    def __init__(self) -> None:
        self._items: list[Item] = []

    def add_item(self, item: Item) -> None:
        """Add an item to the inventory."""
        self._items.append(item)


class Dungeon:
    """A dungeon containing rooms."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._rooms: list["Room"] = []

    def add_room(self, room: "Room") -> None:
        """Add a room to the dungeon."""
        self._rooms.append(room)


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


if __name__ == "__main__":
    print("Zelda Protocols!")
