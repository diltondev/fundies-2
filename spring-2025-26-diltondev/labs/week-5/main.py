from character import Character, Mario, Luigi, Peach, Toad
from exceptions import CharacterDeadError, InvalidLivesError


def main():
    # Create characters
    mario = Mario()
    luigi = Luigi(lives=5)
    peach = Peach()
    toad = Toad()

    # Demonstrate polymorphism - same method, different behaviour
    print("--- Character Actions ---")
    characters = [mario, luigi, peach, toad]
    for character in characters:
        print(character.jump())

    print()
    for character in characters:
        print(character.special_ability())

    # Demonstrate coin collection
    print("\n--- Coin Collection ---")
    for i in range(100):
        result = mario.collect_coin()
        if i < 3 or i == 99:
            print(result)
        elif i == 3:
            print("...")

    # Demonstrate damage and exception handling
    print("\n--- Damage and Exceptions ---")
    test_luigi = Luigi(lives=2)

    print(test_luigi.take_damage())
    print(test_luigi.take_damage())

    try:
        test_luigi.take_damage()
    except CharacterDeadError as e:
        print(f"Error caught: {e}")

    # Demonstrate validation exceptions
    print("\n--- Validation Exceptions ---")
    try:
        invalid_mario = Mario(lives=150)
    except InvalidLivesError as e:
        print(f"Error caught: {e}")

    try:
        peach.coins = -50
    except Exception as e:
        print(f"Error caught: {e}")

    # Demonstrate dead character exception
    print("\n--- Dead Character Cannot Act ---")
    dead_toad = Toad(lives=1)
    dead_toad.take_damage()

    try:
        dead_toad.jump()
    except CharacterDeadError as e:
        print(f"Error caught: {e}")

    # Static variable
    print("\n--- Statistics ---")
    print(f"Total characters created: {Character.get_total_characters()}")


if __name__ == "__main__":
    main()
