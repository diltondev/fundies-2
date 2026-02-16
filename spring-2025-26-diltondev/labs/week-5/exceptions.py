class CharacterError(Exception):
    """Base exception for character-related errors."""

    pass


class InvalidLivesError(CharacterError):
    def __init__(self, value: int):
        super().__init__("Lives must be between 0 and 99")
        self.value = value


class InvalidCoinsError(CharacterError):
    def __init__(self, value: int):
        super().__init__("Coins must be between 0 and 999")
        self.value = value


class CharacterDeadError(CharacterError):
    def __init__(self, name: str):
        super().__init__(f"{name} has no lives remaining!")
        self.name = name
