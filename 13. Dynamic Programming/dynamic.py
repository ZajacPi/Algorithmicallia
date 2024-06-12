import numpy as np
import time

def rekurencyjnie(P, T, i=None, j=None):

    if i == None:
        i = len(P)-1
        j = len(T)-1

    if i == 0:
        return j
    if j == 0:
        return i
    
    switch   = rekurencyjnie(P, T, i-1, j-1) + (P[i] != T[j])
    insert = rekurencyjnie(P, T, i, j-1) + 1
    delete  = rekurencyjnie(P, T, i-1, j) + 1
 
    min_cost = min(switch, insert, delete)
   
    return min_cost
    


def PD_method(P, T):
    lenP = len(P)
    lenT =len(T)
    
    #tworzę macierz D i pierwszy wiersz i pierwszą kolumnę wypełniam
    D = np.zeros((lenP, lenT))
    for x in range(lenP):
        D[x][0] = x
    D[0] = [x for x in range(lenT)]
    #tworzę macierz P, dwypełniam domyślną literą X i zmieniam pierwszy wiersz i kolumnę
    parents = np.full((lenP, lenT), 'X')
    for x in range(1, lenP):
        parents[x][0] = 'D'
    parents[0] = ['I' for x in range(lenT)]
    #upewniam się że na pierwszej pozycji została domyślna wartość
    parents[0][0] = 'X'

    for i in range(1, lenP):
        for j in range(1, lenT):
            switch = D[i-1][j-1] + (P[i]!=T[j])
            insert = D[i][j-1] + 1
            delete = D[i-1][j] + 1

            min_cost = min(switch, insert, delete)
            D[i][j] = min_cost
            #jak wyszła zamiana to muszę sprawdzić czy rzeczywiście doszło do zamiany
            if min_cost == switch:
                if P[i] == T[j]:
                    parents[i][j] = 'M'  
                else:
                    parents[i][j] = 'S'  
            elif min_cost == delete:
                parents[i][j] = 'D'
            elif min_cost == insert:
                parents[i][j] = 'I'
           
    result = D[lenP-1][lenT-1]
    return result, parents

def search_path(parent):
    X, Y = parent.shape
    operations = []
    i = X-1
    j = Y-1
    found = parent[i][j]
    #pętla działa aż nie dojdę do pierwszej pozycji, czyli domyślnej wartości
    while found != 'X':
        operations.append(found)
        if found == 'M' or found == 'S':
            i -= 1
            j -= 1
        elif found == 'D':
            i -= 1
        elif found == 'I':
            j -= 1
        found = parent[i][j]
    result = ''
    #muszę odwrócić wyraz
    for i in reversed(range(len(operations))):
        result += operations[i]
    return result

#
def goal_cell(P, T, D):
    i = len(P)-1
    j = 0
    for k in range(1, len(T)):
        if D[i][k] < D[i][j]: 
            j = k  
    return j



def search_subtext(P, T, i=None, j=None):
    lenP = len(P)
    lenT =len(T)
    #tym razem nie zmieniam pierwszego rzędu w obu macierzach
    D = np.zeros((lenP, lenT))
    for x in range(lenP):
        D[x][0] = x

    parents = np.full((lenP, lenT), 'X')
    for x in range(1, lenP):
        parents[x][0] = 'D'

    for i in range(1, lenP):
        for j in range(1, lenT):
            switch = D[i-1][j-1] + (P[i] != T[j])
            insert = D[i][j-1] + 1
            delete = D[i-1][j] + 1

            min_cost = min(switch, insert, delete)
            D[i][j] = min_cost
            #jak wyszła zamiana to muszę sprawdzić czy doszło do zamiany
            if min_cost == switch:
                if P[i] == T[j]:
                    parents[i][j] = 'M'  
                else:
                    parents[i][j] = 'S'  
                    D[i][j]+=1
            elif min_cost == delete:
                parents[i][j] = 'D'
                
            elif min_cost == insert:
                parents[i][j] = 'I'
    # zwracam indeks najmniejszej wartości w ostatnim wierszu macierzy D
    return goal_cell(P, T, D)
      
def longest_common_sequence(P, T):
    lenP = len(P)
    lenT = len(T)
    D = np.zeros((lenP + 1, lenT + 1))
    
    parents = np.full((lenP+1, lenT+1), 'X')
    
    #ulepszona wersja algorytmu
    for i in range(1, lenP + 1):
        for j in range(1, lenT + 1):
            #zamiast szukać najmniejszej wartości, tym razem od razu sprawdzę czy litery są takie same
            if P[i - 1] == T[j - 1]:
                D[i][j] = D[i - 1][j - 1] + 1
                parents[i][j] = 'M' 
            else:
                insert = D[i][j-1] 
                delete = D[i-1][j] 
                
                if delete >= insert:
                    D[i][j] = delete
                    parents[i][j] = 'D' 
                else:
                    D[i][j] = insert
                    parents[i][j] = 'I'
                #nie daję opcji zamiany
    
    #teraz odzyskuję napis na podstawie ścieżki
    i, j = lenP, lenT
    lcs = ''
    while i > 0 and j > 0:
        #jak nie doszło do zamiany to dopisuję
        if parents[i][j] == 'M':
            lcs += P[i - 1]
            i -= 1
            j -= 1
        #jak usunięcie albo podstawienie to muszę się odpowiednio przesunąć
        elif parents[i][j] == 'D':
            i -= 1
        else: 
            j -= 1
    # musi być odczytane od tyłu
    lcs_reverse = lcs[::-1]
    
    return D[lenP][lenT], lcs_reverse


def test1():
    P = ' kot'
    T = ' koń'    
    cost1 = rekurencyjnie(P, T)
    print(f"Koszt obliczony rekurencyjnie dla {P} i {T}: {cost1}")
    cost2 = PD_method(P, T)
    print(f"Koszt obliczony metodą PD dla {P} i {T}: {cost2}")
    print("#####################################################\n")


def test_a():
    P = ' kot'
    T = ' pies'
    
    t_start = time.perf_counter()
    cost1 = rekurencyjnie(P, T) 
    t_stop = time.perf_counter()
    calc_time = t_stop - t_start
    
    print("Test a)")
    print(f"Koszt obliczony rekurencyjnie dla {P} i {T}: {cost1}")
    print(f"Czas obliczeń: {calc_time}")
    print("#####################################################\n")


def test_b():
    P = ' biały autobus'
    T = ' czarny autokar'
    t_start = time.perf_counter()
    cost, _ = PD_method(P, T) 
    t_stop = time.perf_counter()
    calc_time = t_stop - t_start
    
    print("Test b)")
    print(f"Koszt obliczony metodą PD dla {P} i {T}: {cost}")
    print(f"Czas obliczeń: {calc_time}")
    print("#####################################################\n")

def test_c():
    P = ' thou shalt not'
    T = ' you should not'
    _, parents = PD_method(P, T) 
    path = search_path(parents)
    
    print("Test c)")
    print(f"Ścieżka odtworzona z {P} i {T}: {path}")
    # print("DSMMMMMISMSMMMM")
    print("#####################################################\n")

def test_d():
    P = ' ban'
    T = ' mokeyssbanana'
    index= search_subtext(P, T)
    print("Test d)")
    print(f"Wzorzec zaczyna się na pozycji {index-len(P)+1}")
    print(f"Wzorzec: {P}\nZnaleziony podciąg: {T[(index-len(P)+1):index+1]}")
    print("#####################################################\n")
    
def test_e():
    P = ' democrat'
    T = ' republican'
    cost, lcs= longest_common_sequence(P, T)
    print("Test e)")
    print(f"Najdłuższa podsekwencja: {lcs}")
    print("#####################################################\n")
    
def test_f():
    T = ' 243517698'
    #wyciągam liczby z napisu
    digits = [char for char in T if char.isdigit()]
    digits.sort()
    P = ' ' +  ''.join(digits)
    cost, lcs= longest_common_sequence(P, T)
    print("Test f)")
    print(f"Najdłuższa podsekwencja monotoniczna: {lcs}")
    print("#####################################################\n")

def main():
    # test1()
    test_a()
    test_b()
    test_c()
    test_d()
    test_e()
    test_f()

if __name__ == '__main__':
    main()