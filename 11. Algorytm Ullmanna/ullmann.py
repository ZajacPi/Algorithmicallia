import numpy as np
import copy

graph_G = [ ('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
graph_P = [ ('A','B',1), ('B','C',1), ('A','C',1)]

class Vertex:
  def __init__(self, id):
    self.id = id
    
  def __eq__(self, other : "Vertex"):
    return isinstance(other, Vertex) and self.id == other.id
  
  def __hash__(self):
    return hash(self.id)
  
  def __str__(self):
    return f'{self.id}'
  

class Matrix_graph:
    def __init__(self, initial_matrix_value = 0):
        self.graph = []
        self.initial = initial_matrix_value
        self.vert = []

    def sort_vertices(self, edges):
        vertices = set()
        for edge in edges:
            vertices.add(edge[0])
            vertices.add(edge[1])
        sorted_vertices = sorted(list(vertices))
        return [Vertex(v) for v in sorted_vertices]
 
    def insert_vertex(self, vertex):
        if vertex not in self.vert:
            self.vert.append(vertex)

            for i in self.graph:
                i.append(self.initial)
            new_row = [self.initial] * len(self.vert)
            self.graph.append(new_row)

    def insert_edge(self, vertex1, vertex2, edge=1):
        if vertex1 not in self.graph:
            self.insert_vertex(vertex1)
        if vertex2 not in self.graph:
            self.insert_vertex(vertex2)
        idx1 = 0
        idx2 = 0
        while self.vert[idx1] != vertex1: 
            idx1 += 1
        while self.vert[idx2] != vertex2: 
            idx2 += 1
        self.graph[idx1][idx2] = edge
        self.graph[idx2][idx1] = edge

    def delete_vertex(self, vertex):
        del_idx = 0
        while self.vert[del_idx] != vertex: 
            del_idx += 1
        for row in self.graph:
            row.pop(del_idx) 
        self.graph.pop(del_idx)
        self.vert.pop(del_idx)

    def delete_edge(self, vertex1, vertex2):
        idx1 = 0
        idx2 = 0
        while self.vert[idx1] != vertex1: 
            idx1 += 1
        while self.vert[idx2] != vertex2: 
            idx2 += 1
        self.graph[idx1][idx2] = self.initial
        self.graph[idx2][idx1] = self.initial

    def neighbours(self, index):
        result = []
        for i in range(len(self.graph[index])):
            if self.graph[index][i] != self.initial:
                result.append(i)

        return result
    
    def vertices(self):
        return self.vert
    
    def get_vertex(self, vertex_id):
          for node in self.vert:
            if node.id == str(vertex_id):
                return node
    
    def is_empty(self):
      return len(self.vert)==0
        
    def __getVertexID(self, vertex):
        return self.vertices_.index(vertex)
  
    def edges(self):
        edges = set()
        for i, row in enumerate(self.matrix):
            for j, val in enumerate(row):
                if val != self.empty:
                    if self.vertices_[i] < self.vertices_[j]:
                        edges.add((str(self.vertices_[i]), str(self.vertices_[j])))
                else:
                    edges.add((str(self.vertices_[j]), str(self.vertices_[i])))
        return edges
    
    def __iter__(self):
        return iter(self.edges())
    
    def __eq__(self, other):
        return 
    
    def printGraph(self):
        print("Vertices:", [str(v) for v in self.vert])
        print("Adjacency Matrix:")
        for row in self.graph:
            print(" ".join(map(str, row)))
#################################################################################

def ullman_test(used, M, current_row=0):
    num_of_rows = len(M)
    if current_row == num_of_rows:
        print("#############################")
        print(M)
        return
    for c in range(len(M[0])):
        if used[c] == False:
            used[c] = True
            for i in range(len(M[0])):
                M[current_row][i] = 0
            M[current_row][c] = 1
            ullman_test(used, M, current_row+1)
            used[c] = False

def ullmann_V1(used, G, P, M, current_row=0, izomorfizms = None, calls = 1):
    if izomorfizms is None:
        izomorfizms = []
    num_of_rows = len(M)

    #sprawdzam izomorfizm
    if current_row == num_of_rows:
        MG = np.dot(M, G)
        check = np.dot(M, np.transpose(MG))
        if np.array_equal(check, P):
            izomorfizms.append(np.copy(M))
        return izomorfizms, calls
    
    for c in range(len(M[0])):
        if used[c] == False:
            used[c] = True
            for i in range(len(M[0])):
                M[current_row][i] = 0
            M[current_row][c] = 1
            izomorfizms, calls = ullmann_V1(used, G, P, M, current_row+1, izomorfizms, calls)
            calls += 1
            used[c] = False

    return izomorfizms, calls

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


def ullmann_V2(used, G, P, M, current_row=0, izomorfizms = None, calls = 1):
    if izomorfizms is None:
        izomorfizms = []
    num_of_rows = len(M)

    #sprawdzam izomorfizm
    if current_row == num_of_rows:
        MG = np.dot(M, G)
        check = np.dot(M, np.transpose(MG))
        if np.array_equal(check, P):
            izomorfizms.append(np.copy(M))
        return izomorfizms, calls

    # tworzę kopię macierzy M i to na niej działam
    Mo = np.copy(M)

    for c in range(len(M[0])):
        if used[c] == False and M[current_row][c] != 0:
            used[c] = True

            for i in range(len(Mo[0])):
                Mo[current_row][i] = 0
            Mo[current_row][c] = 1

            izomorfizms, calls = ullmann_V2(used, G, P, Mo, current_row+1, izomorfizms, calls + 1)
   
            used[c] = False

    return izomorfizms, calls


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
                    #pobieram sąsiadów (neighbours zwraca listę indeksów na jakich jest sąsiad)
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
    

def test():
    rows = 2
    columns = 3
    used_colls = [False for x in range(columns)]
    short_matrix = np.zeros((rows, columns))
    ullman_test(used_colls, short_matrix)


def test_ullmann_V1(P, G):
    rows_P = len(P.graph)
    rows_G = len(G.graph)

    M = np.zeros((rows_P, rows_G))
    used_colls = [False for x in range(rows_G)]

    izomorfizmy, calls = ullmann_V1(used_colls, G.graph, P.graph, M)

    print(f"{len(izomorfizmy)} {calls}")

    # print(f"liczba wywołań: {calls}")
    # print(f"liczba izomorfizmów: {len(izomorfizmy)}")
    # for izomorfizm in izomorfizmy:
    #     print(izomorfizm)
    #     print("################################")


def test_ullmann_V2(P, G):
    rows_P = len(P.graph)
    rows_G = len(G.graph)

    # wrzucam macierze sąsiedztwa
    M = create_M0(P.graph, G.graph)
    used_colls = [False for x in range(rows_G)]
    izomorfizmy, calls = ullmann_V2(used_colls, G.graph, P.graph, M)
    
    print(f"{len(izomorfizmy)} {calls}")

    # print(f"liczba wywołań: {calls}")
    # for izomorfizm in izomorfizmy:
    #     print(izomorfizm)
    #     print("################################")
        

def test_ullmann_V3(P, G):
    rows_G = len(G.graph)
    M = create_M0(P.graph, G.graph)
    used_colls = [False for x in range(rows_G)]
    izomorfizmy, calls = ullmann_V3(used_colls, G, P, M)

    print(f"{len(izomorfizmy)} {calls}")

    # print(f"liczba wywołań: {calls}")
    # for izomorfizm in izomorfizmy:
    #     print(izomorfizm)
    #     print("################################")


def main():
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
    

    test_ullmann_V1(P, G)
    test_ullmann_V2(P, G)
    test_ullmann_V3(P, G)

main()