class Node():
    def __init__(self):
        self.children = {}
  
class Suffix_Tree():
    def __init__(self, word):
        self.root = Node()
        self.children = {}
        self.create_tree(word)
 
    def create_tree(self, word):
        suffixes = []
        #tworzę tablicę suffixów, daję 0 na koniec jako znak zakończenia
        for i in range(len(word)+1):
            suffixes.append((word[i:])+'0')
            print((word[i:])+'0')
        
        for suffix in suffixes:
            current = self.root
            for char in suffix:
                #jesli litera jest już określona dla aktualnego node, to przechodzę do niej
                if char in current.children:
                    current = current.children[char]
                else:
                # Jeśli nie to tworzę nowy node
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

            for char, child in left_children:
                self.__print_tree(child, lvl + 5, False)
                print()
                print(lvl * " " + char)

            for char, child in right_children:
                self.__print_tree(child, lvl + 5, True)
                print()
                print(lvl * " " + char)  
            
    def search_pattern(self, pattern):
        current = self.root
        for char in pattern:
            if char in current.children:
                current = current.children[char]
            else:
                return 0  # nie znalazł wzorca
        #jeśli przeszło znaczy że wzorzec znaleziony
        return self.__count_leaves(current)

    def __count_leaves(self, node):
        if len(node.children) == 0: #brak dzieci, czyli jeden liść
            return 1
        count = 0
        for child in node.children.values():
            count += self.__count_leaves(child)
        return count

############################################
def suffix_array(word):
    suffixes = []
    for i in range(len(word)+1):
        suffixes.append((i, word[i:]))
    suffixes.sort(key=lambda x: x[1])
    suffix_array = [i for i, suf in suffixes] 
    return suffix_array

def binary_search(word, pattern, suffix_array):
    #indeksy początku i końca
    left, right = 0, len(suffix_array) - 1

    result = None

    while left <= right:
        #znajduję środek
        mid = (left + right) // 2
        #przy pomocy tablicy odtwarzam suffix
        suffix = word[suffix_array[mid]:]

        if suffix.startswith(pattern):
            result = suffix_array[mid]  #zapisuję znaleziony wynik
            right = mid - 1  #nadal przeszukuję lewą połówkę
        elif suffix < pattern:
            left = mid + 1
        else:
            right = mid - 1
    return result

def test_suffix_tree(word, pat1, pat2, pat3):
    Trie = Suffix_Tree(word)
    Trie.print_tree()
    test_search_tree(Trie, pat1)
    test_search_tree(Trie, pat2)
    test_search_tree(Trie, pat3)

def test_search_tree(Trie, pattern):
        print(f"Wzorzec {pattern} pojawia się {Trie.search_pattern(pattern)} razy.")

def test_suffix_array(word, patterns):
    S_array = suffix_array(word)
    for pattern in patterns:
        found = binary_search(word, pattern, S_array)
        if found != None: 
            print(f"Znaleziono wzorzec {pattern} na pozycji {found}")
            print(word[found:found+len(pattern)])

def main():
    # test_suffix_tree('banana', 'ana', 'na', 'ban')
    # test_suffix_tree('azbestmaster', 'st', 'natura2000', 'ster')

    test_suffix_array('banana', ['ana', 'na', 'ban'])


if __name__ == '__main__':
    main()