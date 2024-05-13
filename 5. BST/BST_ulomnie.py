#NIESKOŃCZONE
class Node:
    def __init__(self, key_, data_):
        self.key = key_
        self.data = data_
        self.left = None
        self.right = None


class Tree:
    def __init__(self):
        self.root = None

    #funkcja decydująca czy to co wrzucam jest większe czy większe od aktualnego klucza i przypisuje lewo albo prawo 
    def decide(self, current, key):
        if key<current.key:
            if current.left == None:
                return 'left', 'empty'
            return 'left', 'full'
        if current.right == None:
            return 'right', 'empty'
        return 'right', 'full'
    
    def insert(self, key, data, node = None):
        start = self.root
        #jeśli None to znaczy że wrzucam po raz pierwszy Node
        if start == None:
            self.root = Node(key, data, None, None)  
            return
        
        current = start
        #chcę żebby next to był adres na lewo albo prawo
        next = self.decide(current, key)
            
        while next[1] != 'empty':
            #podmiana wartości pod istniejącym kluczem
            if current.key == key:
                current.val = data
                return
            if next[0] == 'left':
                current = current.left 
            else:
                current = current.right 
            next = self.decide(current, key)
        if next[0] == 'left':
                current.left = Node(key, data, None, None)

        else:
                current.right = Node(key, data, None, None)

  

                
    def search(self, key):
        current = self.root
        if current == None:
            print("Brak elementów w drzewie")
            return

        #chcę żebby next to był adres na lewo albo prawo
        next = self.decide(current, key)
            
        while next[1] != 'empty':
            # jak znalazłem
            if current.key == key:
                return current.data
            
            if next[0] == 'left':
                current = current.left 
            else:
                current = current.right 

            next = self.decide(current, key)

        print("Brak klucza o podanej wartości")
        return
    
    def delete(self, key):
        current = self.root
        if current == None:
            print("Brak elementów w drzewie")
            return

        #chcę żebby next to był adres na lewo albo prawo
        next = self.decide(current, key)
            
        while next[0] != 'empty':
            if next[0] == 'left':
                if current.left.key == key:
                     current.left == current.left.left
            else:
                current = current.right 
            next = self.decide(current, key)
        if next[0] == 'left':
                current.left = Node(key, data, None, None)

        else:
                current.right = Node(key, data, None, None)
    #TO DO
    def print(self):
        current = self. root
        sorted = []
        if current != None:
            next = current.left
            while next != None:
                #dobijam do najmniejszego klucza
                current = next
                next = current.left
            sorted.append(current)
                # print(f"{current.key}: {current.data}")


    def height(self):
        pass

    def print_tree(self):
            print("==============")
            self.__print_tree(self.root, 0)
            print("==============")

    def __print_tree(self, node, lvl):
        if node!=None:
            self.__print_tree(node.right, lvl+5)

            print()
            print(lvl*" ", node.key, node.data)
     
            self.__print_tree(node.left, lvl+5)

def test():
    test = Tree()
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    root = Node(40, 'root')
    test.insert(root)
    keys = [50, 15, 62, 5, 20, 58, 91, 3, 8, 37, 60, 24]
    for i in range(len(keys)):
        test.insert(root, keys[i], letters[i])
    # test.insert(root, 5, 'B')
    # test.insert(root, 15, 'H')
    # # test.insert(1, 'C')
    # # test.insert(6, 'G')
    test.print_tree()
    # search_key = 60
    # print(f"wartość pod kluczem {search_key}: {test.search(search_key)}")
    # print(test.search(24))
    # test.insert(20, 'AA')
    # test.insert(6, 'M')
    
test()