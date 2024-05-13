#NIESKOŃCZONE

class Element:
    def __init__(self, key_, val_):
        self.key = key_
        self.val = val_

    def __str__(self):
        #zwraca napis przedstawiający  element w postaci klucz:wartość
        return str(f"{self.key}: {self.val},")
    
class NoEmptySpaces(Exception):
    pass

class Hash_table:
    def __init__(self, size_, c1_ = 1, c2_ = 0):
        self.size = size_
        self.c1 = c1_
        self.c2 = c2_
        self.tab = [None for i in range(size_)]
    

    def hashing(self, key):
        if isinstance(key, str):
            hash_val = sum(ord(char) for char in key)
            return hash_val % self.size
        
        else:
            return key % self.size
    

    def probing(self, element, search_key = None):
        #niepotrzebnie jest rozbijać nma dwa przypadki liniowe/kwadratowe bo kwadratowe z parametrem c1=1 i c2=0 będzie liniowe
        index = self.hashing(element.key)
        for i in range(1, self.size):
            index = (index + self.c1*1 + self.c2*i**2) % self.size

            # wywoływane tylko przez search i remove
            if search_key != None:
                if self.tab[index].key == search_key:
                    return self.tab[index].val
                #jeśli przeszliśmy przez cały range to znaczy że nie znaleziono
                if i == self.size-1:
                    # print("Nie znaleziono elementu o podanym kluczu")
                    return
                    
            # wywoływane przez insert
            elif self.tab[index] == None or self.tab[index].key == element.key or self.tab[index].val == None:
                self.tab[index] = element       
                return      
                                 
        #jeśli nic nie znalazło znaczy że lista jest zapełniona
        # raise NoEmptySpaces
        print("Brak miejsca, lista pełna")
        
  

    def search(self, key):
        index = self.hashing(key)
        found = self.tab[index]
      
        # jak to znalezionme po hashowaniu ma ten sam klucz to bez problemu
        if found.key == key:
            return found.val
        #jeśli nie, to znaczy że było użyte sondowanie
        else:
            return self.probing(Element(key, None), key)
            
    def insert(self, element: Element):
        index = self.hashing(element.key)
        # dwie sytuacje kiedy chcemu nadpisać miejsce: kiedy jest puste (czyli None) albo jest tam element który ma ten sam klucz, wtedy zmieniam jego value
        if self.tab[index] == None or self.tab[index].key == element.key:
            self.tab[index] = element                              
            return 
        # teraz naprawianie konfliktu, czyli miejsce pod indeksem jest zajęte przez inny element
        self.probing(element)
        
      
    def remove(self, key):
        index = self.hashing(key)
        if self.tab[index].key == key:
            self.tab[index].val = None
            return
        probed_index = self.probing(Element(key, None), key)
        self.tab[probed_index].val = None
                
    def __str__(self):
        result = ''
        for element in self.tab:
            result += str(element) 
            result += " "
        return result

def main():
    def test1(size, c1=1, c2=0):
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
            hash = Hash_table(size, c1, c2)
            for i in range(1, 16):
                if i == 6:
                    hash.insert(Element(18, letters[i-1]))
                elif i == 7:
                    hash.insert(Element(31, letters[i-1]))
                else:
                    hash.insert(Element(i, letters[i-1]))
            print(hash)
            print(hash.search(5))
            print(hash.search(14))
            hash.insert(Element(5, 'Z'))
            print(hash.search(5))
            hash.remove(5)
            print(hash)
            print(hash.search(31))
            hash.insert(Element('test', 'W'))
            print(hash)


    def test2(size, c1 = 1, c2 = 0):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
        hash = Hash_table(size, c1, c2)
        for i in range(1, 14):
            hash.insert(Element(13*i, letters[i-1]))
        print(hash)

    test1(13)
    test2(13)
    test2(13, 0, 1)
    test1(13, 0, 1)

main()

def test():
        
        def test1(size, c1 = 1, c2 = 0):
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
            hash = Hash_table(size, c1, c2)
            for i in range(1, 16):
                if i == 6:
                    hash.insert(Element(18, letters[i-1]))
                elif i == 7:
                    hash.insert(Element(31, letters[i-1]))
                else:
                    hash.insert(Element(i, letters[i-1]))
            #wypisanie tablicy, działa tak bo dodano __str__
            print(hash)
            print("Szukam wartości z kluczem 5")
            print(hash.search(5))
            print("Szukam wartości z kluczem 14")
            print(hash.search(14))
            print("Insert Z pod kluczem 5")
            hash.insert(Element(5, 'Z'))
            print(hash.search(5))
            print("Usunięcie 5")
            hash.remove(5)
            print(hash)
            print("Wyszukanie danej o kluczu 31")
            print(hash.search(31))
            print("Insert wartości W o kluczu test")
            hash.insert(Element('test', 'W'))
            print(hash)


        def test2(size, c1 = 1, c2 = 0):
            letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
            hash = Hash_table(size, c1, c2)
            for i in range(1, 14):
                hash.insert(Element(13*i, letters[i-1]))
            print(hash)
        
        print("TEST 1")
        test1(13)
        print("TEST 2: próbkowanie liniowe")
        test2(13)
        #próbkowanie kwadratowe, zmieniam wartości c1 i c2
        print("TEST 2: próbkowanie kwadratowe")
        test2(13, 0, 1)
        print("TEST1: próbkowanie kwadratowe")
        test1(13, 0, 1)

# test()