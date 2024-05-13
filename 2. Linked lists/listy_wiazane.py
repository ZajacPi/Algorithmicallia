
class linked_2:
    def __init__(self, university_):
        self.university = university_
        self.next = None

class linked:
    def __init__(self):
        self.head = None

    def create():
        pass

    def destroy(self):
        self.head = None

    def add(self, university):
        new_uni = linked_2(university)
        #sprawdzam czy przypadkliem lista nie jest pusta
        if self.head == None:
            self.head = new_uni
            return 0
        #wystarczy ustawić dla nowego elementu next jako nasz head, wtedy będzie przed nim
        new_uni.next = self.head
        # na koniec ustawiam nowy element jako head
        self.head = new_uni 

    def append(self, university):
        new_uni = linked_2(university)
        #sprawdzam czy przypadkliem lista nie jest pusta
        if self.head == None:
            self.head = new_uni
            return 0
        last_uni = self.head #idę od początku, czyli że last uni będzie pierwszym
        #elementem i będę szedł do przodu aż dobiję elementu który za next ma ustawione None
        while(last_uni.next != None):
            last_uni = last_uni.next
        #jak już dobiłem to za tego next ustawiam nowy element, który next ma ustawione na None
        last_uni.next = new_uni
        
    def remove(self):
        # zabezpieczenie przed sytuacją usuwania elementu z pustej listy
        if self.head == None:
            return
        # po prostu wartość pierwszego elementu zmieniamy na wskaźnik na drugi element
        self.head = self.head.next

    def remove_end(self):
        last_uni = self.head 
        # zabezpieczenie przed sytuacją usuwania elementu z pustej listy
        if last_uni == None:
            return
        #co jeśli jest tylko jeden element?
        if last_uni.next == None:
                self.head = None
                return 
        # jeśli NASTĘPNY, NASTĘPNY ma next jako none to jest ostatni, więc element wcześniej muszę ustawić na None
        while(last_uni.next.next != None):
            last_uni = last_uni.next
        last_uni.next = None
        
    def is_empty(self):
        if self.head == None:
            return True
        else: 
            return False
    
    def length(self):
        size = 0
        current_element = self.head
        #Znowu podobna logika, przechodzimy po kolei i jak znajdziemy None to znaczy że to ostatni element, przerywamy i zwracamy
        while current_element != None:
            size += 1
            current_element = current_element.next
        return size
    
    def get(self):
        return self.head.university
    def display(self):
        current_element = self.head
        while current_element != None: 
            message = '-> ' + str(current_element.university)
            current_element = current_element.next
            print(message)


    



def main():
    universities = [('AGH', 'Kraków', 1919),
    ('UJ', 'Kraków', 1364),
    ('PW', 'Warszawa', 1915),
    ('UW', 'Warszawa', 1915),
    ('UP', 'Poznań', 1919),
    ('PG', 'Gdańsk', 1945)]

    uczelnie = linked()
    for i in range(3):  
        another= universities[i]
        uczelnie.append(another)
    for i in range(3, len(universities)):
        uczelnie.add(universities[i])
    uczelnie.display()
    print(uczelnie.length())
    uczelnie.remove()
    print(uczelnie.get())
    uczelnie.remove_end()
    uczelnie.display()
    uczelnie.destroy()
    print(uczelnie.is_empty())
    uczelnie.remove()
    uczelnie.append(universities[0])
    uczelnie.remove_end()
    print(uczelnie.is_empty())


# main()

def test():
    universities = [('AGH', 'Kraków', 1919),
    ('UJ', 'Kraków', 1364),
    ('PW', 'Warszawa', 1915),
    ('UW', 'Warszawa', 1915),
    ('UP', 'Poznań', 1919),
    ('PG', 'Gdańsk', 1945)]
    uczelnie = linked()
    for i in range(3):  
        another= universities[i]
        uczelnie.append(another)
    for i in range(3, len(universities)):
        uczelnie.add(universities[i])
    uczelnie.display()
    print(f"Ilość uczelni: {uczelnie.length()}")
    uczelnie.remove()
    print(f"Pierwsza uczelnia po usunięciu pierwszej:{uczelnie.get()}")
    uczelnie.remove_end()
    print("Wszystkie uczelnie po usunięciu ostatniej:")
    uczelnie.display()

    uczelnie.destroy()
    print(f"Czy zniszczenie zadziałało: {uczelnie.is_empty()}")

    uczelnie.remove()
    uczelnie.append(universities[0])
    print("Ponowne dodanie uczelni, po próbie usuwania z pustej listy:")
    uczelnie.display()
    uczelnie.remove_end()

    print(f"Czy usunięcie ostatniego elementu jednoelementowej listy zadziałało: {uczelnie.is_empty()}")

# test()
