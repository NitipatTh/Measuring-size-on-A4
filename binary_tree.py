class Node:

    def __init__(self, data, parent, class_obj, level):

        self.left = None
        self.right = None
        self.data = data
        self.parent = parent
        self.class_obj = class_obj
        self.level = level

    def insert(self, data):
        # Compare the new value with the parent node
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data, self.data, "left", self.level+1)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data, self.data, "right", self.level+1)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    # Print the tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data, " Parent:", self.parent, "  class:", self.class_obj, " Level:", self.level),
        if self.right:
            self.right.PrintTree()


# Use the insert method to add nodes
root = Node(8, -1, "root", 0)
root.insert(4)
root.insert(12)
root.insert(2)
root.insert(6)
root.insert(10)
root.insert(14)
root.insert(1)
root.insert(3)
root.insert(5)
root.insert(7)
root.insert(9)
root.insert(11)
root.insert(13)
root.insert(15)
root.insert(0)
root.PrintTree()
