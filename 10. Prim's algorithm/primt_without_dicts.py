#nieskończone
from graf_mst import graf
class Vertex:
    def __init__(self, key, color_=None):
        self.key = key
        #dodaję kolor wierzchoła
        self.color = color_
        self.intree = 0
        self.distance = float('inf')
        self.parent = None

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.key == other.key
        return False
    
    def __hash__(self):
        return hash(self.key)
    
    def __str__(self):
        return str(self.key)

class List_Graph:
    def __init__(self):
        self.graph = {} 
        # trzy dodatkowe słowniki indeksowane wierzchołkiem: intree - czy wierzchołek jest w drzewie, distance - minimalna waga krawędzi
        # dla danego wierzchołka, parent - “rodzic”/poprzedni wierzchołek w drzewie (do opisu krawędzi). Rozmiar tych tablic to liczba 
        # wierzchołków, a ich początkowe wartości to - intree:  0, distance: duża liczba (np. float('inf')), parent: None.  
        # self.intree = {}
        # self.distance = {}
        # self.parent = {}

    def insert_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = {}


    def insert_edge(self, vertex1, vertex2, edge=None):
        if vertex1 not in self.graph:
            self.insert_vertex(vertex1)
        if vertex2 not in self.graph:
            self.insert_vertex(vertex2)

        self.graph[vertex1][vertex2] = edge

    def delete_vertex(self, vertex):
        neighbours = self.neighbours(vertex)
        for neighbour in neighbours:
            del self.graph[neighbour[0]][vertex]
        del self.graph[vertex]

    def delete_edge(self, vertex1, vertex2):
        del self.graph[vertex1][vertex2]
        del self.graph[vertex2][vertex1]

    def neighbours(self, vertex_id):
        return list(self.graph[vertex_id].items())
    
    def vertices(self):
        return list(self.graph.keys())
    
    def get_vertex(self, vertex_id):
        for node in self.graph:
            if node.key == str(vertex_id):
                return node
    
    def is_empty(self):
        if not self.graph():
            return True
        else:
            return False
    
    def display(self):
        print("Graph:")
        for vertex in self.graph.items():
            print(f"{vertex}\n")
            # print(", ".join(edges))
##############################################################
    def printGraph(g):
        print("------GRAPH------")
        for v in g.vertices():
            print(v, end = " -> ")
            for (n, w) in g.neighbours(v):
                print(n, w, end=";")
            print()
        print("-------------------")
    
        
def MST(graph, first):
    tree = List_Graph()
    v = graph.get_vertex(first)
    #pierwszy vertex nie ma rodzica i nie będzie miał distance
    v.distance = 0
    while v != None and v.intree == 0:
        tree.insert_vertex(v)
        v.intree = 1
        # przeglądamy sąsiadów aktualnie rozważanego wierzchołka:
        #sprawdzamy, czy waga krawędzi jest mniejsza od tej zapisanej w distance oraz czy wierzchołek nie jest już w drzewie,
        # jeśli warunek jest spełniony, to uaktualniamy  distance dla sąsiada oraz zapamiętujemy parent sąsiada na rozważany wierzchołek,
        # if v not in tree and edge.weight < tree_weight[edge]:
        #     parent[v]
        for neighbour, weight in graph.neighbours(v):
            if neighbour.intree == 0 and weight < neighbour.distance:
                neighbour.distance = weight
                neighbour.parent = v
                # v.distance = weight
                # neighbour.parent = v

        #szukam kolejnego wierzchołka który dodam do drzewa
        # musimy wykonać przegląd po wszystkich wierzchołkach (technicznie po tych, które nie są w drzewie),
        min_distance = float('Inf')
        next_vertex = None

        for v in graph.vertices():
            if v.intree == 0 and v.distance < float('Inf'):
                # for neighbour, weight in graph.neighbours(v):
                    # if neighbour.distance < min_distance:
                    if v.distance < min_distance:
                        min_distance = v.distance
                        next_vertex = v
        
        if next_vertex != None:
            tree.insert_edge(next_vertex.parent, next_vertex, min_distance)
            tree.insert_edge(next_vertex, next_vertex.parent, min_distance)

        v = next_vertex

    tree.printGraph()
def test():
    test_graph = List_Graph()

    for tup in graf:
        v1 = Vertex(tup[0])
        v2 = Vertex(tup[1])
        test_graph.insert_edge(v1,v2, tup[2])
        test_graph.insert_edge(v2, v1, tup[2])
    test_graph.printGraph()
    MST(test_graph, 'A')
    
test()