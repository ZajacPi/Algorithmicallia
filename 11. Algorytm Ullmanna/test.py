from Matrix_graph import Matrix_graph, Vertex
import numpy as np
import copy

graph_G = [ ('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
graph_P = [ ('A','B',1), ('B','C',1), ('A','C',1)]

def ullman_test(używane, macierz_M, aktualny_wiersz=0):
    liczba_wierszy = len(macierz_M)
    if aktualny_wiersz == liczba_wierszy:
        print("#############################")
        print(macierz_M)
        return
    for c in range(len(macierz_M[0])):
        if używane[c] == False:
            używane[c] = True
            for i in range(len(macierz_M[0])):
                macierz_M[aktualny_wiersz][i] = 0
            macierz_M[aktualny_wiersz][c] = 1
            ullman_test(używane, macierz_M, aktualny_wiersz+1)
            używane[c] = False

def test():
    rows = 2
    columns = 3
    used_colls = [False for x in range(columns)]
    short_matrix = np.zeros((rows, columns))
    ullman_test(used_colls, short_matrix)

test()
