from Matrix_graph import Matrix_graph, Vertex
import numpy as np
import copy

graph_G = [ ('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
graph_P = [ ('A','B',1), ('B','C',1), ('A','C',1)]

# tworzę macierz Mo dzięki której szybciej będę eliminował te wersje gdzie izomorfizm jest niemożliwy
def create_M0(P, G):
    M0 = np.zeros((len(P), len(G)))
    for i in range(len(P)):
        for j in range(len(G)):
            if degree(P, i) <= degree(G, j):
                M0[i][j] = 1
    return M0
#stopień wierzchołka, czyli ile ma krawędzi - czyli ilość jedynek w wierszu, bo wszystkie mają wagę 1, ale mogę
# zrobić lepszą wersję gdzie sprawdzam ilość niezewrowych elementów - wtedy jest bardziej uniwersalne
# def degree(matrix, vertex):
#     return sum(matrix[vertex])
def degree(matrix, vertex):
    return np.count_nonzero(matrix[vertex])


def ullmann_V3(używane, G, P, M, aktualny_wiersz=0, izomorfizmy = None, calls = 1):
    if izomorfizmy is None:
        izomorfizmy = []
    liczba_wierszy = len(M)

    #sprawdzam izomorfizm
    if aktualny_wiersz == liczba_wierszy:
        MG = np.dot(M, G.graph)
        check = np.dot(M, np.transpose(MG))
        if np.array_equal(check, P.graph):
            izomorfizmy.append(np.copy(M))
        return izomorfizmy, calls

    # tworzę kopię macierzy M i to na niej działam
    Mo = np.copy(M)
    Mo = prune(G, P, Mo)
    for c in range(len(M[0])):
        if używane[c] == False and M[aktualny_wiersz][c] != 0:
            używane[c] = True

            for i in range(len(Mo[0])):
                Mo[aktualny_wiersz][i] = 0
            Mo[aktualny_wiersz][c] = 1

            izomorfizmy, calls = ullmann_V3(używane, G, P, Mo, aktualny_wiersz+1, izomorfizmy, calls + 1)
   
            używane[c] = False

    return izomorfizmy, calls


def prune(G, P, M):
    # Mc = copy.deepcopy(M)
    changed = True

    while changed == True:
        changed = False
        for i in range(len(M)):
            for j in range(len(M[0])):
                if M[i][j] == 1:
                    valid = False
                    P_neighbours = P.neighbours(i)
                    G_neighbours = G.neighbours(j)

                    for x in P_neighbours:
                        for y in G_neighbours:
                            if M[x][y] == 1:
                                #jeśli istnieje taki sąsiad y wierzchołka j grafu żę M[x][y] == 1 to przerywam 
                                valid = True
                                break
                        if valid:
                            break
                    #jeżeli valid będzie na False to znaczy że nie isntnieje taki sąsiad
                    if valid == False:
                        M[i][j] = 0
                        changed = True
                        break
        # M = copy.deepcopy(Mc)
    
    return M
    

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
    M = create_M0(P.graph, G.graph)
    used_colls = [False for x in range(rows_G)]

    izomorfizmy, calls = ullmann_V3(used_colls, G, P, M)

    print(f"liczba wywołań: {calls}")
    print(f"liczba izomorfizmów: {len(izomorfizmy)}")

    for izomorfizm in izomorfizmy:
        print(izomorfizm)
        print("################################")

test_ullman_V3()



    
