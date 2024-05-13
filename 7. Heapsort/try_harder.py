#NIESKOŃCZONE

class Node():
    def __init__(self, key, data):
        self.__key = key
        self.__data = data

    def __lt__(self, other):
        return self.__key < other.__key

    def __gt__(self, other):
        return self.__key >other.__key
    
    def __repr__(self):
        return f"{self.__key}: {self.__data}"
    
class Heap:
    def __init__(self, to_sort_ = None):
        self.heap_size = 0
        self.heap = []
#dodaję dodatkowy parametr określający elementy do posortowania
        if to_sort_ != None:
            self.heap = to_sort_  
            self.heap_size = len(self.heap)
            for i in reversed(range(self.heap_size)):
                # if self.to_sort[self.left(i)] != None and self.to_sort[self.right(i)] != None:
                if self.left(i) < self.heap_size and self.heap[self.left(i)] != None:
                    self.dequeue_repair(i)
                i-=1

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
        if left >= self.heap_size:
            return 
        max_idx = i
        if self.heap[left] > self.heap[i]:
            max_idx = left
        if right < self.heap_size and self.heap[right] > self.heap[max_idx]:
            max_idx = right

        if max_idx != i:
            self.heap[i], self.heap[max_idx] = self.heap[max_idx], self.heap[i]
            self.dequeue_repair(max_idx)

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


def test1():
    data = [ Node(key, value) for key,value in  [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]]

    test = Heap(data)
    test.print_tab()
    test.print_tree(0, 0)



test1()

# main()