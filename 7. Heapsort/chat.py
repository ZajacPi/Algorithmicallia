import random
import time
class Elem:
    def __init__(self,priority,data) -> None:
        
        self.__data = data
        self.__priority = priority
    
    def __lt__(self,other):
        return self.__priority < other.__priority

    def __gt__(self,other):
        return self.__priority > other.__priority
    
    def __repr__(self):
        return (f"{self.__priority} : {self.__data}")

class Pqueue:
    def __init__(self,el_to_sort = None) -> None:
        if el_to_sort is not None:
            self.queue = el_to_sort
        self.heap_size = len(self.queue)
        # self.elems_to_sort = el_to_sort
        if self.queue is not None:
            for i in reversed(range(len(self.queue))):
                idx_left = self.left(i)
                if idx_left < len(self.queue):
                    self.fix_sort_heap(i)
        

    def is_empty(self):
        if not self.queue:
            return True
        return False

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[0]


    def dequeue(self):
        if self.is_empty():
            return None
        deq = self.queue[0]
        self.queue[0] = self.queue[self.heap_size - 1]
        self.queue = self.queue[:-1]
        self.heap_size -= 1
        self.fix_sort_heap(0)
        return deq

    def fix_sort_heap(self,idx):
        left_idx = self.left(idx)
        right_idx = self.right(idx)
        largest = idx
        if left_idx < self.heap_size and self.queue[left_idx] > self.queue[idx]:
            largest = left_idx
        if right_idx < self.heap_size and self.queue[right_idx] > self.queue[idx]:
            if self.queue[right_idx] > self.queue[left_idx]:
                largest = right_idx
        if largest != idx:
            temp = self.queue[idx]
            self.queue[idx] = self.queue[largest]
            self.queue[largest] = temp
            self.fix_sort_heap(largest)


    def left(self,idx):
        return idx * 2 + 1
        

    def right(self,idx):
        return idx * 2 + 2

    def parent(self,idx):
        if idx == 0:
            return 0
        return (idx) // 2

    def print_tab(self):
        print ('{', end=' ')
        print(*self.queue[:len(self.queue)], sep=', ', end = ' ')
        print( '}')

    def print_tree(self, idx, lvl):
        if idx<len(self.queue):           
            self.print_tree(self.right(idx), lvl+1)
            print(2*lvl*'  ', self.queue[idx] if self.queue[idx] else None)           
            self.print_tree(self.left(idx), lvl+1)
    

def main():
    
    data = [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]    
    tab = [ Elem(key, value) for key,value in  data]
    heap_tab = Pqueue(tab)
    heap_tab.print_tab()
    heap_tab.print_tree(0,0)
    deq = 0
    while deq != None:
        deq = heap_tab.dequeue()
        if deq != None:
            print(deq)
    heap_tab.print_tab()

def test2():
    tab = []
    while len(tab) < 10000:
        tab.append(int(random.random() * 100))
    
    tab_t_s = [Elem(key,'A') for key in tab]
    t_start = time.perf_counter()
    # testowana metoda
    heap = Pqueue(tab_t_s)
    t_stop = time.perf_counter()
    print("Czas obliczeĹ:", "{:.7f}".format(t_stop - t_start))

main()
test2()