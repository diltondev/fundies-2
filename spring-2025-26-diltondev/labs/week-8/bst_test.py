from bst import BinarySearchTree


bst = BinarySearchTree()
for word in ["piano", "crane", "stove", "apple", "zebra", "mango", "flute"]:
    bst.insert(word)

print(bst.to_list())
print(bst.range_query("crane", "stove"))
