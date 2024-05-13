#NIESKOŃCZONE
import random
class Node:
    def __init__(self, key_, val_, level_ ):
        self.key = key_
        self.val = val_
        self.forward = [None for i in range(level_+1)]

class SkipList:
    def __init__(self, maxLevel_):
        self.maxLevel = maxLevel_
        #head ma być wskaźnikiem na pierwsze elementy na wszystkich poziomach
        self.head = Node(None, None, self.maxLevel)
        # Jaki jest największy poziom
        self.current_lvl = 0

    # def createEmptyNode(self, level):
    #     return Node(None, None, level)
    
    def randomLevel(self, p = 0.5):
        lvl = 1  
         
        while float(random.random()) < 0.5 and lvl < self.maxLevel:
                lvl = lvl + 1
        return lvl
    
    def insert(self, key, val):
        #historia odwiedzonych elementów
        history = [None for i in range(self.maxLevel+1)]
        current = self.head

        #NAJWAŻNIEJSZA CZĘŚĆ CAŁEGO PROGRAMU: SZUKANIE DANEGO KLUCZA
        #najpier na najwyższym poziomie czyli "autostradzie"
        #będę sobie trawersował prze elementy schowane w forwardlicy elementu pierwszego tak długo jak nie są puste i są mniejsze od szukanego klucza (czyli w while idę prawo)
        # range mogę ustawić tak żeby przechodziło od majwyższego (maxLevel-1) do -1, z krokiem -1
        for i in range(self.maxLevel- 1, -1, -1):
            while current.forward[i] != None and current.forward[i].key < key:
                current = current.forward[i]
            history[i] = current

        #teraz już jestem na poziomie 0 czyli wszystkie elementy bez skoków
        current = current.forward[0]

        # jeśli jest puste to znaczy że dobiłem do końca albo żę muszę wstawić pomiędzy jeśli nie równa się kluczowi, trzeba zrobić nowy Node
        if current == None or current.key != key:
            random_level = self.randomLevel()
        
             #jeśli wygenerowało wyższy level niż aktualny najwyższy trzeba zrobić update
            if random_level > self.current_lvl:
                for i in range(self.current_lvl+1, random_level+1):
                    history[i] = self.head
                self.current_lvl = random_level

            #tworzę nowy Node 
            newNode = Node(key, val, random_level)

            for i in range(random_level):
                    newNode.forward[i] = history[i].forward[i]
                    history[i].forward[i] = newNode
        #w przypadku gdzie znalazło się current o podanym kluczu to nadpisuję val
        elif current.key == key:
            current.val = val

    def search(self, key):
        current = self.head
        #podobnie jak w insert sobie trawersuję od najwyższego poziomu
        for i in range(self.maxLevel- 1, -1, -1):
            while current.forward[i] != None and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current != None and current.key == key:
            return current.val
        else:
            return None
 

    def remove(self, key):
        history = [None for i in range(self.maxLevel)]
        current = self.head
        # znowu używam trawersu do znalezienia podanej wartości
        for i in range(self.maxLevel-1, -1, -1):
            while current.forward[i] != None and current.forward[i].key < key:
                current = current.forward[i]
            history[i] = current
        current = current.forward[0]

        #jak znaleziono trzeba posprzątać na wszystkich poziomach
        if current != None and current.key == key:
            for i in range(self.current_lvl):
                #muszę przerwać w przypadku kiedy nie ma go już na tym poziomie
                if history[i].forward[i] != current:
                    break
                history[i].forward[i] = current.forward[i]
 
        # Jeśli najwyższe poziomy nie mają elementów no to trzeba je usunąć
        while(self.current_lvl > 0 and self.head.forward[self.current_lvl] == None):
            self.current_lvl -= 1

    def __str__(self):
        result = ""
        node = self.head.forward[0]  # pierwszy element na poziomie 0
        while node is not None:
            result += f"{node.key}:{node.val} "
            node = node.forward[0]   #trawersuje do kolejnego elementu na poziomie 0
        return result
    
    def displayList_(self):
        node = self.head.forward[0]  # pierwszy element na poziomie 0
        keys = [ ]                        # lista kluczy na tym poziomie
        while node is not None:
            keys.append(node.key)
            node = node.forward[0]

        for lvl in range(self.maxLevel - 1, -1, -1):
            print(f"{lvl}  ", end=" ")
            node = self.head.forward[lvl]
            idx = 0
            while node is not None:
                while node.key > keys[idx]:
                    print(end=5*" ")
                    idx += 1
                idx += 1
                print(f"{node.key:2d}:{node.val:2s}", end="")
                node = node.forward[lvl]
            print()
            
def main():
    random.seed(42)
    test = SkipList(5)
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

    for i in range(1, 16):
        test.insert(i, letters[i-1])
    test.displayList_()
    print(test.search(2))
    test.insert(2, 'Z')
    print(test.search(2))
    test.remove(5)
    test.remove(6)
    test.remove(7)
    print(test)
    test.insert(6, 'W')
    print(test)
# main()
def test():
    random.seed(42)
    test = SkipList(5)
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

    for i in range(1, 16):
        test.insert(i, letters[i-1])
    test.displayList_()
    print("Szukam wartości pod kluczem 2")
    print(test.search(2))
    test.insert(2, 'Z')
    print("Nadpisuję wartość pod 2 literą Z i sprawdzam czy sie udało:")
    print(test.search(2))
    print("Usuwam 5, 6 i 7")
    test.remove(5)
    test.remove(6)
    test.remove(7)
    print(test)
    test.insert(6, 'W')
    print(test)

# test()