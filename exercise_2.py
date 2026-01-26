"""
Exercise 2: Tuple Unpacking
TASK: Write the function to make the tests pass

Create a function called get_high_performers that:
- Takes a list of participant tuples: (name: str, points: int, category: str)
- Returns a list of names of participants who have points > 75
- Names should be in the same order as the input list
"""


def get_high_performers(participants: list[tuple[str, int, str]]) -> list[str]:
    """
    Extract names of participants with scores above 75 points.

    Args:
        participants: List of tuples containing (name, points, category)

    Returns:
        List of names of high-performing participants
    """
    # YOUR CODE HERE
    # Remove pass when you implement
    pass


def test_get_high_performers_all_qualify():
    participants = [
        ("Maple", 85, "Gold"),
        ("Raymond", 92, "Platinum"),
        ("Sherb", 78, "Silver")
    ]
    assert get_high_performers(participants) == ["Maple", "Raymond", "Sherb"]


def test_get_high_performers_mixed():
    participants = [
        ("Marina", 85, "Gold"),
        ("Ankha", 65, "Bronze"),
        ("Apollo", 88, "Platinum"),
        ("Audie", 50, "Bronze")
    ]
    assert get_high_performers(participants) == ["Marina", "Apollo"]


def test_get_high_performers_boundary():
    participants = [
        ("Marshal", 76, "Silver"),
        ("Judy", 75, "Bronze")
    ]
    assert get_high_performers(participants) == ["Marshal"]


def test_get_high_performers_empty():
    assert get_high_performers([]) == []


def test_get_high_performers_none_qualify():
    participants = [
        ("Stitches", 70, "Bronze"),
        ("Bob", 60, "Bronze")
    ]
    assert get_high_performers(participants) == []
