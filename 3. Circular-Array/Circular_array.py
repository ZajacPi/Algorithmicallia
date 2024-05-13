class cyclic:
    def __init__(self, size_=5):
        
        # na początku tworzę tablicę o danym rozmiarze wypełnioną None
        tab_ = [None for i in range(size_)]

        self.tab = tab_
        self.size = size_
        self.front = 0 
        self.back = 0 

       
    def realloc(self, back):
        oldSize = len(self.tab)
        # realloced = [self.tab[i-oldSize] if i>oldSize else None  for i in range(oldSize*2)]
        reallocked = [None for _ in range(self.size * 2)]
        for i in range(back):
            reallocked[i] = self.tab[i]
        for i in range(oldSize-back):
            reallocked[oldSize+i+1] = self.tab[back]
            back+=1
        self.size = 2*oldSize
        self.tab = reallocked
        self.front += oldSize-1
 

    def is_empty(self):
        #miejsce odczytu równe miejscu zapisu
        if self.front == self.back:
            return True
        else:
            return False

# peek - zwracająca daną z miejsca odczytu lub None dla pustej kolejki
    def peek(self):
        if self.is_empty() == True:
            return None
        return self.tab[self.front]
    


    def dequeue(self):
        #sprawdzam czy pusta
        if self.is_empty() == True:
            return None
        else:
            temp = self.tab[self.front]
            if self.front == self.size-1:
                self.front = 0
            else:
                self.tab[self.front] = None
                self.front+=1
            return temp

    def enqueue(self, elem):
        # # najpierw sprawdzam czy pełna, czyli czy odległosć od back do front jest równa wielkości tablicy????
        self.tab[self.back] = elem
        if self.back == self.size-1:
            self.back = 0
        else:
            self.back += 1

        if self.back == self.front:
            self.realloc(self.back)
        


# __str__ do wypisywania printem obiektu stworzonej klasy ciąg jako wartości od początku kolejki do jej końca zapisany
# w nawiasach [ ] (tak jak lista pythonowa).
    def __str__(self):
        start = self.front
        finish = self.back
        tab_list = []
        while start != finish:
            tab_list.append(self.tab[start])
            start+=1
            if start == self.size:
                start = 0
        print(tab_list)
            
            

    def display(self):
        if self.is_empty() == True:
            print("Pusta lista")
            return 0
        else:
            print(self.tab)

def main():
    circle = cyclic()

    for i in range(1, 5):
        circle.enqueue(i)

    print(circle.dequeue())

    print(circle.peek())

    circle.__str__()

    for i in range(5, 9):
        circle.enqueue(i)

    circle.display()

    while circle.is_empty() == False:
        print(circle.dequeue())
    circle.display()

main()

def test():
    print("Tworzę pustą listę bez podawania rozmiaru")
    circle = cyclic()
    circle.display()
    print("Wpisuję do niej liczby od 1 do 4")
    for i in range(1, 5):
        circle.enqueue(i)
    circle.display()
    print("odczyt pierwszej danej, usunięcie i wypisanie jej")
    print(circle.dequeue())
    print("odczyt drugiej danej i wypisanie jej")
    print(circle.peek())
    print("Ładne wypisanie listy od front do back")
    circle.__str__()
    for i in range(5, 9):
        circle.enqueue(i)
    circle.__str__()
    while circle.is_empty() == False:
        print(circle.dequeue())

# test()