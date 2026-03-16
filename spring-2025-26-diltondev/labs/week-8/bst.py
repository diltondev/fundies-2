class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left_child = left
        self.right_child = right


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert(value, self.root)

    def _insert(self, value, node):
        if value < node.value:
            if not node.left_child:
                node.left_child = TreeNode(value)
            else:
                self._insert(value, node.left_child)
        elif value > node.value:
            if not node.right_child:
                node.right_child = TreeNode(value)
            else:
                self._insert(value, node.right_child)

    def search(self, value):
        return self._search(value, self.root)

    def _search(self, value, node):
        if not node:
            return None
        if node.value == value:
            return node
        if value < node.value:
            return self._search(value, node.left_child)
        return self._search(value, node.right_child)

    def delete(self, value):
        self.root = self._delete(value, self.root)

    def _delete(self, value, node):
        if node is None:
            return None
        if value < node.value:
            node.left_child = self._delete(value, node.left_child)
        elif value > node.value:
            node.right_child = self._delete(value, node.right_child)
        else:
            if not node.left_child and not node.right_child:
                return None
            elif not node.left_child:
                return node.right_child
            elif not node.right_child:
                return node.left_child
            else:
                successor = self._find_min_node(node.right_child)
                node.value = successor.value
                node.right_child = self._delete(successor.value, node.right_child)
        return node

    def _find_min_node(self, node):
        while node.left_child:
            node = node.left_child
        return node

    def traverse(self):
        self._traverse(self.root)

    def _traverse(self, node):
        if not node:
            return
        self._traverse(node.left_child)
        print(node.value)
        self._traverse(node.right_child)

    def to_list(self):
        """Return a list of all values in the BST in alphabetical order."""
        result = list()
        self._to_list(self.root, result)
        return result

    def _to_list(self, node, result):
        if not node:
            return []
        self._to_list(node.left_child, result)
        result.append(node.value)
        self._to_list(node.right_child, result)

    def range_query(self, lower, upper):
        """
        Return a list of all values in the BST that fall between
        lower and upper (inclusive).

        Args:
            lower (str): the lower bound of the range (inclusive)
            upper (str): the upper bound of the range (inclusive)

        Returns:
            list: all values in the tree where lower <= value <= upper,
                  in alphabetical order
        """
        results = []
        self._range_query(self.root, lower, upper, results)
        return results

    def _range_query(self, node, lower, upper, results):
        if not node:
            return
        if node.value >= lower:
            self._range_query(node.left_child, lower, upper, results)
        if node.value >= lower and node.value <= upper:
            results.append(node.value)
        if node.value <= upper:
            self._range_query(node.right_child, lower, upper, results)
