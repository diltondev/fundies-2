import math
def question1() -> None:
    # Given this list of student IDs, convert it to a set to remove duplicates and find the unique students. Print how many unique students there are.

    student_ids = [101, 102, 103, 101, 104, 102, 105, 103]
    unique_students = set(student_ids)
    print(f'Unique students: {unique_students}')
    
    print("End of question1")
    return None

def question2() -> None:
    class_a = {'Angus', 'Bubbles', 'Chester', 'Daisy'}
    class_b = {'Chester', 'Daisy', 'Eve', 'Frita'}

    # Students in both classes (intersection)
    # Students in either class (union)
    # Students only in class_a (difference)
    # Students in only one class (symmetric difference)
    
    intersection = class_a & class_b
    union = class_a | class_b
    difference = class_a - class_b
    xor = class_a ^ class_b
    
    print("End of question2")
    return None

def question3() -> None:
    # Create a new dictionary with only students who scored above 75 using a dictionary comprehension

    scores = {'Angus': 85, 'Bubbles': 92, 'Chester': 78, 'Daisy': 95, 'Eve': 88}
    bs_and_up = {n: s for n, s in scores.items() if s > 85}
    # Create a dictionary that counts how many times each letter appears in the word "hello". The expected output is as follows:
    freq = dict()
    for c in "hello":
        if not c in freq:
            freq[c] = 0
        freq[c] += 1
    print(freq)
    # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    
    print("End of question3")
    return None

def question4() -> None:
    # Create a program that tracks inventory for a small shop. Start with this dictionary:

    inventory = {
        'apples': 50,
        'bananas': 30,
        'oranges': 45,
        'pears': 20
    }
    # Complete the following tasks:
    # 
    # Add a new item 'grapes' with quantity 35
    # A customer buys 10 apples - update the inventory
    # Check if 'mangoes' are in stock using the in operator
    # Print all items with quantity less than 25
    # Create a new dictionary using comprehension that applies a 10% restock to all items (multiply quantities by 1.1)
    
    inventory['grapes'] = 25
    inventory['apples'] -= 10
    print(f'Mangoes are {'not ' if 'mangoes' not in inventory or inventory['mangoes'] == 0  else ''}in stock')
    print(f'Items with less than 25 items: { list({n: q for n, q in inventory.items() if q < 25}.keys())}')
    new_inventory = {k: math.floor(v*1.1) for k, v in inventory.items()}
    print(f"New inventory: {new_inventory}")
    print("End of question4")
    return None





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