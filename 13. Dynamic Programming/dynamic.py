import numpy as np
def rekurencyjnie(P, T, i=None, j=None):
    
    if i == None:
        i = len(P)-1
        j = len(T)-1

    if i == 0:
        return j
    if j == 0:
        return i
    
    zamian   = rekurencyjnie(P, T, i-1, j-1) + (P[i] != T[j])
    wstawień = rekurencyjnie(P, T, i, j-1) + 1
    usunięć  = rekurencyjnie(P, T, i-1, j) + 1
 
    najniższy_koszt = min(zamian, wstawień, usunięć)
   
    return najniższy_koszt
    


def PD_method(P, T, i = None, j = None):
    lenP = len(P)
    lenT =len(T)
    D = np.zeros((lenP, lenT))
    for x in range(lenP):
        D[x][0] = x
    D[0] = [x for x in range(lenT)]

    parents = np.full((lenP, lenT), 'X')
    for x in range(lenP):
        parents[x][0] = 'D'
    parents[0] = ['I' for x in range(lenT)]
    parents[0][0] = 'X'

    if i == None:
        i = lenP-1
        j = lenT-1

    for i in range(1, lenP):
        for j in range(1, lenT):
            zamian = D[i-1][j-1] + (P[i]!=T[j])
            wstawień = D[i][j-1] + 1
            usunięć = D[i-1][j] + 1

            najniższy_koszt = min(zamian, wstawień, usunięć)
            D[i][j] = najniższy_koszt
            #jak wyszła zamiana to muszę sprawdzić czy doszło do zamiany
            if najniższy_koszt == zamian:
                if P[i] == T[j]:
                    parents[i][j] = 'M'  
                else:
                    parents[i][j] = 'S'  
            elif najniższy_koszt == usunięć:
                parents[i][j] = 'D'
            elif najniższy_koszt == wstawień:
                parents[i][j] = 'I'
           
    result = D[lenP-1][lenT-1]
    return result, parents

def search_path(parent):
    X, Y = parent.shape
    operations = []
    i = X-1
    j = Y-1
    found = parent[i][j]
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
    for i in reversed(range(len(operations))):
        result += operations[i]
    return result

def goal_cell(P, T, D):
    i = len(P)-1
    j = 0
    for k in range(1, len(T)):
        if D[i][k] < D[i][j]: 
            j = k  
    return j



def search_subtext(P, T):
    lenP = len(P)
    lenT =len(T)
    #tym razem nie zmieniam pierwszego rzędu
    D = np.zeros((lenP, lenT))
    for x in range(lenP):
        D[x][0] = x

    parents = np.full((lenP, lenT), 'X')
    for x in range(1, lenP):
        parents[x][0] = 'D'

    if i == None:
        i = lenP-1
        j = goal_cell()

    for i in range(1, lenP):
        for j in range(1, lenT):
            zamian = D[i-1][j-1] + (P[i]!=T[j])
            wstawień = D[i][j-1] + 1
            usunięć = D[i-1][j] + 1

            najniższy_koszt = min(zamian, wstawień, usunięć)
            D[i][j] = najniższy_koszt
            #jak wyszła zamiana to muszę sprawdzić czy doszło do zamiany
            if najniższy_koszt == zamian:
                if P[i] == T[j]:
                    parents[i][j] = 'M'  
                else:
                    parents[i][j] = 'S'  
            elif najniższy_koszt == usunięć:
                parents[i][j] = 'D'
            elif najniższy_koszt == wstawień:
                parents[i][j] = 'I'
           
    result = D[lenP-1][lenT-1]
    return result, parents
    

        

    




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
    cost1 = rekurencyjnie(P, T) 
    print(f"Koszt obliczony rekurencyjnie dla {P} i {T}: {cost1}")
   
    # cost2 = PD_method(P, T)
    # print(f"Koszt obliczony metodą PD dla {P} i {T}: {cost2}")
    # print("#####################################################\n")

def test_b():
    P = ' biały autobus'
    T = ' czarny autokar'
    cost, _ = PD_method(P, T) 
    print(f"Koszt obliczony metodą PD dla {P} i {T}: {cost}")
    print("#####################################################\n")

def test_c():
    P = ' thou shalt not'
    T = ' you should not'
    _, parents = PD_method(P, T) 
    path = search_path(parents)
    print(f"Ścieżka odtworzona z {P} i {T}: {path}")
    print(path)
    print("DSMMMMMISMSMMMM")
    print("#####################################################\n")

def test_d():
    P = ' ban'
    T = ' mokeyssbanana'
    cost, j= search_subtext_main(P, T)
    print(f"Minimalny koszt z {P} i {T}: {cost}")
    print(f"Wzorzec zaczyna się na pozycji {j}")
    print("#####################################################\n")

def main():
    # test1()
    # test_a()
    # test_b()
    # test_c()
    test_d()

if __name__ == '__main__':
    main()