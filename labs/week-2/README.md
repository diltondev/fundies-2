# Week 2 Lab: Lists, Tuples, Sets, and Dictionaries
## Overview

This lab will help you practice working with Python's core data structures: lists, tuples, sets, and dictionaries.

## Getting Started

The exercises are split into separate Python files in this directory. Each file contains one exercise with its function definition and tests.

## Writing Tests
Write tests functions by writing functions that test functions using the `assert` statement in Python. Test function names should clearly describe what is being tested and the expected outcome. All test should start with `test_` and use `_` underscores to seperate words.

A good test function name answers three questions:
- what is being tested
- under what conditions
- what is the expected result

It should be easy recognise what went wrong when read the function name from a failed test.

You should write different functions to test the expected behaviour.

```python
def test_deposit_with_positive_amount_increases_balance():
    ...

def test_withdraw_with_insufficient_funds_raises_error():
    ...

def test_email_validation_with_missing_at_symbol_returns_false():
    ...
```

## Running Tests
Change in to the directory for the lab using `cd week-2-lab` in the terminal.

To run tests for a specific exercise:
```bash
uv run pytest exercise_1.py
```

To run all exercises at once:
```bash
uv run pytest exercise_*.py
```
The `*` catches all filenames with `exercise_` at the start.

To see more detailed output:
```bash
uv run pytest exercise_1.py -v
```

## Lab Structure

Each exercise file follows this pattern:
1. Read the function description and requirements at the top of the file
2. Either:
   - **Write the function** to make the provided tests pass, OR
   - **Write tests** for the provided function
3. Run pytest to verify your solutions

## Submission
1. Ensure all tests pass by running `uv run pytest exercise_*.py`
2. Review your code for style and clarity
3. Run the linter: `uv run ruff check exercise_*.py`
4. Format your code: `uv run ruff format exercise_*.py`
5. Commit and push to GitHub
5. Submit the link for your lab directory on GitHub on Canvas for feedback
