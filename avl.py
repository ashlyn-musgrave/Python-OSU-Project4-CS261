# Name: Ashlyn Musgrave
# Course: CS261 - Data Structures
# Assignment: Assignment 4 BST/AVL Tree Implementation
# Due Date: November 20, 2023
# Description: This assignment implements an AVL tree


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #
    def add(self, value: object) -> None:
        """
        Add a new value to the AVL tree.

        Duplicate values are not allowed.

        Implemented with O(log N) runtime complexity.
        """
        # Check if the value is not already in the tree
        if not self.contains(value):
            # Call the recursive helper function to add the value to the tree
            self._root = self._add_recursive(self._root, value)

    def _add_recursive(self, node: AVLNode, value: object) -> AVLNode:
        """
        Helper method for recursive addition of a value to the AVL tree.
        """
        # Base case: if the current node is None, create a new node with the given value
        if node is None:
            return AVLNode(value)

        # Compare the value to be added with the current node's value
        if value < node.value:
            node.left = self._add_recursive(node.left, value)
            node.left.parent = node  # Update left child's parent pointer
        elif value > node.value:
            node.right = self._add_recursive(node.right, value)
            node.right.parent = node  # Update right child's parent pointer

        # Update the height of the current node
        self._update_height(node)

        # Perform AVL tree balancing
        return self._rebalance(node)

    def remove(self, value: object) -> None:
        """
        Remove a value from the AVL tree.

        Implemented with O(log N) runtime complexity.
        """
        # Check if the value is present in the tree before attempting removal
        if self.contains(value):
            # Call the recursive helper function to remove the value from the tree
            self._root = self._remove_recursive(self._root, value)
            return True  # Return True after successful removal
        return False  # Return False if the value is not found

    def _remove_recursive(self, node: AVLNode, value: object) -> AVLNode:
        """
        Helper method for recursive removal of a value from the AVL tree.
        """
        # Base case: if the current node is None, the value is not found
        if node is None:
            return node

        # Compare the value to be removed with the current node's value
        if value < node.value:
            node.left = self._remove_recursive(node.left, value)
            if node.left:
                node.left.parent = node  # Update left child's parent pointer
        elif value > node.value:
            node.right = self._remove_recursive(node.right, value)
            if node.right:
                node.right.parent = node  # Update right child's parent pointer
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children: Get the inorder successor (smallest
            # in the right subtree)
            successor = self._get_min_value_node(node.right)

            # Copy the inorder successor's value to this node
            node.value = successor.value

            # Delete the inorder successor
            node.right = self._remove_recursive(node.right, successor.value)

        # Update height and rebalance the node
        self._update_height(node)
        return self._rebalance(node)
    def _get_min_value_node(self, node: AVLNode) -> AVLNode:
        """
        Get the node with the minimum value in the AVL tree.
        """
        # Start from the given node and traverse the left child until reaching the leftmost leaf
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _update_height(self, node: AVLNode) -> None:
        """
        Update the height of a given AVL node based on the heights of its children.
        """
        # Calculate the height of the left child (or -1 if the left child is None)
        left_height = node.left.height if node.left else -1
        # Calculate the height of the right child (or -1 if the right child is None)
        right_height = node.right.height if node.right else -1

        # Update the height of the current node based on the maximum height of its children
        node.height = 1 + max(left_height, right_height)

    def _rebalance(self, node: AVLNode) -> AVLNode:
        """
        Rebalance the AVL tree if necessary after an insertion.
        """
        balance = self._get_balance(node)

        # Left Heavy
        if balance > 1:
            # Left Right Case
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            # Left Left Case
            return self._rotate_right(node)

        # Right Heavy
        if balance < -1:
            # Right Left Case
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            # Right Right Case
            return self._rotate_left(node)

        return node

    def _get_balance(self, node: AVLNode) -> int:
        """
        Get the balance factor of a given AVL node.
        """
        # Calculate the height of the left child (or -1 if the left child is None)
        left_height = node.left.height if node.left else -1
        # Calculate the height of the right child (or -1 if the right child is None)
        right_height = node.right.height if node.right else -1

        # Return the balance factor: difference in heights of left and right subtrees
        return left_height - right_height

    def _rotate_left(self, current: AVLNode) -> AVLNode:
        """
        Perform a left rotation on a given AVL node.
        """

        right_child = current.right
        left_of_right_child = right_child.left

        # Perform rotation
        right_child.left = current
        current.right = left_of_right_child

        # Update heights and parent pointers
        self._update_height(current)
        self._update_height(right_child)

        right_child.parent = current.parent  # Update parent pointer for right_child
        current.parent = right_child  # Update parent pointer for current

        if left_of_right_child:
            left_of_right_child.parent = current  # Update parent pointer for left_of_right_child

        return right_child

    def _rotate_right(self, current: AVLNode) -> AVLNode:
        """
        Perform a right rotation on a given AVL node.
        """

        left_child = current.left
        right_of_left_child = left_child.right

        # Perform rotation
        left_child.right = current
        current.left = right_of_left_child

        # Update heights and parent pointers
        self._update_height(current)
        self._update_height(left_child)

        left_child.parent = current.parent  # Update parent pointer for left_child
        current.parent = left_child  # Update parent pointer for current

        if right_of_left_child:
            right_of_left_child.parent = current  # Update parent pointer for right_of_left_child

        return left_child

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)