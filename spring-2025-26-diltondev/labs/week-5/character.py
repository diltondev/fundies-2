from abc import ABC, abstractmethod
from exceptions import InvalidLivesError, InvalidCoinsError, CharacterDeadError


class Character(ABC):
    _total_characters = 0

    @staticmethod
    def get_total_characters() -> int:
        return Character._total_characters

    _name: str
    _lives: int
    _coins: int
    _speed: float

    @property
    def name(self) -> str:
        return self._name

    @property
    def lives(self) -> int:
        return self._lives

    @lives.setter
    def lives(self, lives: int) -> None:
        if not isinstance(lives, int):
            raise TypeError("Cannot set lives of a Character to a non-int value!")
        if lives < 0 or lives > 99:
            raise InvalidLivesError(lives)
        self._lives = lives

    @property
    def coins(self) -> int:
        return self._coins

    @coins.setter
    def coins(self, coins: int) -> None:
        if not isinstance(coins, int):
            raise TypeError("Cannot set coins of a character to non-int value")
        if coins < 0 or coins > 999:
            raise InvalidCoinsError(coins)
        self._coins = coins
        # while self._coins >= 100:
        #     self._coins -= 100
        #     self._lives += 1

    @property
    def is_alive(self) -> bool:
        return self._lives > 0

    def collect_coin(self) -> str:
        self._coins += 1
        if self._coins >= 100:
            self._coins -= 100
            self._lives += 1
            return (
                f"{self._name} collected 100 coins! Extra life! ({self._lives} lives)"
            )
        return f"{self._name} collected a coin! ({self._coins}/100)"

    def take_damage(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self._name)
        self._lives -= 1
        if self._lives > 0:
            return f"{self._name} was hit! {self._lives} lives remaining"
        else:
            return f"{self._name} was hit! Game over for {self._name}!"

    def __init__(self, name: str, lives: int | None = 3, speed: float = 1.0) -> None:
        Character._total_characters += 1
        if lives is None:
            lives = 3

        if not isinstance(name, str):
            raise TypeError("Cannot create a Character with non-str name!")
        self._name = name
        self.lives = lives
        if not isinstance(speed, float):
            raise TypeError("Cannot create a Character with non-float speed!")
        self._speed = speed
        self.coins = 0

    @abstractmethod
    def jump(self) -> str:
        pass

    @abstractmethod
    def run(self) -> str:
        pass

    @abstractmethod
    def special_ability(self) -> str:
        pass


class Mario(Character):
    def jump(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Mario jumps!"

    def run(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Mario runs at normal speed!"

    def special_ability(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Mario uses fireball!"

    def __init__(self, lives: int | None = None):
        super().__init__(name="Mario", speed=1.0, lives=lives)


class Luigi(Character):
    def jump(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Luigi jumps higher and floatier!"

    def run(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Luigi runs with slippery momentum!"

    def special_ability(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Luigi uses Poltergust!"

    def __init__(self, lives: int | None = None):
        super().__init__(name="Luigi", speed=0.9, lives=lives)


class Peach(Character):
    def jump(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Peach floats gracefully through the air!"

    def run(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Peach runs elegantly!"

    def special_ability(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Peach uses her parasol!"

    def __init__(self, lives: int | None = None):
        super().__init__(name="Peach", speed=0.85, lives=lives)


class Toad(Character):
    def jump(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Toad does a short but quick jump!"

    def run(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Toad zooms ahead!"

    def special_ability(self) -> str:
        if not self.is_alive:
            raise CharacterDeadError(self.name)
        return "Toad uses spore burst!"

    def __init__(self, lives: int | None = None):
        super().__init__(name="Toad", speed=1.2, lives=lives)
