# Week 6 Lab: Design Patterns

In this lab you will implement three design patterns in the context of a simplified Pokemon Go-style spawn system.

- Observer to  notify players when a Pokemon appears at a spawn point
- Strategy to sort nearby Pokemon in different ways
- Decorator to log calls to `SpawnPoint.spawn()`

The files in this lab are:

- `observer.py` implement this first
- `strategy.py` implement this second
- `decorator.py` implement this third
- `main.py` provided, run this once all three parts are done


## Part 1: Observer `observer.py`

The Observer pattern lets objects subscribe to a subject so they are notified automatically when something changes. `SpawnPoint` is the subject which records nearby Pokemon and notifies subscribed observers.

`observer.py` already provides `Spawn`, `Rarity`, and the `Observer` ABC.

`Spawn` is a dataclass with four fields: `name`, `cp` (combat power), `rarity`, and `distance_km`. `Rarity` is defined using `Literal["common", "uncommon", "rare"]`, which tells your type checker that only those three strings are valid values for `rarity`, your IDE will flag any other values as errors.

`Observer` is the interface every observer must implement:

```python
class Observer(ABC):
    @abstractmethod
    def update(self, spawn: Spawn) -> None: ...
```

### Step 1
Implement `SpawnPoint`. `SpawnPoint` represents a fixed location where Pokemon appear. When `spawn()` is called it should:

1. Construct a `Spawn` instance from the arguments
2. Append it to the internal list of pokemon tracked by the `SpawnPoint`
3. Call `update()` on every subscribed observer, passing the new `Spawn`

Two things to be careful about:

- `subscribe()` should not add the same observer instance twice
- `unsubscribe()` should silently do nothing if the observer is not subscribed


### Step 2: Concrete observers
Implement `PlayerAlert` and `RareBroadcast`.

#### `PlayerAlert`

Notifies a named player when any Pokemon spawns. Takes the player's name at construction time and prints:

```
[Alert] <player>: <name> appeared <distance_km>km away (CP <cp>)
```

#### `RareBroadcast`

Prints an alert only when a rare Pokemon spawns:

```
[Rare spawn] <name> appeared <distance_km>km away (CP <cp>)
```

Note: `RareBroadcast` does not need an `__init__` method.


## Part 2: Strategy `strategy.py`

The Strategy pattern defines a family of interchangeable algorithms that can be swapped at runtime. Here, each strategy is a different way of sorting the list of nearby Pokemon.

```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, spawns: list[Spawn]) -> list[Spawn]: ...
```


### Step 1: Concrete strategies
Implement `SortByDistance` and `SortByCP`. A `SortByName` strategy is provided as an example:

```python
class SortByName(SortStrategy):
    def sort(self, spawns: list[Spawn]) -> list[Spawn]:
        return sorted(spawns, key=lambda s: s.name)
```

This strategy extracts the name from each spawn so the list is sorted alphabetically.

Implement the following two strategies using the same approach. Each must return a new sorted list without modifying the original.

- `SortByDistance`: ascending by `distance_km` (closest first)
- `SortByCP`: descending by `cp` (highest first)


### Step 3: `NearbyList`

Implement `__init__`, `generate()` and `set_strategy()` methods in `NearbyList`. `NearbyList` holds a reference to a `SortStrategy` and delegates sorting to it. 

- `generate()` returns the result of calling the `sort()` method on the `SortStrategy`.
- `set_strategy()` swaps in a different strategy at runtime without changing anything else.


## Part 3: Decorator `decorator.py`

Write a `log_spawn` decorator that logs every call to `SpawnPoint.spawn()` so that it prints:

```
[LOG] Town Square: Spawning Pikachu
```

Then apply it to `SpawnPoint.spawn()` in `observer.py`. You will need to access the `args` from the decorator to get the name of the Pokemon.

## Running the Finished System

Once all three parts are complete, run:

```
uv run python main.py
```

The output should show log lines for each spawn, player alerts, rare broadcast alerts, and sorted views of the nearby Pokemon.


## Submission

1. Run the linter: `uv run ruff check`
2. Format your code: `uv run ruff format`
3. Commit and push to GitHub
4. Submit your repository link on Canvas
