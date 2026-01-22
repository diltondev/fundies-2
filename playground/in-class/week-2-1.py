"""Homework launcher that steps through four question stubs."""


def question1() -> None:
    """Stub for Question 1."""

    print("Running question1")
    grades = [78, 85, 92, 68, 95, 88, 73, 90, 82, 87]
    """Find the highest and lowest grades
    Calculate the average grade
    Count how many students scored above 80
    Create a new list with only grades above 85
    Sort the grades in descending order"""
    print(f"Max: {max(grades)}")  # Highest grade
    print(f"Min: {min(grades)}")  # Lowest grade
    print(f"Average grade: {sum(grades) / len(grades):.2f}")  # Average grade
    print(f"Students scoring above 80: {len(list(filter(lambda x: x > 80, grades)))}")  # Count of students above 80
    print(f"Grades above 85: {list(filter(lambda x: x > 85, grades))}")  # List of grades above 85
    grades.sort(reverse=True)
    print(f"Grades sorted descending: {grades}")  # Grades sorted descending


def question2() -> None:
    """Stub for Question 2."""

    print("Running question2")
    #     Create a list of squares for numbers 1 to 10
    # From the following list, create a list of words with more than 5 letters
    words = ["apple", "banana", "kiwi", "strawberry", "grape"]
    # Given the temperatures in the following list, create a list with temperatures in Fahrenheit
    temperatures = [23, 18, 32, 15, 28, 20]
    # (F = C × 9/5 + 32)
    print(f'words with more than 5 letters: {list(filter(lambda x: len(x) > 5, words))}')
    print([(x*9/5)+32 for x in temperatures])


def question3() -> None:
    """Stub for Question 3."""
    print("Running question3")
    users = [
    (101, "barold@email.com", "Barold"),
    (102, "cleo@email.com", "Cleo"),
    (103, "kabuki@email.com", "Kabuki")]
    # Print each user's name and email using a for loop
    # Find the user with ID 102
    # Add a new user (104, "maddie@email.com", "Maddie")
    # Create a list of just the email addresses by unpacking each tuple in a loop or list comprehension
    user102 = None
    for user in users:
        print(f'Name: {user[2]}, Email: {user[1]}')
        if user[0] == 102:
            user102 = user
    users.append((104, "maddie@email.com", "Maddie"))
    newList = [user[1] for user in users]
    


def question4() -> None:
    """Stub for Question 4."""
    print("Running question4")
    products = ["laptop", "mouse", "keyboard", "monitor"]
    prices = [899, 25, 75, 350]
    # Use zip() to create a list of tuples pairing each product with its price
    # Use enumerate() to print each product with its position number (starting from 1)
    # Find the most expensive product using max() with a lambda function
    # Create a new list with a 10% discount applied to all prices using map()
    # Filter and show only products that cost more than 50
    cataloge = list(zip(products, prices))
    print(list(enumerate(cataloge, start=1)))
    most_expensive = max(cataloge, key=lambda x: x[1])
    print(f'Most expensive product: {most_expensive}')
    discounted = map(lambda x: (x[0], x[1]*0.9), cataloge)
    print(f'Discounted products: {list(discounted)}')


def main() -> None:
    """Invoke each homework question stub in order while logging the steps."""

    print("Starting homework run")
    print("Step 1: invoking question1")
    question1()
    print("Step 2: invoking question2")
    question2()
    print("Step 3: invoking question3")
    question3()
    print("Step 4: invoking question4")
    question4()
    print("Homework run complete")


if __name__ == "__main__":
    main()