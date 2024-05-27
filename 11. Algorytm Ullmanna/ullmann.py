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

def ullmann_V2(używane, G, P, M, aktualny_wiersz=0, izomorfizmy = None, calls = 1):
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

    # tworzę kopię macierzy M i to na niej działam
    Mo = np.copy(M)

    for c in range(len(M[0])):
        if używane[c] == False and M[aktualny_wiersz][c] != 0:
            używane[c] = True

            for i in range(len(Mo[0])):
                Mo[aktualny_wiersz][i] = 0
            Mo[aktualny_wiersz][c] = 1
            izomorfizmy, calls = ullmann_V2(używane, G, P, Mo, aktualny_wiersz+1, izomorfizmy, calls)
            calls += 1
            używane[c] = False

    return izomorfizmy, calls


def ullmann_V3(używane, G, P, M, aktualny_wiersz=0, izomorfizmy = None, calls = 1):
    if izomorfizmy is None:
        izomorfizmy = []
    liczba_wierszy = len(M)

    if aktualny_wiersz == liczba_wierszy:
        MG = np.dot(M, G)
        check = np.dot(M, np.transpose(MG))
        if np.array_equal(check, P):
            izomorfizmy.append(np.copy(M))
        return izomorfizmy, calls
    
    M = prune(G, P, M)
    # tworzę kopię macierzy M i to na niej działam
    for c in range(len(M[0])):
        if używane[c] == False and M[aktualny_wiersz][c] != 0:
            używane[c] = True

            M0 = copy.deepcopy(M)
            for i in range(len(M0[0])):
                M0[aktualny_wiersz][i] = 0
            M0[aktualny_wiersz][c] = 1
            izomorfizmy, calls = ullmann_V2(używane, G, P, M0, aktualny_wiersz+1, izomorfizmy, calls)
            calls += 1
            używane[c] = False

    return izomorfizmy, calls

# def prune(G, P, M):
#     Mc = copy.deepcopy(M)
#     while M == Mc:
#         for i in range(len(M)):
#             for j in range(len(M[0])):
#                 if M[i][j] == 1:
#                     for x in P.neighbours(i):
#                         for y in G.neighbours(j):
#                             if Mc[x][y] == 1:
#                                 Mc[i][j] = 0
#     return Mc
def prune(G, P, M):
    Mc = copy.deepcopy(M)
    changed = True

    while changed:
        changed = False
        for i in range(len(M)):
            for j in range(len(M[0])):
                if M[i][j] == 1:
                    # Check neighbors of vertex i in P against neighbors of vertex j in G
                    valid = False
                    for x in P.neighbours(i):
                        for y in G.neighbours(j):
                            if Mc[x[0].id][y[0].id] == 1:
                                valid = True
                                break
                        if valid:
                            break
                    if not valid:
                        Mc[i][j] = 0
                        changed = True
        M = copy.deepcopy(Mc)
    
    return Mc
    

def test1():
    rows = 2
    columns = 3
    used_colls = [False for x in range(columns)]
    short_matrix = np.zeros((rows, columns))
    ullman_test(used_colls, short_matrix)


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

def test_ullman_V2():
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
    izomorfizmy, calls = ullmann_V2(used_colls, G.graph, P.graph, M)
    print(f"liczba wywołań: {calls}")
    for izomorfizm in izomorfizmy:
        print(izomorfizm)
        print("################################")
        
def test_ullman_V3():
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
    izomorfizmy, calls = ullmann_V3(used_colls, G.graph, P.graph, M)
    print(f"liczba wywołań: {calls}")
    for izomorfizm in izomorfizmy:
        print(izomorfizm)
        print("################################")
# test1()
# test_ullmann_V1()
# test_ullman_V2()
test_ullman_V3()
