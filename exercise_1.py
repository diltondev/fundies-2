"""
Exercise 1: List Operations
TASK: Write the function to make the tests pass

Create a function called process_game_ratings that:
- Takes a list of game ratings (integers)
- Removes any ratings below 1 or above 10 (invalid ratings)
- Returns a new list with only valid ratings, sorted in ascending order
"""


def process_game_ratings(ratings: list[int]) -> list[int]:
    """
    Filter out invalid game ratings and return valid ratings in ascending order.

    Valid ratings are between 1 and 10.

    Args:
        ratings: List of integer game ratings

    Returns:
        Sorted list of valid ratings in ascending order
    """
    # YOUR CODE HERE
    # Remove pass when you implement
    pass


def test_process_game_ratings_basic():
    assert process_game_ratings([7, 9, 5, 10]) == [5, 7, 9, 10]


def test_process_game_ratings_with_invalid():
    assert process_game_ratings([7, -2, 9, 15, 5]) == [5, 7, 9]


def test_process_game_ratings_empty():
    assert process_game_ratings([]) == []


def test_process_game_ratings_all_invalid():
    assert process_game_ratings([-5, 20, 0, 100]) == []


def test_process_game_ratings_boundary():
    assert process_game_ratings([1, 10, 5]) == [1, 5, 10]
