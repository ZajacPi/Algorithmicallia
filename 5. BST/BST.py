#NIESKOŃCZONE
class Node:
    def __init__(self, key_, data_):
        self.key = key_
        self.data = data_
        self.left = None
        self.right = None

#każda metoda działa rekurencyjnie odwołując się do funkcji pomocniczej, żeby użytkownik musiał wpisywać tylko interesujące go dane
class Tree:
    def __init__(self):
        self.root = None 

    def insert(self, key, data):
        #ustawiam root jeśli jeszcze nie ma
        if self.root == None:
            self.root = Node(key, data)
        return self.__insert(self.root, key, data)
    
    def __insert(self, node, key = None, data=None):
        #jeśli root jest None to znaczy że wrzucam po raz pierwszy 
        if self.root == None:
            self.root = node
            return
        #znalazłem wolne miejsce, tworzę node
        if node == None:
            return  Node(key, data)  
        #nadpisywanie istniejącego klucza
        elif node.key == key:
            node.data = data  
            return node
        #szukam wolnego miejsca
        elif key < node.key:
            node.left = self.__insert(node.left, key, data )
        elif key>node.key:
            node.right = self.__insert( node.right, key, data)
       
        return node

                
    def search(self, key):
        if self.root == None:
            print("Brak elementów w drzewie!")
            return
        return self.__search(key, self.root)
       
    def __search(self, key, node):
        if node.key == key:
            return node.data
        elif key < node.key:
            return self.__search(key, node.left)
        elif key > node.key:
            return self.__search(key, node.right)
    

    def delete(self, key):
        if self.root == None:
            print("Brak elementów w drzewie!")
            return  
        self.__delete(self.root, key)
        
    def __delete(self, node, key):
        #szukam klucza
        if key < node.key:
            node.left = self.__delete(node.left, key)
            
        elif key > node.key:
            node.right = self.__delete(node.right, key)

        #znaleziono klucz!
        else:
            #dwójka dzieci
            if node.left != None and node.right != None:
                new = node.right
                while new.left != None:
                    new = new.left
              
                #teraz new jest najmniejszym elementem z prawego poddrzewa
                node.key =  new.key 
                node.data = new.data 
        
                # na koniec sprzątanie, czyli usunięcie tego nowego którym zastąpiłem usuwany node, bo inaczej pojawi się dwukrotnie
                node.right = self.__delete(node.right, new.key)
         
            
            # #jedno dziecko (sprawdzam czy lewe czy prawe)
            elif node.left != None or node.right != None:
                if node.left is None:
                    temp = node.right
            #         # del node
                    return temp
            #         return node.right
                elif node.right is None:
                    temp = node.left
            #         # del node
                    return temp
            
            # #brak dzieci
            elif node.left == None and node.right == None:
                return None
        return node
 

    def height(self):
        if self.root == None:
            # print("Brak elementów w drzewie!")
            return 0
        return self.__height(self.root)
        
    def __height(self, node):
        if node == None:
            return 0
        else:
            left_height = self.__height(node.left)
            right_height = self.__height(node.right)
            
        if right_height > left_height:
            return right_height + 1
        else:       
            return left_height + 1
        

    def print(self):
        sorted = self.__print(self.root, [])
        #dostaję listę, zmieniam na string jak w treści zadania
        result = ""
        for i in sorted:
            result += i +', '
        print(result)
        # zwracam posortowaną listę (może być przydatne dla użytkownika)
        return sorted

    def __print(self, node, result):
        if node != None:
            if node.left != None:
                self.__print(node.left, result)
            result.append(f"{str(node.key)}:{node.data}")
            if node.right != None:
                self.__print(node.right, result) 
        return result
                
        
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


def main():
    test = Tree()

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
 
    keys = [50, 15, 62, 5, 20, 58, 91, 3, 8, 37, 60, 24]
    for i in range(len(keys)):
        test.insert(keys[i], letters[i])
    test.print_tree()   
    test.print()
    print(test.search(24))
    test.insert(20, 'AA')
    test.insert(6, 'M')
    test.delete(62)
    test.insert(59, 'N')
    test.insert(100, 'P')
    test.delete(8)
    test.delete(15)
    test.insert(55, 'R')
    test.delete(50)
    test.delete(5)
    test.delete(24)
    print(test.height())
    test.print()
    test.print_tree()

main()

def test():
    test = Tree()
    letters = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    #tworzenie root
    test.insert(50, 'A')
    keys = [15, 62, 5, 20, 58, 91, 3, 8, 37, 60, 24]
    for i in range(len(keys)):
        test.insert(keys[i], letters[i])
    #TEST INSERT
    # test.insert(root, 5, 'B')
    # test.insert(root, 15, 'H')
    # # test.insert(1, 'C')
    # # test.insert(6, 'G')
    # print("podstawiam za 20 AA i za 6 M")
    # test.insert(root, 20, 'AA')
    # test.insert(root, 6, 'M')
    test.print_tree()

    #TEST SEARCH
    # search_key = 20
    # print(f"wartość pod kluczem {search_key}: {test.search(search_key)}")
    # print(test.search(24))
    # test.print_tree()

    # TEST DELETE
    # print("Test usunięcia node bez dzieci (elementu 6 M)")
    # test.delete(6)
    # test.print_tree()
    # print("Test usunięcia node z jednym dzieckiem (elementu 37 J)")
    # test.delete(37)
    # test.print_tree()
    # print("Test usunięcia elementu z dwoma dziećmi (15 B)")
    # test.delete(15)
    # test.print_tree()

    # TEST HEIGHT
    # print(test.height())

    # TEST PRINT
    test.print()
    #TEST ZADANIA
    test.insert(20, 'AA')
    test.insert(6, 'M')
    test.delete(62)
    test.insert(59, 'N')
    test.insert(100, 'P')
    print("Check 1")
    test.print_tree()

    test.delete(8)
    test.delete(15)
    print("Check 2")
    test.print_tree()

    print("Check 3")
    test.insert(55, 'R')
#mamy problem z usunięciem root
    test.delete(50)
    print("Check 4")
    test.print_tree()
    test.delete(5)
    test.delete(24)
    test.print_tree()


# test()