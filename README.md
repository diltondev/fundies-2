# Lab: Wordle with a Binary Search Tree

In this lab you will build a playable Wordle game backed by a binary search tree.

You are already familiar with BST search, insertion, deletion, and traversal from the object developed in the lecture. In this lab you will implement two new BST operations: `to_list` and `range_query` for a Wordle game.

The files in this lab are:

- `bst.py`: implement `to_list` and `range_query` here (Part 1)
- `wordle.py`: implement the game logic here (Part 2)
- `main.py`: run this once both parts are done
- `words.txt`: the Wordle word list

## File Loading

This program loads data form a file using a context manager inside `wordle.py`:

``` python
def load_words(filepath):
    bst = BinarySearchTree()
    with open(filepath) as f:
        words = [line.strip().lower() for line in f if line.strip()]
    # Shuffle words before insertion into BST
    random.shuffle(words)
    for word in words:
        bst.insert(word)
    return bst
```

This uses the `open` function to load the file, read it line by line into a list, shuffle the words and insert into the BST.

## Part 1: New BST Operations

Open `bst.py`. The `BinarySearchTree` class is fully implemented except for two methods.

### Step 1: `to_list`

Implement `_to_list`, a method that collects every value in the BST into a list in alphabetical order. We will use this list to pick a random word from the tree.

> **Hint:** Look at `_traverse`. Your solution has almost exactly the same structure, instead of printing each value, append it to the `result` list that is passed in as an argument.

Test your solution in a separate file called `bst_test.py` before moving on:

```python
from bst import BinarySearchTree

bst = BinarySearchTree()
for word in ["piano", "crane", "stove", "apple", "zebra", "mango", "flute"]:
    bst.insert(word)

print(bst.to_list())
```

Run it with `uv run bst_test.py`, the expected printed output is:

```
['apple', 'crane', 'flute', 'mango', 'piano', 'stove', 'zebra']
```

### Step 2: `range_query`

Implement `_range_query`, a method that returns all values in the BST that fall between a lower and upper bound. This function will be used to calculate the number of words between the first guess word and the last guessed word. For example from our test list:

```python
bst.range_query("crane", "stove")
```

The range between `"crane"` and `"stove"` should return every word that comes alphabetically after or equal to `"crane"` and before or equal to `"stove"`.

> **Hint:** Your solution will look very similar to `_to_list`. The difference is that you use the BST ordering invariant to decide which subtrees are worth visiting, just as `search` uses it to eliminate half the tree at each step:
> - If the current node's value is less than `lower`, there is no point recursing left, everything there is even smaller and cannot be in range.
> - If the current node's value is greater than `upper`, there is no point recursing right, everything there is even larger and cannot be in range.

Test your solution in `bst_test.py` before moving on:

```python
print(bst.range_query("crane", "stove"))
```

Expected output:

```
['crane', 'flute', 'mango', 'piano', 'stove']
```

Do not move on to Part 2 until both methods are working correctly.


## Part 2: Game Logic

Open `wordle.py`. There is one section inside the `play` function marked with a `TODO` comment.

### Guess range summary

After the game ends, use `bst.range_query()` to find all words that fall between the player's alphabetically smallest and largest guess. Print the result in the following format:

```
Your guesses ranged from crane to stove: 148 words apart.
```

If the player guessed correctly on the first attempt, print:

```
You got it in one guess!
```

> **Hint:** `min_guess` and `max_guess` are already being tracked for you in the loop. You just need to pass them to `bst.range_query()` and print the result.

## Running the Game

Once both parts are complete, run:

```
uv run python main.py
```

Don't forget to remove the secret word from the welcome message!

## Submission

1. Run the linter: `uv run ruff check`
2. Format your code: `uv run ruff format`
3. Commit and push to GitHub
4. Submit your repository link on Canvas
