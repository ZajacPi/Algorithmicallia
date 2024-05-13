#NIESKOŃCZONE

#używam elementu Node, ale program ma być uniwersalny, czyli można wrzucać cokolwiek!
#kopiec ma działać dla dowolnej tablicy dowolnych elementów które można porównać (priority)

class Node():
    def __init__(self, key, data):
        self.__key = key
        self.__data = data

    #przy porównaniu obiekt1>obiekt2 dla obiektów tego typu będzie zwracało bool
    def __lt__(self, other):
        return self.__key < other.__key

    #przy porównaniu obiekt1 > obiekt2 dla obiektów tego typu będzie zwracało bool
    def __gt__(self, other):
        return self.__key >other.__key
    
    def __repr__(self):
        return f"{self.__key}: {self.__data}"
    
class Heap:
    def __init__(self):
        #jest to rozmiar KOPCA, ale nie tablicy
        self.heap_size = 0
        self.heap = []

    def is_empty(self):
        if len(self.heap) == 0:
            return True
        return False

    def peek(self):
        if self.is_empty():
            return None
        return self.heap[0]
    
    def dequeue(self):
        if self.is_empty():
            return None
    
        deleted = self.heap[0]
        
        # biorę ostatni element i wrzucam na pierwze miejsce a ostatni usuwam, porównuję z lewym i prawym dzieckiem i idę 
        # w stronę większego
        last_index = self.heap_size - 1
        self.heap[0] = self.heap[last_index]
        self.heap[last_index] = None
        self.dequeue_repair(0)
        # długość listy ma zostać taka sama, ale zmniejszam długość kopca
        self.heap_size -= 1
        return deleted

    def dequeue_repair(self, i):
        left = self.left(i)
        right = self.right(i)
        #jak doszliśmy tak głęboko że szukamy indeksów które nie istnieją musimy przerwać
        if right > self.heap_size-1 or left > self.heap_size-1:
            return
        swapp = self.heap[i]
        if swapp < self.heap[left]:
            if swapp < self.heap[right]:
                #zamieniam z WIĘKSZYM z tej dwójki
                if self.heap[left] > self.heap[right]:
                    temp = self.heap[left]
                    self.heap[left] = self.heap[i]
                    self.heap[i] = temp
                    return self.dequeue_repair(left)
                else:
                    temp = self.heap[right]
                    self.heap[right] = self.heap[i]
                    self.heap[i] = temp
                    return self.dequeue_repair(right)
            #prawy jest większy więc zamieniam z lewym, to sie chyba da zoptymalizować
            temp = self.heap[left]
            self.heap[left] = swapp
            self.heap[i] = temp
            return self.dequeue_repair(left)

        #dzieci są mniejsze, zwracam none
        else:
            return None 

    def enqueue(self, element):
        #jeśli rozmiar koca równy rozmiarowi tablicy to append
        if len(self.heap) == self.heap_size:
            self.heap.append(element)
            self.heap_size += 1

        #Kiedy usuwam jakiś element to nie skracam listy, więc mogą być puste miejsca
        else:
            self.heap[self.heap_size] = element
            self.heap_size += 1
        
        #daję na koniec, i teraz bubblesort
        i = self.heap_size - 1
        parent_i = self.parent(i)
        if  self.heap[i] != None and self.heap[parent_i] != None:
            while self.heap[i] > self.heap[parent_i]:
                temp = self.heap[parent_i]
                self.heap[parent_i] = self.heap[i]
                self.heap[i] = temp
                i =  parent_i
                #dobra hamuj, jesteś już największy!
                if i == 0:
                    return 
                parent_i = self.parent(parent_i)


    # funkcje pomocnicze
    def parent(self, index):
        return (index-1)//2
    def left(self, index):
        return 2*index+1
    def right(self, index):
        return 2*index+2
    
    def print_tab(self):
        print ('{', end=' ')
        print(*self.heap[:self.heap_size], sep=', ', end = ' ')
        print( '}')

    def print_tree(self, idx, lvl):
        if idx<self.heap_size:           
            self.print_tree(self.right(idx), lvl+1)
            print(2*lvl*'  ', self.heap[idx] if self.heap[idx] else None)           
            self.print_tree(self.left(idx), lvl+1)


def main():
    test = Heap()
    keys = [7, 5, 1, 2, 5, 3, 4, 8, 9]
    data = ['G', 'R', 'Y', 'M', 'O', 'T', 'Y', 'L', 'A']

    for i in range(len(keys)):
        node = Node(keys[i], data[i])
        test.enqueue(node)

    test.print_tree(0, 0)
    test.print_tab()
    deleted1 = test.dequeue()
    print(test.peek())
    test.print_tab()
    print(deleted1)
    while test.heap_size != 0:
        print(test.dequeue())
    test.print_tab()


def test():
    test = Heap()
    keys = [7, 5, 1, 2, 5, 3, 4, 8, 9]
    data = ['G', 'R', 'Y', 'M', 'O', 'T', 'Y', 'L', 'A']
    for i in range(len(keys)):
        node = Node(keys[i], data[i])
        test.enqueue(node)
    test.print_tree(0, 0)
    test.print_tab()
    deleted1 = test.dequeue()
    test.print_tree(0, 0)
    print(f"Usunięto: {deleted1}")
    print(f"Pierwsza dana: {test.peek()}")
    test.print_tab()
    print(deleted1)
    #opróżnienie kolejki
    while test.heap_size != 0:
        test.dequeue()
    test.print_tab()
    keys = [7, 5, 1, 2, 5,]
    data = ['G', 'R', 'Y', 'M', 'O']
    for i in range(len(keys)):
        node = Node(keys[i], data[i])
        test.enqueue(node)
    test.print_tab()


# test()
main()