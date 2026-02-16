# Week 5 Lab: Abstract Classes

This lab will help you practice abstract base classes, properties with validation, and custom exceptions by building a Mario character system.

> [!IMPORTANT]
> This week, there is a fully written test file inside the lab exercise, run the tests as you complete each feature to ensure that you have a proper implementation. The test will give you assurance that the your implementation will work with the rest of the system. If you get stuck on getting test to pass, open `test_character.py` and and examine the test to understand the behaviour required to pass.

Files in the lab:

- `exceptions.py` - Custom exception classes
- `character.py` - Abstract `Character` class and concrete subclasses
- `main.py` - Demonstration program (provided)
- `test_character.py` - Unit tests (provided, use to check your work)

## Part 1: Custom Exceptions (`exceptions.py`)

Implement the following exception classes:

1. `CharacterError` - Base exception for all character-related errors
2. `InvalidLivesError` - Raised when lives is outside 0-99
   - Message: `"Lives must be between 0 and 99"`
3. `InvalidCoinsError` - Raised when coins is outside 0-999
   - Message: `"Coins must be between 0 and 999"`
4. `CharacterDeadError` - Raised when using a dead character
   - Message: `"<name> has no lives remaining!"`

## Part 2: Abstract Character Class (`character.py`)

Implement the abstract `Character` class:

### Attributes

- `name` - the character's name (stored in `_name`)
- `lives` - current lives, default 3 (stored in `_lives`)
- `coins` - current coins, starts at 0 (stored in `_coins`)
- `speed` - movement speed multiplier (stored in `_speed`)
- `total_characters` - static variable tracking all characters created

### Properties

| Property   | Validation                                                |
|------------|-----------------------------------------------------------|
| `name`     | Read-only, returns `_name`                                |
| `lives`    | Integer, 0-99, raises `TypeError` or `InvalidLivesError`  |
| `coins`    | Integer, 0-999, raises `TypeError` or `InvalidCoinsError` |
| `is_alive` | Returns `True` if lives > 0                               |

### Concrete Methods

- `__init__()` - This method should increment the `total_characters` static variable
- `collect_coin()` - Add 1 coin; at 100 coins, reset to 0 and gain a life
- `take_damage()` - Lose 1 life; raise `CharacterDeadError` if already dead

### Abstract Methods

- `jump()` - Subclasses implement their jump style
- `run()` - Subclasses implement their run style
- `special_ability()` - Subclasses implement their unique ability

### Class/Static Methods

- `get_total_characters()` - Class method returning total characters created

## Part 3: Concrete Characters

Implement `Mario`, `Luigi`, `Peach`, and `Toad`. Each should:

- Call `super().__init__()` with the character's name and speed
- Implement all abstract methods, each method should return a string from the tables below
- A `CharacterDeadError` should be raised if the `jump()`, `run()` or `special_ability()` methods are used when the `is_alive` property is `False`

| Character | speed | jump                                         |
|-----------|-------|----------------------------------------------|
| Mario     | 1.0   | `"Mario jumps!"`                             |
| Luigi     | 0.9   | `"Luigi jumps higher and floatier!"`         |
| Peach     | 0.85  | `"Peach floats gracefully through the air!"` |
| Toad      | 1.2   | `"Toad does a short but quick jump!"`        |

| Character | run                                    | special_ability             |
|-----------|----------------------------------------|-----------------------------|
| Mario     | `"Mario runs at normal speed!"`        | `"Mario uses fireball!"`    |
| Luigi     | `"Luigi runs with slippery momentum!"` | `"Luigi uses Poltergust!"`  |
| Peach     | `"Peach runs elegantly!"`              | `"Peach uses her parasol!"` |
| Toad      | `"Toad zooms ahead!"`                  | `"Toad uses spore burst!"`  |

## Main

Run the `main.py` file to test that your implementation worked after passing all the tests.

``` bash
uv run main.py
```

## Running Tests

Run the provided tests to check your implementation:

```bash
uv run pytest -v
```

## Submission

1. Ensure all tests pass
2. Run `uv run ruff check` and `uv run ruff format`
3. Commit and push to GitHub
4. Submit your GitHub link on Canvas
