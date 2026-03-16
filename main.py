from wordle import load_words, play


def main():
    print("Loading word list...")
    bst = load_words("words.txt")
    print("Ready!\n")

    while True:
        play(bst)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Bye!")
            break


if __name__ == "__main__":
    main()
