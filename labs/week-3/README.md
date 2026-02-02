# Week 3 Lab: Inheritance and Composition

This lab will help you practice inheritance, polymorphism, and composition by building a simplified Pokemon battle system. You will:

- Create a base `Pokemon` class with shared attributes and methods
- Extend it with type-specific subclasses that override behaviour (polymorphism)
- Compose Pokemon into a `Trainer` class that manages a team (composition)

Work in pairs to think through the problem, start by looking at `main.py` to understand how the program works. You will be implementing the classes for the Pokemon and the Trainers. Since there are multiple classes, it might help you to create a UML diagram of the system to think about interactions between objects in the program first.

## Simplifications

In the real Pokemon games, each Pokemon can learn up to four moves. For this lab, we have simplified this so that each Pokemon has only a single move that is specified when it is created.

## Damage Calculation

In the real Pokemon games, damage is calculated using a formula that considers the attacker's Attack stat, the defender's Defence stat, the move's base power, and a random modifier. We use a simplified version:

```
max_damage = (attacker.attack / defender.defence) * move_power
damage = random value between 85% and 100% of max_damage
```

The random modifier adds unpredictability to battles (like the original games). The result is rounded down to a whole number, with a minimum of 1 damage (so attacks always do something).

For example, if Charmander (attack: 12) uses Ember (power: 40) against Squirtle (defence: 10):
```
max_damage = (12 / 10) * 10 = 12
damage = random value between 10 and 12
```

The `calculate_damage` and `take_damage` methods are already implemented for you inside the `Pokemon` class.

## Files in This Lab

- `pokemon.py` - Contains the base `Pokemon` class and type subclasses (partially implemented)
- `trainer.py` - Contains the `Trainer` class that manages a team of Pokemon (to be implemented)
- `main.py` - **Provided** - Creates trainers, builds teams, and runs a battle

You will need to add the following files:

- `test_pokemon.py` - Unit tests for the Pokemon class hierarchy
- `test_trainer.py` - Unit tests for the Trainer class

## Tasks

### Part 1: Pokemon Base Class

Open `pokemon.py` and implement the `Pokemon` class:

```python
class Pokemon:
    def __init__(
        self,
        name: str,
        max_hp: int,
        attack: int,
        defence: int,
        move: str,
        move_power: int,
    ) -> None:
        pass
```

#### Attributes

- `name` - the Pokemon's name
- `max_hp` - maximum health points
- `current_hp` - current health points (initialises with the same value as `max_hp`)
- `attack` - attack stat
- `defence` - defence stat
- `move` - the name of the Pokemon's attack
- `move_power` - the base power of the Pokemon's attack

#### Methods

1. `is_fainted()` - returns `True` if `current_hp` is 0
1. `attack_move()` - returns `"<name> uses <move>!"` (e.g., `"Eevee uses Tackle!"`)
1. `description()` - returns `"<name> is a Normal type"` (subclasses will override this)
1. `__str__()` - returns `"<name> (<current_hp>/<max_hp> HP)"`


Already implemented:

1. `take_damage(amount)` - reduces `current_hp` by `amount`
1. `calculate_damage(defender)` - calculates damage dealt to the defender

### Part 2: Type Subclasses

In the same file, create two subclasses that inherit from `Pokemon`. Each subclass should:

- Call `super().__init__()` to initialise the base attributes
- Add one unique attribute specific to that type
  - `burn_chance` for `FireType`
  - `swim_speed` for `WaterType`
- Override the `description()` method to return type-specific information (this is polymorphism — same method name, different behaviour)

#### FireType

```python
class FireType(Pokemon):
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
        pass
```

- Call `super().__init__()` passing all base attributes
- Add `burn_chance` attribute (float between 0 and 1)
- Override `description()` to return `"<name> is a Fire type with <burn_chance>% burn chance"` (e.g., `"Charmander is a Fire type with 20% burn chance"`)

#### WaterType

```python
class WaterType(Pokemon):
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
        pass
```

- Call `super().__init__()` passing all base attributes
- Add `swim_speed` attribute
- Override `description()` to return `"<name> is a Water type with swim speed <swim_speed>"` (e.g., `"Squirtle is a Water type with swim speed 5"`)

#### Sample Pokemon
Use the following sample Pokemon stats for testing:

```python
# Normal types - Pokemon(name, max_hp, attack, defence, move, move_power)
pikachu = Pokemon("Pikachu", 35, 11, 7, "Quick Attack", 10)
eevee = Pokemon("Eevee", 55, 10, 8, "Tackle", 10)
snorlax = Pokemon("Snorlax", 160, 11, 10, "Body Slam", 20)
meowth = Pokemon("Meowth", 40, 9, 7, "Scratch", 10)

# Fire types - FireType(name, max_hp, attack, defence, move, move_power, burn_chance)
charmander = FireType("Charmander", 39, 12, 8, "Ember", 10, 0.2)
vulpix = FireType("Vulpix", 38, 9, 8, "Flamethrower", 22, 0.1)
ponyta = FireType("Ponyta", 50, 17, 11, "Flame Charge", 12, 0.1)

# Water types - WaterType(name, max_hp, attack, defence, move, move_power, swim_speed)
squirtle = WaterType("Squirtle", 44, 9, 10, "Water Gun", 10, 5)
psyduck = WaterType("Psyduck", 50, 10, 9, "Water Pulse", 15, 4)
staryu = WaterType("Staryu", 30, 9, 11, "Swift", 15, 7)
```

### Part 3: Trainer Class

Open `trainer.py` and implement the `Trainer` class.

This demonstrates **composition** — a "has-a" relationship. A Trainer *has* Pokemon, but a Trainer *is not* a Pokemon. Compare this to Part 2, where `FireType` *is a* `Pokemon` (inheritance).

```python
from pokemon import Pokemon

class Trainer:
    def __init__(self, name: str) -> None:
        pass
```

#### Attributes

- `name` - the trainer's name
- `team` - a list of `Pokemon` objects (starts empty)
- `max_team_size` - set this to the value of `6`  in the `__init__` method, it does not need to be changed

#### Methods

1. `add_to_team(pokemon)` - adds a Pokemon to the team if there's room (max 6); returns `True` if successful, `False` if team is full
2. `get_team_size()` - returns the number of Pokemon in the team
3. `get_first_available()` - returns the first non-fainted Pokemon, or `None` if all fainted
4. `__str__()` - returns `"<name> (<count>/6 Pokemon)"`

#### Get Pokemon by Type

The `get_pokemon_by_type` method should take a type class (like `FireType` or `WaterType`) and returns a list of all Pokemon in the team that are instances of that type. There are multiple ways to filter the `team` list in Python, practice using a list comprehension with a conditional and an for this particular implementation.

Example use:

```python
ash = Trainer("Ash")
ash.add_to_team(FireType("Charmander", 39, 12, 8, "Ember", 40, 0.2))
ash.add_to_team(WaterType("Squirtle", 44, 9, 10, "Water Gun", 40, 5))

water_pokemon = ash.get_pokemon_by_type(WaterType)  # Returns [Squirtle]
```

Add tests covering:

- `get_pokemon_by_type` returns correct Pokemon for `FireType`
- `get_pokemon_by_type` returns correct Pokemon for `WaterType`
- `get_pokemon_by_type` returns empty list when no `Pokemon` of that type exist
- `get_pokemon_by_type` handles a team with multiple `Pokemon` of the same type

### Part 4: Running the Game

A fully implemented `main.py` file has been provided for you. Once you have completed Parts 1-3, you can run the game to test your implementation:

```bash
uv run python main.py
```

Take some time to read through `main.py` to understand how it:

1. Creates two trainers with different names
2. Adds Pokemon to each trainer's team (mix of `Pokemon`, `FireType`, and `WaterType`)
3. Prints each Pokemon's description to demonstrate polymorphism
4. Simulates a battle between the two trainers using a `battle()` function

Example output:

```
---Team Descriptions---
Ash (2/6 Pokemon)
* Charmander is a Fire type with 20% burn chance
* Pikachu is a Normal type

Gary (2/6 Pokemon)
* Squirtle is a Water type with swim speed 5
* Eevee is a Normal type

---Battle: Ash vs Gary---
Ash sends out Charmander!
Gary sends out Squirtle!

Charmander vs Squirtle!

Charmander uses Ember!
Squirtle takes 11 damage!
Squirtle (33/44 HP)

Squirtle uses Water Gun!
Charmander takes 10 damage!
Charmander (29/39 HP)

...

Squirtle fainted!

Ash wins!
```

Note: The damage values will vary slightly each time due to the random modifier in the damage calculation.

### Part 5: Unit Tests

#### test_pokemon.py

Write tests covering:

- Initial `current_hp` equals `max_hp`
- `is_fainted` returns `True` when HP is 0
- `is_fainted` returns `False` when HP is above 0
- `attack_move` returns the correct format with the Pokemon's move
- `__str__` returns the correct format
- `FireType.description()` returns Fire type message
- `WaterType.description()` returns Water type message
- Base `Pokemon.description()` returns Normal type message

Example fixture:

```python
import pytest
from pokemon import Pokemon, FireType, WaterType


@pytest.fixture
def pokemon():
    return Pokemon("Eevee", 55, 10, 8, "Tackle", 40)


@pytest.fixture
def fire_pokemon():
    return FireType("Charmander", 39, 12, 8, "Ember", 40, 0.2)


@pytest.fixture
def water_pokemon():
    return WaterType("Squirtle", 44, 9, 10, "Water Gun", 40, 5)
```

#### test_trainer.py

Write tests covering:

- Team starts empty
- `add_to_team` adds Pokemon successfully
- `add_to_team` returns `False` when team is full (6 Pokemon)
- `get_team_size` returns correct count
- `get_first_available` returns first non-fainted Pokemon
- `get_first_available` skips fainted Pokemon
- `get_first_available` returns `None` when all fainted
- `__str__` returns the correct format

#### Running the Tests

```bash
uv run pytest -v
```

## Submission

> [!IMPORTANT]
> Ensure that you have completed the tests for the application before submission. Feedback will be provided on the basis of your tests.

1. Ensure all tests pass by running `uv run pytest -v`
2. Review your code for style and clarity
3. Run the linter: `uv run ruff check`
4. Format your code: `uv run ruff format`
5. Commit and push to GitHub
6. Submit the link for your lab directory on GitHub on Canvas for feedback
