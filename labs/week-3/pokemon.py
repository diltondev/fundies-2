#!/usr/bin/env python3

"""Pokemon classes for the battle system."""

import random


class Pokemon:
    """Base class for all Pokemon."""

    name: str
    max_hp: int
    attack: int
    defence: int
    move: str
    move_power: int
    current_hp: int

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
        self.name = name
        self.max_hp = max_hp
        self.attack = attack
        self.defence = defence
        self.move = move
        self.move_power = move_power
        self.current_hp = max_hp

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
        return self.current_hp == 0

    def attack_move(self) -> str:
        """Return the attack message for this Pokemon."""
        return f"{self.name} uses {self.move}!"

    def description(self) -> str:
        """Return a description of this Pokemon."""
        return f"{self.name} is a Normal type"

    def __str__(self) -> str:
        """Return a string representation of this Pokemon."""
        return f"{self.name} ({self.current_hp}/{self.max_hp} HP)"


class FireType(Pokemon):
    """A Fire type Pokemon."""

    burn_chance: float

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
        super().__init__(
            name=name,
            max_hp=max_hp,
            attack=attack,
            defence=defence,
            move=move,
            move_power=move_power,
        )
        self.burn_chance = (
            0 if burn_chance <= 0 else 1 if burn_chance >= 1 else burn_chance
        )

    def description(self) -> str:
        """Return a description of this Fire type Pokemon."""
        return (
            f"{self.name} is a Fire type with {self.burn_chance * 100:.0f}% burn chance"
        )


class WaterType(Pokemon):
    """A Water type Pokemon."""

    swim_speed: int

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
        super().__init__(
            name=name,
            max_hp=max_hp,
            attack=attack,
            defence=defence,
            move=move,
            move_power=move_power,
        )
        self.swim_speed = swim_speed

    def description(self) -> str:
        """Return a description of this Water type Pokemon."""
        return f"{self.name} is a Water type with swim speed {self.swim_speed}"


def test_initialize_pokemon():
    # Normal types - Pokemon(name, max_hp, attack, defence, move, move_power)
    pikachu = Pokemon("Pikachu", 35, 11, 7, "Quick Attack", 10)
    assert pikachu.name == "Pikachu"
    assert pikachu.max_hp == 35
    assert pikachu.attack == 11
    assert pikachu.defence == 7
    assert pikachu.move == "Quick Attack"
    assert pikachu.move_power == 10


def test_description_methods():
    eevee = Pokemon("Eevee", 55, 10, 8, "Tackle", 10)
    assert eevee.description() == "Eevee is a Normal type"

    charmander = FireType("Charmander", 39, 12, 8, "Ember", 10, 0.2)
    assert charmander.description() == "Charmander is a Fire type with 20% burn chance"

    squirtle = WaterType("Squirtle", 44, 9, 10, "Water Gun", 10, 5)
    assert squirtle.description() == "Squirtle is a Water type with swim speed 5"


def test_is_fainted_method():
    bulbasaur = Pokemon("Bulbasaur", 45, 10, 10, "Vine Whip", 10)
    bulbasaur.current_hp = 0
    assert bulbasaur.is_fainted()
    bulbasaur.current_hp = 10
    assert not bulbasaur.is_fainted()


def test_calculate_damage():
    attacker = Pokemon("Attacker", 50, 15, 5, "Strike", 10)
    defender = Pokemon("Defender", 50, 10, 10, "Block", 10)

    # Calculate max and min damage
    max_damage = int((attacker.attack / defender.defence) * attacker.move_power)
    min_damage = int(max_damage * 0.85)

    damage = attacker.calculate_damage(defender)
    assert min_damage <= damage <= max_damage


def test_attack_move():
    meowth = Pokemon("Meowth", 40, 10, 8, "Scratch", 10)
    assert meowth.attack_move() == "Meowth uses Scratch!"
