"""
Exercise 3: Set Operations
TASK: Write tests for the provided function

The function find_common_and_unique is provided below.
- Write at least 5 tests that verify it works correctly.
- Consider: basic cases, empty sets, no overlap, complete overlap, subset relationships, etc
- Write descriptive test function names such as:
    - test_find_common_and_unique_basic()
    - test_find_common_and_unique_no_overlap()
    - test_find_common_and_unique_complete_overlap()
    - test_find_common_and_unique_empty_sets()
"""


def find_common_and_unique(set_a: set[str], set_b: set[str]) -> dict[str, set[str]]:
    """
    Find common elements and unique elements in two sets.

    Args:
        set_a: First set of strings
        set_b: Second set of strings

    Returns:
        Dictionary with keys:
        - 'common': elements in both sets (intersection)
        - 'only_a': elements only in set_a (difference)
        - 'only_b': elements only in set_b (difference)
    """
    return {"common": set_a & set_b, "only_a": set_a - set_b, "only_b": set_b - set_a}


def test_find_common_and_unique_all_overlap():
    result = find_common_and_unique(
        set_a={"apple", "banana", "orange", "kiwi", "watermelon"},
        set_b={"apple", "banana", "orange", "kiwi", "watermelon"},
    )
    assert result["common"] == {"apple", "banana", "orange", "kiwi", "watermelon"}
    assert result["only_a"] == set()
    assert result["only_b"] == set()


def test_find_common_and_unique_no_overlap():
    set_a = {"apple", "banana", "orange", "kiwi", "watermelon"}
    set_b = {"pear", "grape", "pineapple", "mango", "papaya"}
    result = find_common_and_unique(set_a=set_a, set_b=set_b)
    assert result["common"] == set()
    assert result["only_a"] == set_a
    assert result["only_b"] == set_b


def test_find_common_and_unique_empty_set():
    result = find_common_and_unique(set(), set())
    assert result["common"] == set()
    assert result["only_a"] == set()
    assert result["only_b"] == set()


def test_find_common_and_unique_case_differences():
    list_a = {"APPLE", "Banana", "orange", "kiwi", "waTerMelon"}
    list_b = {"apple", "banana", "orange", "KIWI", "watermelon"}
    result = find_common_and_unique(set_a=list_a, set_b=list_b)
    assert result["common"] == {"orange"}
    assert result["only_a"] == {"APPLE", "Banana", "kiwi", "waTerMelon"}
    assert result["only_b"] == {"apple", "banana", "KIWI", "watermelon"}


def test_find_common_and_unique_with_repeats():
    list_a = {"apple", "apple", "orange", "orange", "watermelon"}
    list_b = {"apple", "banana", "banana", "orange", "orange"}
    result = find_common_and_unique(set_a=list_a, set_b=list_b)
    assert result["common"] == {"apple", "orange"}
    assert result["only_a"] == {"watermelon"}
    assert result["only_b"] == {"banana"}
