class Node:
    def __init__(self):
        self.children = {}

class SuffixTree:
    def __init__(self, word):
        self.root = Node()
        self.create_tree(word)

    def create_tree(self, word):
        suffixes = []
        # Create suffix array with '0' as a termination character
        for i in range(len(word) + 1):
            suffixes.append(word[i:] + '0')
        
        for suffix in suffixes:
            current = self.root
            for char in suffix:
                # If the character is already a child of the current node, move to that child
                if char in current.children:
                    current = current.children[char]
                else:
                    # Otherwise, create a new node and move to it
                    new_node = Node()
                    current.children[char] = new_node
                    current = new_node

    def print_tree(self):
        print("==============")
        self.__print_tree(self.root, 0, True)
        print("==============")

    def __print_tree(self, node, lvl, is_right):
        if node is not None:
            children = list(node.children.items())
            left_children = [child for child in children if child[0] == '0']
            right_children = [child for child in children if child[0] != '0']

            # Print left children first
            for char, child in left_children:
                self.__print_tree(child, lvl + 5, False)
                print()
                print(lvl * " " + char)

            # Print right children
            for char, child in right_children:
                self.__print_tree(child, lvl + 5, True)
                print()
                print(lvl * " " + char)

def main():
    word = "banana"
    tree = SuffixTree(word)
    tree.print_tree()

if __name__ == '__main__':
    main()
