#NIESKOŃCZONE
def chio(matrix, first = None, swapped = False):
    #jeśli wołamy funkcję po raz pierwszy, tworzę pustą listę dla pierwszych elementów
    if first is None:
        first = []
    n = len(matrix)
    
    if n == 1:
        return matrix[0][0]
    
    # jeśli element a1,1 jest równy 0 to muszę zamienić go z innym wierszem którego pierwszy element jest niezerowy
    check = n
    while matrix[0][0] == 0:

        temp_row = matrix[0]
        matrix[0] = matrix[check-1]
        matrix[check-1] = temp_row
        check -= 1
        #jeśli dokonaliśmy zmiany wiersza zapamiętuję to za pomocą zmiennej swapped, domyślnie ustawionej na False
        swapped = not swapped 
        
        # jesli licznik dobił do 0, to wszystkie elementy w pierwszej kolumnie są równe 0
        if check == 0:  
            return 0
        
    #  kiedy będzie długość 2, to wszystkie first wymnożone pomnożę razy wyznacznik macierzy 2x2
    if n == 2:  
        last_det = matrix[0][0] * matrix [1][1] - matrix[1][0]* matrix[0][1]
        #jeśli zamienialiśmy miejscami wiersze nieparzystą ilość razy, czyli swapped jest ustawiona na True, to mnożę wyznacznik *-1
        if swapped:
            multiplier = -1
        else:
            multiplier = 1
            
        for i in first:
            multiplier *= i
        return last_det /multiplier
    
    #tworzę pustą funkcję o wymiarze o jeden mniejszym niż aktualna macierz
    simplified = [[0]*(n-1) for _ in range(n-1)]

    first.append(matrix[0][0]**(n-2))
    for i in range(n-1):
        for j in range(n-1):
            simplified[i][j] = matrix[0][0]*matrix[i+1][j+1] - matrix[i+1][0]*matrix[0][j+1]
            
    return chio(simplified, first, swapped)


m1 = [

[5 , 1 , 1 , 2 , 3],

[4 , 2 , 1 , 7 , 3],

[2 , 1 , 2 , 4 , 7],

[9 , 1 , 0 , 7 , 0],

[1 , 4 , 7 , 2 , 2]

]
m2 =  [
     [0 , 1 , 1 , 2 , 3],
     [4 , 2 , 1 , 7 , 3],
     [2 , 1 , 2 , 4 , 7],
     [9 , 1 , 0 , 7 , 0],
     [1 , 4 , 7 , 2 , 2]
    ]
print(chio(m1))
print(chio(m2))

#TEST ZMIANY WIERSZA, tak aby a1,1 nie było równe 0
m3 =  [
     [0 , 1 , 1 , 2 , 3],
     [9 , 2 , 1 , 7 , 3],
     [0 , 1 , 2 , 4 , 7],
     [0 , 1 , 0 , 7 , 0],
     [0 , 4 , 7 , 2 , 2]
    ]
# print(chio(m3))

#TEST MACIERZY Z WSZYSTKIMI ELEMENTAMI 0 W PIERWSZEJ KOLUMNIE
m4 =  [
     [0 , 1 , 1 , 2 , 3],
     [0 , 2 , 1 , 7 , 3],
     [0 , 1 , 2 , 4 , 7],
     [0 , 1 , 0 , 7 , 0],
     [0 , 4 , 7 , 2 , 2]
    ]
# print(chio(m4))