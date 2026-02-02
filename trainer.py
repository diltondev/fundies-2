#!/usr/bin/env python3

"""Trainer class for managing a team of Pokemon."""

from pokemon import Pokemon


class Trainer:
    """A Pokemon trainer who manages a team of Pokemon."""


    def __init__(self, name: str) -> None:
        """Initialise a new Trainer."""
        self.max_team_size = 6
        pass

    def add_to_team(self, pokemon: Pokemon) -> bool:
        """Add a Pokemon to the trainer's team.

        Returns True if successful, False if team is full.
        """
        pass

    def get_team_size(self) -> int:
        """Get the number of Pokemon in the team."""
        pass

    def get_first_available(self) -> Pokemon | None:
        """Get the first non-fainted Pokemon in the team."""
        pass

    def get_pokemon_by_type(self, pokemon_type: type) -> list[Pokemon]:
        """Get a list of all Pokemon in the team that are instances of pokemon_type."""
        pass

    def __str__(self) -> str:
        """Return a string representation of this Trainer."""
        pass
