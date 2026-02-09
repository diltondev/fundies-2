# Week 4 Lab: Protocols

In this lab we will build components for a Zelda-inspired adventure game where you implement protocols to make your game objects work with Python's built-in operations. We have a bit more focus on writing tests this week as the protocols themselves are quite straightforward to implement.

> [!IMPORTANT]
> You must write pytest tests for each exercise before you write your implementation. Writing code this way is known as Test Driven Development, pretend that what you are asked to implement already works and write the assert statements then figure out how to implement each feature after writing the associated test.

There are two files in this lab project:
- `zelda.py` — your game classes
- `test_zelda.py` — your pytest tests

## Part 1: The Sequence Protocol

### 1.1 Indexing the Inventory

Link needs to access items in his inventory by position. Implement `__getitem__` to enable square bracket notation.

**Task:** 
1. Write pytest tests for `__getitem__`
2. Implement `__getitem__` in the `Inventory` class

```python
# Test cases to cover:
# - Access first item with index 0
# - Access last item with index -1
# - Access item attribute (e.g., inventory[1].name)
# - Slicing returns correct items (e.g., inventory[0:2])
# - IndexError raised for invalid index

# Example test structure:
def test_inventory_getitem_first():
    inventory = Inventory()
    inventory.add_item(Item("Rupee", value=1))
    inventory.add_item(Item("Bomb", value=20))
    assert inventory[0].name == "Rupee"

def test_inventory_getitem_negative_index():
    # TODO: Write this test
    pass

def test_inventory_getitem_slicing():
    # TODO: Write this test
    pass

def test_inventory_getitem_empty_index_error():
    """Check that accessing an empty index raises IndexError."""
    inventory = Inventory()
    with pytest.raises(IndexError):
        _ = inventory[0]
```

---

### 1.2 Modifying Items

Link needs to replace items in his inventory. Implement `__setitem__`.

**Task:**
1. Write pytest tests for `__setitem__`
2. Implement `__setitem__` in the `Inventory` class

```python
# Test cases to cover:
# - Replace item at index 0
# - Replace item at negative index
# - Verify the old item is gone and new item is present
# - IndexError raised for invalid index

def test_inventory_setitem_replace():
    # TODO: Write this test
    pass

def test_inventory_setitem_invalid_index_raises_index_error():
    # TODO: Write this test
    pass
```

---

### 1.3 Length

Link needs to know how many items he's carrying.

**Task:**
1. Write pytest tests for `__len__`
2. Implement `__len__` in the `Inventory` class

```python
# Test cases to cover:
# - Empty inventory has length 0
# - Inventory with 3 items has length 3
# - Length updates after adding items
# - Boolean test: empty inventory is falsy, non-empty is truthy

def test_inventory_len_empty():
    # TODO: Write this test
    pass

def test_inventory_len_with_items():
    # TODO: Write this test
    pass

def test_inventory_bool_empty_is_falsy():
    inventory = Inventory()
    assert not inventory  # Should be falsy when empty

def test_inventory_bool_nonempty_is_truthy():
    # TODO: Write this test
    pass
```

---

### 1.4 Iteration

Link wants to examine all items using a `for` loop.

**Task:**
1. Write pytest tests for `__iter__`
2. Implement `__iter__` in the `Inventory` class using a generator (`yield`)

```python
# Test cases to cover:
# - Can iterate over all items
# - Iteration order matches insertion order
# - Empty inventory yields nothing
# - Works with list() conversion

def test_inventory_iter_all_items():
    inventory = Inventory()
    inventory.add_item(Item("Rupee", value=1))
    inventory.add_item(Item("Bomb", value=20))
    
    names = [item.name for item in inventory]
    assert names == ["Rupee", "Bomb"]

def test_inventory_iter_empty():
    # TODO: Write this test
    pass
```

---

### 1.5 Custom Iteration - Valuable Items Generator

Create a method that yields only items above a certain value.

**Task:**
1. Write pytest tests for `iter_valuable()`
2. Implement `iter_valuable()` in the `Inventory` class

```python
# Test cases to cover:
# - Only items >= min_value are yielded
# - Items below threshold are excluded
# - Empty result when no items meet threshold
# - All items returned when threshold is 0

def test_inventory_iter_valuable_filters_correctly():
    inventory = Inventory()
    inventory.add_item(Item("Rupee", value=1))
    inventory.add_item(Item("Heart", value=100))
    inventory.add_item(Item("Bomb", value=20))
    
    valuable = list(inventory.iter_valuable(50))
    assert len(valuable) == 1
    assert valuable[0].name == "Heart"

def test_inventory_iter_valuable_none_match():
    # TODO: Write this test
    pass
```

---

### 1.6 Membership Testing

Link needs to check if he has a specific item by name OR by object.

**Task:**
1. Write pytest tests for `__contains__`
2. Implement `__contains__` in the `Inventory` class

```python
# Test cases to cover:
# - Search by string name returns True when present
# - Search by string name returns False when absent
# - Search by Item object (requires __eq__ to be implemented first)

def test_inventory_contains_by_name_found():
    inventory = Inventory()
    inventory.add_item(Item("Bomb", value=20))
    assert "Bomb" in inventory

def test_inventory_contains_by_name_not_found():
    # TODO: Write this test
    pass

def test_inventory_contains_by_object():
    # TODO: Write this test (may need __eq__ on Item first)
    pass
```

---

## Part 2: Comparison and Hashing

### 2.1 Equality

Two items should be considered equal if they have the same name.

**Task:**
1. Write pytest tests for `__eq__`
2. Implement `__eq__` in the `Item` class

```python
# Test cases to cover:
# - Items with same name are equal (even if different value)
# - Items with different names are not equal
# - Comparing with non-Item returns False or NotImplemented
# - Item is equal to itself (identity)

def test_item_eq_same_name():
    item1 = Item("Rupee", value=1)
    item2 = Item("Rupee", value=50)
    assert item1 == item2

def test_item_eq_different_name():
    # TODO: Write this test
    pass

def test_item_eq_with_string():
    item = Item("Rupee", value=1)
    assert not (item == "Rupee")  # Should not be equal to a string
```

---

### 2.2 Ordering Enemies

We want to sort enemies by their strength for difficulty ranking.

**Task:**
1. Write pytest tests for `__eq__` and `__lt__`
2. Implement both methods in the `Enemy` class

```python
# Test cases to cover:
# - Enemies with same name are equal
# - Enemy with lower strength is less than enemy with higher strength
# - Sorting a list of enemies orders by strength (weakest first)
# - Comparing with non-Enemy returns NotImplemented

def test_enemy_eq_same_name():
    # TODO: Write this test
    pass

def test_enemy_lt_by_strength():
    weak = Enemy("Bokoblin", health=50, strength=10)
    strong = Enemy("Lynel", health=500, strength=50)
    assert weak < strong

def test_enemy_sort_by_strength():
    enemies = [
        Enemy("Lynel", health=500, strength=50),
        Enemy("Bokoblin", health=50, strength=10),
        Enemy("Moblin", health=100, strength=25),
    ]
    enemies.sort()
    names = [e.name for e in enemies]
    assert names == ["Bokoblin", "Moblin", "Lynel"]
```

---

### 2.3 Hashing Items

To use items as dictionary keys or in sets, we need proper hashing.

**Task:**
1. Write pytest tests for `__hash__`
2. Implement `__hash__` in the `Item` class

```python
# Test cases to cover:
# - Equal items have equal hashes
# - Items can be added to a set
# - Duplicate items (same name) only appear once in set
# - Items can be used as dictionary keys

def test_item_hash_equal_items_same_hash():
    item1 = Item("Rupee", value=1)
    item2 = Item("Rupee", value=50)
    assert hash(item1) == hash(item2)

def test_item_hash_in_set():
    item1 = Item("Rupee", value=1)
    item2 = Item("Rupee", value=50)
    item3 = Item("Bomb", value=20)
    
    unique_items = {item1, item2, item3}
    assert len(unique_items) == 2  # Rupee counted once

def test_item_hash_as_dict_key():
    # TODO: Write this test
    pass
```

> [!NOTE]
> Why must `__hash__` use the same attributes as `__eq__`?

---

### 2.4 Hashing Weapons

Link wants to track which weapons he's found using a set. Two weapons are equal if they have the same `name`.

**Task:**
1. Write pytest tests for `__eq__` and `__hash__`
2. Implement both methods in the `Weapon` class

```python
# Test cases to cover:
# - Weapons with same name are equal (regardless of durability)
# - Weapons with different names are not equal
# - Equal weapons have equal hashes
# - Weapons work correctly in sets
# - Weapons work correctly as dictionary keys

def test_weapon_eq_same_name_different_durability():
    sword1 = Weapon("Master Sword", damage=30, durability=100)
    sword2 = Weapon("Master Sword", damage=30, durability=50)
    assert sword1 == sword2

def test_weapon_eq_different_name():
    # TODO: Write this test
    pass

def test_weapon_hash_in_set():
    sword1 = Weapon("Master Sword", damage=30, durability=100)
    sword2 = Weapon("Master Sword", damage=30, durability=50)
    rusty = Weapon("Rusty Sword", damage=5, durability=20)
    
    weapons = {sword1, sword2, rusty}
    assert len(weapons) == 2

def test_weapon_hash_as_dict_key():
    # TODO: Write this test
    pass
```

> [!NOTE]
> Why is it safe to hash by `name` but not by `durability`?

---

## Part 3: The Dungeon System

### 3.1 Room Truthiness

A room should be "truthy" if it has undefeated enemies (not cleared).

**Task:**
1. Write pytest tests for `__bool__`
2. Implement `__bool__` in the `Room` class

```python
# Test cases to cover:
# - Room with enemies and not cleared is truthy
# - Room with enemies but cleared is falsy
# - Empty room is falsy
# - Room becomes falsy after setting cleared = True

def test_room_bool_with_enemies_is_truthy():
    room = Room("Eastern Chamber")
    room.add_enemy(Enemy("Bokoblin", 50, 10))
    assert room  # Should be truthy

def test_room_bool_cleared_is_falsy():
    room = Room("Eastern Chamber")
    room.add_enemy(Enemy("Bokoblin", 50, 10))
    room.cleared = True
    assert not room  # Should be falsy after clearing

def test_room_bool_empty_is_falsy():
    # TODO: Write this test
    pass
```

---

### 3.2 Dungeon Protocols

Implement the full sequence protocol for the `Dungeon` class.

**Task:**
1. Write pytest tests for `__getitem__`, `__len__`, `__iter__`, `__contains__`, and `iter_uncleared()`
2. Implement all methods in the `Dungeon` class

```python
# Test cases to cover for each method:

# __getitem__:
# - Access room by index
# - Negative indexing works

# __len__:
# - Empty dungeon has length 0
# - Dungeon with rooms has correct length

# __iter__:
# - Can iterate over all rooms
# - Order matches insertion order

# __contains__:
# - Search by room name (string)
# - Search by Room object

# iter_uncleared:
# - Only yields rooms where cleared is False
# - Skips cleared rooms

def test_dungeon_getitem():
    dungeon = Dungeon("Forest Temple")
    dungeon.add_room(Room("Entry Hall"))
    dungeon.add_room(Room("Boss Room"))
    assert dungeon[0].name == "Entry Hall"
    assert dungeon[-1].name == "Boss Room"

def test_dungeon_len():
    # TODO: Write this test
    pass

def test_dungeon_iter():
    # TODO: Write this test
    pass

def test_dungeon_contains_by_name():
    dungeon = Dungeon("Forest Temple")
    dungeon.add_room(Room("Boss Room"))
    assert "Boss Room" in dungeon
    assert "Secret Room" not in dungeon

def test_dungeon_iter_uncleared():
    dungeon = Dungeon("Forest Temple")
    room1 = Room("Entry Hall")
    room2 = Room("Boss Room")
    room1.cleared = True
    dungeon.add_room(room1)
    dungeon.add_room(room2)
    
    uncleared = list(dungeon.iter_uncleared())
    assert len(uncleared) == 1
    assert uncleared[0].name == "Boss Room"
```

## Running Your Tests

Run all tests:
```bash
uv run pytest test_zelda.py -v
```

## Submission

> [!IMPORTANT]
> Ensure that you have completed the tests for the application before submission. Feedback will be provided on the basis of your tests.

1. Ensure all tests pass by running `uv run pytest -v`
2. Run the linter: `uv run ruff check`
3. Format your code: `uv run ruff format`
4. Commit and push to GitHub
5. Submit the link for your lab directory on GitHub on Canvas for feedback
