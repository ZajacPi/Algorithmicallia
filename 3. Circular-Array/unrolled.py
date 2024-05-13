#rozmiar tablicy w zmiennej globalnej 
size = 6
class Unrolled_element:
    def __init__(self):
        self.counter = 0
        self.tab =  [None for i in range(size)]
        self.front = None
    
class Unrolled_list:
    def __init__(self, size_):
        self.tab = []
        self.size = size_
        self.head = None
        self.rear = None
        
    def get(self, index):
        
        pass
    
    def insert(self, index, data):
        pass
        
        # Podanie indeksu większego od aktualnej liczby elementów listy skutkuje wstawieniem danej na końcu listy.
        if index > self.size:
            pass
    def delete(self, index):
        pass
    
    def __str__(self):
        pass
    
def main():
    size = 6
    unrolled = Unrolled_list(size)
    for i in range(1, 10):
        unrolled.insert(i)
    unrolled.get(3)
    unrolled.insert(1, 10)
    unrolled.insert(8, 11)
    print(unrolled)
    unrolled.delete(1)
    unrolled.delete(2)
    print(unrolled)


def test():
    unrolled = Unrolled_list(size)
    for i in range(1, 10):
        unrolled.insert(i)
    unrolled.get(3)
    unrolled.insert(1, 10)
    unrolled.insert(8, 11)
    print(unrolled)
    unrolled.delete(1)
    unrolled.delete(2)
    print(unrolled)
