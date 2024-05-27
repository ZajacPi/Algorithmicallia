from Matrix_graph import Matrix_graph, Vertex
import numpy as np
import copy

graph_G = [ ('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
graph_P = [ ('A','B',1), ('B','C',1), ('A','C',1)]

def ullmann_V1(używane, G, P, M, aktualny_wiersz=0, izomorfizmy = None, calls = 1):
    if izomorfizmy is None:
        izomorfizmy = []
    liczba_wierszy = len(M)

    #sprawdzam izomorfizm
    if aktualny_wiersz == liczba_wierszy:
        MG = np.dot(M, G)
        check = np.dot(M, np.transpose(MG))
        if np.array_equal(check, P):
            izomorfizmy.append(np.copy(M))
        return izomorfizmy, calls
    
    for c in range(len(M[0])):
        if używane[c] == False:
            używane[c] = True
            for i in range(len(M[0])):
                M[aktualny_wiersz][i] = 0
            M[aktualny_wiersz][c] = 1
            izomorfizmy, calls = ullmann_V1(używane, G, P, M, aktualny_wiersz+1, izomorfizmy, calls)
            calls += 1
            używane[c] = False

    return izomorfizmy, calls

def test_ullmann_V1():

    G = Matrix_graph()
    sorted_vertices_G = G.sort_vertices(graph_G)
    for v in sorted_vertices_G:
        G.insert_vertex(v)
    for tup in graph_G:
        v1 = Vertex(tup[0])
        v2 = Vertex(tup[1])
        weight = tup[2]
        G.insert_edge(v1, v2, 1)

    P = Matrix_graph()
    sorted_vertices_P = G.sort_vertices(graph_P)
    for v in sorted_vertices_P:
        G.insert_vertex(v)
    for tup in graph_P:
        v1 = Vertex(tup[0])
        v2 = Vertex(tup[1])
        weight = tup[2]
        P.insert_edge(v1, v2, weight)

    # P.printGraph()
    # G.printGraph()
    rows_P = len(P.graph)
    rows_G = len(G.graph)
    M = np.zeros((rows_P, rows_G))
    used_colls = [False for x in range(rows_G)]
    izomorfizmy, calls = ullmann_V1(used_colls, G.graph, P.graph, M)
    print(f"liczba wywołań: {calls}")
    print(f"liczba izomorfizmów: {len(izomorfizmy)}")
    for izomorfizm in izomorfizmy:
        print(izomorfizm)
        print("################################")
        
test_ullmann_V1()