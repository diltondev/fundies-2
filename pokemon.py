#!/usr/bin/env python3

"""Pokemon classes for the battle system."""

import random


class Pokemon:
    """Base class for all Pokemon."""

    def __init__(
        self,
        name: str,
        max_hp: int,
        attack: int,
        defence: int,
        move: str,
        move_power: int,
    ) -> None:
        """Initialise a new Pokemon."""
        pass

    def take_damage(self, amount: int) -> None:
        """Reduce current_hp by amount (minimum 0)."""
        self.current_hp = max(0, self.current_hp - amount)

    def calculate_damage(self, defender: "Pokemon") -> int:
        """Calculate damage dealt to defender.

        Damage is a random value between 85% and 100% of max damage.
        Minimum damage is 1.
        """
        max_damage = int((self.attack / defender.defence) * self.move_power)
        min_damage = int(max_damage * 0.85)
        return max(1, random.randint(min_damage, max_damage))

    def is_fainted(self) -> bool:
        """Check if the Pokemon has fainted."""
        pass

    def attack_move(self) -> str:
        """Return the attack message for this Pokemon."""
        pass

    def description(self) -> str:
        """Return a description of this Pokemon."""
        pass

    def __str__(self) -> str:
        """Return a string representation of this Pokemon."""
        pass


class FireType(Pokemon):
    """A Fire type Pokemon."""

    def __init__(
        self,
        name: str,
        max_hp: int,
        attack: int,
        defence: int,
        move: str,
        move_power: int,
        burn_chance: float,
    ) -> None:
        """Initialise a new Fire type Pokemon."""
        pass

    def description(self) -> str:
        """Return a description of this Fire type Pokemon."""
        pass


class WaterType(Pokemon):
    """A Water type Pokemon."""

    def __init__(
        self,
        name: str,
        max_hp: int,
        attack: int,
        defence: int,
        move: str,
        move_power: int,
        swim_speed: int,
    ) -> None:
        """Initialise a new Water type Pokemon."""
        pass

    def description(self) -> str:
        """Return a description of this Water type Pokemon."""
        pass
