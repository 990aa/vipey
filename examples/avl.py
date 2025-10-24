"""
Problem Statement:
You are given the Node class for an AVL tree, which includes a height attribute. You are also given a complete insert function.

Your task is to implement the delete(root, key) function. This function must:

Perform a standard Binary Search Tree (BST) deletion.

After deletion, update the height of the ancestor nodes.

Check the balance factor (height(left_subtree) - height(right_subtree)) of each ancestor node on the path back up to the root.

If a node becomes unbalanced (balance factor > 1 or < -1), perform the correct single or double rotation (Left-Left, Left-Right, Right-Right, or Right-Left) to rebalance the tree.

Return the new root of the (potentially) modified tree.
"""

import sys
from vipey import Vipey

# Node class for the AVL Tree
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1 # height of a new node is 1

class AVLTree:
    # --- Helper Functions (Provided) ---

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def rightRotate(self, y):
        print(f"Performing right rotation on {y.key}")
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))

        # Return new root
        return x

    def leftRotate(self, x):
        print(f"Performing left rotation on {x.key}")
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        # Return new root
        return y

    def getMinValueNode(self, root):
        """Find the inorder successor (smallest node in the right subtree)"""
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)

    # --- Insertion Function (Provided for context) ---
    def insert(self, root, key):
        # 1. Standard BST Insert
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # 2. Update height
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        # 3. Get balance factor
        balance = self.getBalance(root)

        # 4. Rebalance if needed (4 cases)
        # Left Left
        if balance > 1 and key < root.left.key:
            return self.rightRotate(root)
        # Right Right
        if balance < -1 and key > root.right.key:
            return self.leftRotate(root)
        # Left Right
        if balance > 1 and key > root.left.key:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        # Right Left
        if balance < -1 and key < root.right.key:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root
    
    # --- DELETE FUNCTION (The Task) ---
    
    def delete(self, root, key):
        # 1. Standard BST Delete
        if not root:
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else: # Node with the key is found
            # Case 1: Node has 0 or 1 child
            if root.left is None:
                temp = root.right
                root = None # Free memory (in Python, just de-reference)
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # Case 2: Node has 2 children
            # Get the inorder successor (smallest in the right subtree)
            temp = self.getMinValueNode(root.right)
            
            # Copy the inorder successor's data to this node
            root.key = temp.key
            
            # Delete the inorder successor (which is now a duplicate)
            root.right = self.delete(root.right, temp.key)

        # If the tree had only one node, then return
        if not root:
            return root

        # 2. Update Height of the current node
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        # 3. Get Balance Factor
        balance = self.getBalance(root)

        # 4. Rebalance if needed (4 cases)
        
        # Left Left (balance > 1 and left subtree is left-heavy or balanced)
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)

        # Left Right (balance > 1 and left subtree is right-heavy)
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Right Right (balance < -1 and right subtree is right-heavy or balanced)
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)

        # Right Left (balance < -1 and right subtree is left-heavy)
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def preOrder(self, root):
        """Helper to print tree for verification"""
        if not root:
            return
        print(f"{root.key}(h={root.height}, b={self.getBalance(root)})", end=" ")
        self.preOrder(root.left)
        self.preOrder(root.right)

# --- Example Usage ---
if __name__ == "__main__":
    viz = Vipey()
    tree = AVLTree()
    root = None

    # Insert nodes
    keys = [10, 20, 30, 40, 50, 25]
    for key in keys:
        root = tree.insert(root, key)

    print("Tree after insertions:")
    tree.preOrder(root)
    print("\n" + "-"*20)

    # Wrap delete operations for visualization
    print("Deleting 40...")
    captured_delete = viz.capture(tree.delete)
    root = captured_delete(root, 40)
    print("Tree after deleting 40:")
    tree.preOrder(root)
    print("\n" + "-"*20)

    print("Deleting 50...")
    root = tree.delete(root, 50)
    print("Tree after deleting 50:")
    tree.preOrder(root)
    print("\n" + "-"*20)

    print("Deleting 30...")
    root = tree.delete(root, 30)
    print("Tree after deleting 30:")
    tree.preOrder(root)
    print("\n" + "-"*20)
    
    # Save visualization
    print("\n" + "=" * 60)
    print("Generating visualization...")
    print("=" * 60)
    viz.save(interactive=True)