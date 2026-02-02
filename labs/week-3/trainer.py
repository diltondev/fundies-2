#!/usr/bin/env python3

"""Trainer class for managing a team of Pokemon."""

from pokemon import Pokemon, FireType, WaterType


class Trainer:
    """A Pokemon trainer who manages a team of Pokemon."""

    max_team_size: int
    name: str
    team: list[Pokemon]

    def __init__(self, name: str) -> None:
        """Initialise a new Trainer."""
        self.max_team_size = 6
        self.name = name
        self.team = []

    def add_to_team(self, pokemon: Pokemon) -> bool:
        """Add a Pokemon to the trainer's team.

        Returns True if successful, False if team is full.
        """
        if self.get_team_size() >= self.max_team_size:
            return False
        self.team.append(pokemon)

    def get_team_size(self) -> int:
        """Get the number of Pokemon in the team."""
        return len(self.team)

    def get_first_available(self) -> Pokemon | None:
        """Get the first non-fainted Pokemon in the team."""
        for pokemon in self.team:
            if not pokemon.is_fainted():
                return pokemon
        return None

    def get_pokemon_by_type(self, pokemon_type: type) -> list[Pokemon]:
        """Get a list of all Pokemon in the team that are instances of pokemon_type."""
        return [pokemon for pokemon in self.team if isinstance(pokemon, pokemon_type)]

    def __str__(self) -> str:
        """Return a string representation of this Trainer."""
        return f"{self.name} ({self.get_team_size()}/{self.max_team_size} Pokemon)"


def test_get_one_pokemon_by_type() -> None:
    """Test the get_pokemon_by_type method of the Trainer class."""

    trainer = Trainer("Test Trainer")
    charmander = FireType("Charmander", 39, 52, 43, "Ember", 40, 0.1)

    trainer.add_to_team(charmander)

    fire_pokemon = trainer.get_pokemon_by_type(FireType)
    assert len(fire_pokemon) == 1
    assert charmander in fire_pokemon

    staryu = WaterType("Staryu", 30, 9, 11, "Swift", 15, 7)
    trainer.add_to_team(staryu)
    water_pokemon = trainer.get_pokemon_by_type(WaterType)
    assert len(water_pokemon) == 1
    assert staryu in water_pokemon


def test_get_no_pokemon_by_type() -> None:
    from pokemon import WaterType

    trainer = Trainer("Test Trainer")
    charmander = FireType("Charmander", 39, 52, 43, "Ember", 40, 0.1)

    trainer.add_to_team(charmander)

    water_pokemon = trainer.get_pokemon_by_type(WaterType)
    assert len(water_pokemon) == 0


def test_get_multiple_pokemon_by_type() -> None:
    from pokemon import WaterType

    trainer = Trainer("Test Trainer")
    squirtle = WaterType("Squirtle", 44, 48, 65, "Water Gun", 40, 30)
    psyduck = WaterType("Psyduck", 50, 52, 48, "Confusion", 50, 25)

    trainer.add_to_team(squirtle)
    trainer.add_to_team(psyduck)

    water_pokemon = trainer.get_pokemon_by_type(WaterType)
    assert len(water_pokemon) == 2
    assert squirtle in water_pokemon
    assert psyduck in water_pokemon
