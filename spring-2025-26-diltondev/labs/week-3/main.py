#!/usr/bin/env python3

"""Main program demonstrating the Pokemon battle system."""

from pokemon import Pokemon, FireType, WaterType
from trainer import Trainer


def battle(trainer1: Trainer, trainer2: Trainer) -> Trainer | None:
    """Simulate a battle between two trainers. Returns the winning trainer."""
    print(f"\n---Battle: {trainer1.name} vs {trainer2.name}---")

    pokemon1 = trainer1.get_first_available()
    pokemon2 = trainer2.get_first_available()

    if not pokemon1 or not pokemon2:
        print("One or both trainers have no available Pokemon!")
        return None

    print(f"{trainer1.name} sends out {pokemon1.name}!")
    print(f"{trainer2.name} sends out {pokemon2.name}!")
    print(f"\n{pokemon1.name} vs {pokemon2.name}!\n")

    while True:
        # Pokemon 1 attacks
        damage = pokemon1.calculate_damage(pokemon2)
        print(pokemon1.attack_move())
        pokemon2.take_damage(damage)
        print(f"{pokemon2.name} takes {damage} damage!")
        print(pokemon2)

        if pokemon2.is_fainted():
            print(f"\n{pokemon2.name} fainted!")
            print(f"\n{trainer1.name} wins!")
            return trainer1

        print()

        # Pokemon 2 attacks
        damage = pokemon2.calculate_damage(pokemon1)
        print(pokemon2.attack_move())
        pokemon1.take_damage(damage)
        print(f"{pokemon1.name} takes {damage} damage!")
        print(pokemon1)

        if pokemon1.is_fainted():
            print(f"\n{pokemon1.name} fainted!")
            print(f"\n{trainer2.name} wins!")
            return trainer2

        print()


def main() -> None:
    """Run the Pokemon battle simulation."""
    # Create trainers
    ash = Trainer("Ash")
    gary = Trainer("Gary")

    # Create Pokemon
    charmander = FireType("Charmander", 39, 12, 8, "Ember", 10, 0.2)
    pikachu = Pokemon("Pikachu", 35, 11, 7, "Quick Attack", 10)
    squirtle = WaterType("Squirtle", 44, 9, 10, "Water Gun", 10, 5)
    eevee = Pokemon("Eevee", 55, 10, 8, "Tackle", 10)

    # Build teams
    ash.add_to_team(charmander)
    ash.add_to_team(pikachu)
    gary.add_to_team(squirtle)
    gary.add_to_team(eevee)

    # Display team info
    print("---Team Descriptions---")
    print(ash)
    for pokemon in ash.team:
        print(f"* {pokemon.description()}")

    print()
    print(gary)
    for pokemon in gary.team:
        print(f"* {pokemon.description()}")

    # Start battle
    battle(ash, gary)


if __name__ == "__main__":
    main()
