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


def test_initial_hp_equals_max_hp(pokemon):
    assert pokemon.current_hp == pokemon.max_hp


def test_is_fainted_returns_true_when_hp_is_zero(pokemon):
    pokemon.current_hp = 0
    assert pokemon.is_fainted() is True


def test_is_fainted_returns_false_when_hp_above_zero(pokemon):
    assert pokemon.is_fainted() is False


def test_attack_move_returns_correct_format(pokemon):
    assert pokemon.attack_move() == "Eevee uses Tackle!"


def test_str_returns_correct_format(pokemon):
    assert str(pokemon) == "Eevee (55/55 HP)"


def test_str_after_taking_damage(pokemon):
    pokemon.current_hp = 30
    assert str(pokemon) == "Eevee (30/55 HP)"


def test_fire_type_description(fire_pokemon):
    assert (
        fire_pokemon.description() == "Charmander is a Fire type with 20% burn chance"
    )


def test_water_type_description(water_pokemon):
    assert water_pokemon.description() == "Squirtle is a Water type with swim speed 5"


def test_base_pokemon_description(pokemon):
    assert pokemon.description() == "Eevee is a Normal type"
