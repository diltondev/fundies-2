import random
from bst import BinarySearchTree


def load_words(filepath):
    bst = BinarySearchTree()
    with open(filepath) as f:
        words = [line.strip().lower() for line in f if line.strip()]
    # Shuffle words before insertion into BST
    random.shuffle(words)
    for word in words:
        bst.insert(word)
    return bst


def display_feedback(guess, secret):
    symbols = []
    for i, letter in enumerate(guess):
        if letter == secret[i]:
            symbols.append("🟩")
        elif letter in secret:
            symbols.append("🟨")
        else:
            symbols.append("⬜")
    print(f"{guess.upper()}  {' '.join(symbols)}\n")


def play(bst):
    secret = pick_secret(bst)
    print(f"\nI have chosen a secret five letter word ({secret}). You have 6 guesses.\n")

    min_guess = None
    max_guess = None

    solved = False

    for attempt in range(1, 7):
        guess = input(f"Guess {attempt}: ").strip().lower()

        # Check that we have a valid word guessed from the tree
        while not bst.search(guess):
            print("Not a valid word, try again.")
            guess = input(f"Guess {attempt}: ").strip().lower()

        # Store the lowest and maximum values for displaying stats
        if min_guess is None or guess < min_guess:
            min_guess = guess
        if max_guess is None or guess > max_guess:
            max_guess = guess

        display_feedback(guess, secret)

        if guess == secret:
            print(f"\nWell done! You got it in {attempt} turns!")
            solved = True
            break

    if not solved:
        print(f"\nBad luck! The word was: {secret}")

    # TODO: use bst.range_query() to find all words between min_guess
    # and max_guess. Print the result in the following format:
    #   "Your guesses ranged from {min_guess} to {max_guess}: X words apart."
    # If min_guess == max_guess, print "You got it in one guess!" instead.


def pick_secret(bst):
    return random.choice(bst.to_list())
