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
    def __init__(self, to_sort_=None, method = None):
        self.heap_size = 0
        self.heap = []
        if to_sort_ != None:
            if method == None:
                print("Brak podanej metody!")
                return 
            self.heap = to_sort_  
            self.heap_size = len(self.heap)

            if method=="swap_sort":
                for i in range(self.heap_size - 1):
                    max = i
                    for j in range(i + 1, self.heap_size):
                        if self.heap[j] > self.heap[max]:
                            max = j
                    if max != i:
                        self.heap[i], self.heap[max] = self.heap[max], self.heap[i]
                
            elif method == "shift_sort":
                for i in range(self.heap_size - 1):
                    max = i
                    for j in range(i + 1, self.heap_size):
                        if self.heap[j] > self.heap[max]:
                            max = j
                    if max != i:
                        item = self.heap.pop(max)
                        self.heap.insert(i, item)

    def is_empty(self):
        if len(self.heap) == 0:
            return True
        return False
    def swap(self):
        pass
    def shift(self):
        pass
    def peek(self):
        if self.is_empty():
            return None
        return self.heap[0]
    
    def dequeue(self):
        if self.is_empty():
            return None
    
        deleted = self.heap[0]
        last_index = self.heap_size - 1
        self.heap[0] = self.heap[last_index]
        self.heap[last_index] = None
        self.dequeue_repair(0)
        self.heap_size -= 1
        return deleted

    def dequeue_repair(self, i):
        left = self.left(i)
        right = self.right(i)
        if right > self.heap_size-1 or left > self.heap_size-1:
            return
        swapp = self.heap[i]
        if swapp < self.heap[left]:
            if swapp < self.heap[right]:
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
            temp = self.heap[left]
            self.heap[left] = swapp
            self.heap[i] = temp
            return self.dequeue_repair(left)

        else:
            return None 

    def enqueue(self, element):
        if len(self.heap) == self.heap_size:
            self.heap.append(element)
            self.heap_size += 1

        else:
            self.heap[self.heap_size] = element
            self.heap_size += 1
        
        i = self.heap_size - 1
        parent_i = self.parent(i)
        if  self.heap[i] != None and self.heap[parent_i] != None:
            while self.heap[i] > self.heap[parent_i]:
                temp = self.heap[parent_i]
                self.heap[parent_i] = self.heap[i]
                self.heap[i] = temp
                i =  parent_i
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
    pass


def test1():
    data = [ Node(key, value) for key,value in  [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]]
    test1 = Heap(data, "swap_sort")
    test1.print_tab()
    test1.print_tree(0, 0)
    test2 = Heap(data, "shift_sort")
    test2.print_tab()
    test2.print_tree(0, 0)

def test2():
    random_numbers = [random.randint(0, 99) for _ in range(10000)]
    test = Heap(random_numbers, "")
    sorted = []

    t_start = time.perf_counter()
    while test.heap_size != 0:
        sorted.append(test.dequeue())
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

test1()
test2()