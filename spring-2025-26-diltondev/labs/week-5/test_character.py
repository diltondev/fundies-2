import pytest
from character import Character, Mario, Luigi, Peach, Toad
from exceptions import (
    CharacterError,
    InvalidLivesError,
    InvalidCoinsError,
    CharacterDeadError,
)


# ============ Exception Tests ============


class TestExceptions:
    def test_all_exceptions_inherit_from_character_error(self):
        assert issubclass(InvalidLivesError, CharacterError)
        assert issubclass(InvalidCoinsError, CharacterError)
        assert issubclass(CharacterDeadError, CharacterError)


# ============ Abstract Class Tests ============


class TestCharacterAbstract:
    def test_character_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            Character("Test", 3, 1.0)


# ============ Character Fixtures ============


@pytest.fixture
def mario():
    return Mario()


@pytest.fixture
def luigi():
    return Luigi()


@pytest.fixture
def peach():
    return Peach()


@pytest.fixture
def toad():
    return Toad()


# ============ Initialisation Tests ============


class TestCharacterInit:
    def test_mario_default_lives(self, mario):
        assert mario.lives == 3

    def test_luigi_custom_lives(self):
        luigi = Luigi(lives=5)
        assert luigi.lives == 5

    def test_initial_coins_is_zero(self, mario):
        assert mario.coins == 0

    def test_mario_name(self, mario):
        assert mario.name == "Mario"

    def test_luigi_name(self, luigi):
        assert luigi.name == "Luigi"

    def test_peach_name(self, peach):
        assert peach.name == "Peach"

    def test_toad_name(self, toad):
        assert toad.name == "Toad"

    def test_mario_speed(self, mario):
        assert mario._speed == 1.0

    def test_luigi_speed(self, luigi):
        assert luigi._speed == 0.9

    def test_peach_speed(self, peach):
        assert peach._speed == 0.85

    def test_toad_speed(self, toad):
        assert toad._speed == 1.2


# ============ Property Validation Tests ============


class TestLivesProperty:
    def test_lives_setter_valid(self, mario):
        mario.lives = 5
        assert mario.lives == 5

    def test_lives_setter_zero_valid(self, mario):
        mario.lives = 0
        assert mario.lives == 0

    def test_lives_setter_max_valid(self, mario):
        mario.lives = 99
        assert mario.lives == 99

    def test_lives_setter_negative_raises_error(self, mario):
        with pytest.raises(InvalidLivesError) as exc_info:
            mario.lives = -1
        assert exc_info.value.value == -1

    def test_lives_setter_too_high_raises_error(self, mario):
        with pytest.raises(InvalidLivesError) as exc_info:
            mario.lives = 100
        assert exc_info.value.value == 100

    def test_lives_setter_wrong_type_raises_error(self, mario):
        with pytest.raises(TypeError):
            mario.lives = "three"

    def test_lives_setter_float_raises_error(self, mario):
        with pytest.raises(TypeError):
            mario.lives = 3.5


class TestCoinsProperty:
    def test_coins_setter_valid(self, mario):
        mario.coins = 50
        assert mario.coins == 50

    def test_coins_setter_zero_valid(self, mario):
        mario.coins = 0
        assert mario.coins == 0

    def test_coins_setter_max_valid(self, mario):
        mario.coins = 999
        assert mario.coins == 999

    def test_coins_setter_negative_raises_error(self, mario):
        with pytest.raises(InvalidCoinsError) as exc_info:
            mario.coins = -1
        assert exc_info.value.value == -1

    def test_coins_setter_too_high_raises_error(self, mario):
        with pytest.raises(InvalidCoinsError) as exc_info:
            mario.coins = 1000
        assert exc_info.value.value == 1000

    def test_coins_setter_wrong_type_raises_error(self, mario):
        with pytest.raises(TypeError):
            mario.coins = "fifty"


# ============ is_alive Tests ============


class TestIsAlive:
    def test_is_alive_with_lives(self, mario):
        assert mario.is_alive is True

    def test_is_alive_with_zero_lives(self, mario):
        mario.lives = 0
        assert mario.is_alive is False


# ============ collect_coin Tests ============


class TestCollectCoin:
    def test_collect_coin_increments(self, mario):
        mario.collect_coin()
        assert mario.coins == 1

    def test_collect_coin_returns_message(self, mario):
        result = mario.collect_coin()
        assert result == "Mario collected a coin! (1/100)"

    def test_collect_coin_extra_life_at_100(self, mario):
        mario.coins = 99
        initial_lives = mario.lives
        result = mario.collect_coin()
        assert mario.coins == 0
        assert mario.lives == initial_lives + 1
        assert "Extra life!" in result

    def test_collect_coin_extra_life_message(self, mario):
        mario.coins = 99
        result = mario.collect_coin()
        assert result == "Mario collected 100 coins! Extra life! (4 lives)"


# ============ take_damage Tests ============


class TestTakeDamage:
    def test_take_damage_reduces_lives(self, mario):
        mario.take_damage()
        assert mario.lives == 2

    def test_take_damage_returns_message_alive(self, mario):
        result = mario.take_damage()
        assert result == "Mario was hit! 2 lives remaining"

    def test_take_damage_returns_message_dead(self, mario):
        mario.lives = 1
        result = mario.take_damage()
        assert result == "Mario was hit! Game over for Mario!"

    def test_take_damage_when_dead_raises_error(self, mario):
        mario.lives = 0
        with pytest.raises(CharacterDeadError) as exc_info:
            mario.take_damage()
        assert exc_info.value.name == "Mario"


# ============ Abstract Method Tests ============


class TestMarioMethods:
    def test_jump(self, mario):
        assert mario.jump() == "Mario jumps!"

    def test_run(self, mario):
        assert mario.run() == "Mario runs at normal speed!"

    def test_special_ability(self, mario):
        assert mario.special_ability() == "Mario uses fireball!"


class TestLuigiMethods:
    def test_jump(self, luigi):
        assert luigi.jump() == "Luigi jumps higher and floatier!"

    def test_run(self, luigi):
        assert luigi.run() == "Luigi runs with slippery momentum!"

    def test_special_ability(self, luigi):
        assert luigi.special_ability() == "Luigi uses Poltergust!"


class TestPeachMethods:
    def test_jump(self, peach):
        assert peach.jump() == "Peach floats gracefully through the air!"

    def test_run(self, peach):
        assert peach.run() == "Peach runs elegantly!"

    def test_special_ability(self, peach):
        assert peach.special_ability() == "Peach uses her parasol!"


class TestToadMethods:
    def test_jump(self, toad):
        assert toad.jump() == "Toad does a short but quick jump!"

    def test_run(self, toad):
        assert toad.run() == "Toad zooms ahead!"

    def test_special_ability(self, toad):
        assert toad.special_ability() == "Toad uses spore burst!"


class TestDeadCharacterMethods:
    def test_jump_when_dead_raises_error(self, mario):
        mario.lives = 0
        with pytest.raises(CharacterDeadError):
            mario.jump()

    def test_run_when_dead_raises_error(self, mario):
        mario.lives = 0
        with pytest.raises(CharacterDeadError):
            mario.run()

    def test_special_ability_when_dead_raises_error(self, mario):
        mario.lives = 0
        with pytest.raises(CharacterDeadError):
            mario.special_ability()


# ============ Class/Static Method Tests ============


class TestClassMethods:
    def test_get_total_characters(self):
        initial = Character.get_total_characters()
        Mario()
        Luigi()
        assert Character.get_total_characters() == initial + 2
