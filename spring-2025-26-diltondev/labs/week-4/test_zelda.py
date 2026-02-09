#!/usr/bin/env python3

import pytest
from zelda import Item, Weapon, Enemy, Inventory, Room, Dungeon


@pytest.fixture
def sample_inventory():
    inventory = Inventory()
    inventory.add_item(Item("Rupee", value=10))
    inventory.add_item(Item("Bomb", value=20))
    inventory.add_item(Item("Cloth", value=1))
    return inventory


# Example test structure:
def test_inventory_getitem_first(sample_inventory):
    inventory = sample_inventory
    assert inventory[0].name == "Rupee"


def test_inventory_getitem_negative_index(sample_inventory):
    inventory = sample_inventory
    assert inventory[-1].name == "Cloth"


def test_inventory_getitem_slicing(sample_inventory):
    inventory = sample_inventory
    assert [item.name for item in inventory[0:2]] == ["Rupee", "Bomb"]


def test_inventory_getitem_empty_index_error():
    """Check that accessing an empty index raises IndexError."""
    inventory = Inventory()
    with pytest.raises(IndexError):
        _ = inventory[0]


# Test cases to cover:
# - Replace item at index 0
# - Replace item at negative index
# - Verify the old item is gone and new item is present
# - IndexError raised for invalid index


def test_inventory_setitem_replace(sample_inventory):
    inventory = sample_inventory
    new_item = Item("Heart Container", value=100)
    second_new_item = Weapon("Bow", damage=15)
    inventory[0] = new_item
    inventory[-1] = second_new_item
    assert inventory[0].name == "Heart Container"
    assert inventory[1].name == "Bomb"
    assert inventory[-1].name == "Bow"


def test_inventory_setitem_invalid_index_raises_index_error(sample_inventory):
    inventory = sample_inventory
    with pytest.raises(IndexError):
        _ = inventory[10]
    with pytest.raises(IndexError):
        inventory[10] = Item("Shield", value=50)


# Test cases to cover:
# - Empty inventory has length 0
# - Inventory with 3 items has length 3
# - Length updates after adding items
# - Boolean test: empty inventory is falsy, non-empty is truthy


def test_inventory_len_empty():
    inventory = Inventory()
    assert len(inventory) == 0


def test_inventory_len_with_items(sample_inventory):
    inventory = sample_inventory
    assert len(inventory) == 3


def test_inventory_bool_empty_is_falsy():
    inventory = Inventory()
    assert not inventory  # Should be falsy when empty


def test_inventory_bool_nonempty_is_truthy(sample_inventory):
    inventory = sample_inventory
    assert inventory


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
    inventory = Inventory()
    names = [item.name for item in inventory]
    assert names == []


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
    inventory = Inventory()
    inventory.add_item(Item("Rupee", value=1))
    inventory.add_item(Item("Bomb", value=20))

    valuable = list(inventory.iter_valuable(50))
    assert len(valuable) == 0
    assert valuable == []


# Test cases to cover:
# - Search by string name returns True when present
# - Search by string name returns False when absent
# - Search by Item object (requires __eq__ to be implemented first)


def test_inventory_contains_by_name_found():
    inventory = Inventory()
    inventory.add_item(Item("Bomb", value=20))
    assert "Bomb" in inventory


def test_inventory_contains_by_name_not_found():
    inventory = Inventory()
    inventory.add_item(Item("Rupee", value=1))
    assert "Bomb" not in inventory


def test_inventory_contains_by_object(sample_inventory):
    rupee = Item("Rupee", value=10)
    bomb = Item("Bomb", value=20)
    sword = Item("Cloth", value=1)
    assert rupee in sample_inventory
    assert bomb in sample_inventory
    assert sword in sample_inventory


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
    item1 = Item("Rupee", value=1)
    item2 = Item("Bomb", value=1)
    assert not (item1 == item2)


def test_item_eq_with_string():
    item = Item("Rupee", value=1)
    assert not (item == "Rupee")  # Should not be equal to a string


# Test cases to cover:
# - Enemies with same name are equal
# - Enemy with lower strength is less than enemy with higher strength
# - Sorting a list of enemies orders by strength (weakest first)
# - Comparing with non-Enemy returns NotImplemented


def test_enemy_eq_same_name():
    enemyA = Enemy("Bokoblin", health=50, strength=10)
    enemyB = Enemy("Bokoblin", health=500, strength=50)
    assert enemyA == enemyB


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
    dic: dict[Item, str] = dict()
    item1 = Item("Rupee", value=1)
    item2 = Item("Bomb", value=20)
    dic[item1] = "Rupee"
    dic[item2] = "Bomb"
    assert dic[item1] == "Rupee"
    assert dic[item2] == "Bomb"


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
    sword1 = Weapon("Master Sword", damage=30, durability=100)
    sword2 = Weapon("The Throngler", damage=30, durability=50)
    assert not (sword1 == sword2)


def test_weapon_hash_in_set():
    sword1 = Weapon("Master Sword", damage=30, durability=100)
    sword2 = Weapon("Master Sword", damage=30, durability=50)
    rusty = Weapon("Rusty Sword", damage=5, durability=20)

    weapons = {sword1, sword2, rusty}
    assert len(weapons) == 2


def test_weapon_hash_as_dict_key():
    dic: dict[Weapon, str] = dict()
    sword1 = Weapon("Master Sword", damage=30, durability=100)
    sword2 = Weapon("The Throngler", damage=30, durability=50)
    dic[sword1] = "Master Sword"
    dic[sword2] = "The Throngler"
    assert dic[sword1] == "Master Sword"
    assert dic[sword2] == "The Throngler"


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
    room = Room("Eastern Chamber")
    assert not room


# Test cases to cover for each method:


# __getitem__:
# - Access room by index
# - Negative indexing works
def test_dungeon_getitem():
    dungeon = Dungeon("Forest Temple")
    dungeon.add_room(Room("Entry Hall"))
    dungeon.add_room(Room("Boss Room"))
    assert dungeon[0].name == "Entry Hall"
    assert dungeon[-1].name == "Boss Room"


# __len__:
# - Empty dungeon has length 0
# - Dungeon with rooms has correct length
def test_dungeon_len():
    dungeon = Dungeon("Forest Temple")
    assert len(dungeon) == 0
    dungeon.add_room(Room("Entry Hall"))
    dungeon.add_room(Room("Boss Room"))
    assert len(dungeon) == 2


# __iter__:
# - Can iterate over all rooms
# - Order matches insertion order
def test_dungeon_iter():
    dungeon = Dungeon("Forest Temple")
    room1 = Room("Entry Hall")
    room2 = Room("Boss Room")
    dungeon.add_room(room1)
    dungeon.add_room(room2)

    rooms = list(dungeon)
    assert len(rooms) == 2
    assert rooms[0].name == "Entry Hall"
    assert rooms[1].name == "Boss Room"


# __contains__:
# - Search by room name (string)
# - Search by Room object
def test_dungeon_contains_by_name():
    dungeon = Dungeon("Forest Temple")
    dungeon.add_room(Room("Boss Room"))
    assert "Boss Room" in dungeon
    assert "Secret Room" not in dungeon


# iter_uncleared:
# - Only yields rooms where cleared is False
# - Skips cleared rooms
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
