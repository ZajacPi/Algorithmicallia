#NIESKOŃCZONE
import random
import time
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

        # Set the last element to the root and remove the last element
        self.heap[0] = self.heap[self.heap_size - 1]
        self.heap[self.heap_size - 1] = None
        self.heap_size -= 1

        # Repair the heap property
        self.dequeue_repair(0)

        return deleted

    def dequeue_repair(self, i):
        left = self.left(i)
        right = self.right(i)
        #mocno uproszczona i poprawiona dequeue_repair
        #jak doszliśmy tak głęboko że szukamy indeksów które nie istnieją musimy przerwać
        if left >= self.heap_size-1:
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

def selection_sort_swap(to_sort):
    n = len(to_sort)
    for i in range(n - 1):
        min_i = i
        for j in range(i + 1, n):
            if to_sort[j] < to_sort[min_i]:
                min_i = j
        if min_i != i:
            to_sort[i], to_sort[min_i] = to_sort[min_i], to_sort[i]
    return to_sort

def swap_sort(to_sort):
    n = len(to_sort)
    for i in range(n - 1):
        #szukam największego elementu
        max_i = i
        for j in range(i + 1, n):
            #jeśli większy od max_i do zastępuję
            if to_sort[j] > to_sort[max_i]:
                max_i = j
        # swap       
        if max_i != i:
            temp = to_sort[i] 
            to_sort[i] = to_sort[max_i]
            to_sort[max_i] = temp
    return to_sort

def shift_sort(lst):
    n = len(lst)
    #iteruję podobnie jak w swapsort i szukam największego
    for i in range(n - 1):
        max_i = i
        for j in range(i + 1, n):
            if lst[j] > lst[max_i]:
                max_i = j
        if max_i != i:
            #usuwa się najmniejszy element i wstawiam na przed aktualne i
            item = lst.pop(max_i)
            lst.insert(i, item)
    return lst

def test1():
    data1 = [ Node(key, value) for key,value in  [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]]
    data2 = [ Node(key, value) for key,value in  [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]]
    print(f"Nieposortowana: \n{data1}")
    sorted1 = swap_sort(data1)
    print(f"Swap-sort: \n{sorted1}")
    sorted2 = swap_sort(data2)
    print(f"Shift-sort: \n{sorted2}")


def test2():
    #tworzę kopie tablicy bo sortowanie jest in-situ
    random_numbers = [random.randint(0, 99) for _ in range(10000)]
    random_numbers2 = random_numbers.copy()
    random_numbers3 = random_numbers.copy()
    #heapsort
    t_start = time.perf_counter()
    test = Heap(random_numbers)
    sorted = []
    while test.heap_size != 0:
        sorted.append(test.dequeue())
    t_stop = time.perf_counter()
    print("Czas obliczeń dla heapSort:", "{:.7f}".format(t_stop - t_start))
    # swap_sort
    t_start = time.perf_counter()
    result1 = swap_sort(random_numbers2)
    t_stop = time.perf_counter()
    print("Czas obliczeń dla swapSort:", "{:.7f}".format(t_stop - t_start))
    #shift_sort
    t_start = time.perf_counter()
    result2 = shift_sort(random_numbers3)
    t_stop = time.perf_counter()
    print("Czas obliczeń dla shiftSort:", "{:.7f}".format(t_stop - t_start))

test1()
test2()
