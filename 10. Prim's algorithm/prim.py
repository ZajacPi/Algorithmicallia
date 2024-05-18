from graf_mst import graf
class Vertex:
    def __init__(self, key, color_=None):
        self.key = key
        #dodaję kolor wierzchoła
        self.color = color_
    

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
        print("------GRAPH------")
        for v in self.vertices():
            print(v, end = " -> ")
            for (n, w) in self.neighbours(v):
                print(n, w, end=";")
            print()
        print("-------------------")

# Prim's algorithm
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

    intree = {}
    parent = {}
    distance = {}
    #wszystkie wierzchołki nie są w drzewie więc mają 0, nie mają rodziców więc mają dla parent None, a odległość ustawiam na 
    # nieskończoność 
    for vertex in graph.vertices():
        intree[vertex] = 0
        parent[vertex] = None
        distance[vertex] = float('Inf')

    while v != None and intree[v] == 0:
        tree.insert_vertex(v)
        intree[v] = 1

        # przeglądamy sąsiadów aktualnie rozważanego wierzchołka:
        #sprawdzamy, czy waga krawędzi jest mniejsza od tej zapisanej w distance oraz czy wierzchołek nie jest już w drzewie,
        # jeśli warunek jest spełniony, to uaktualniamy  distance dla sąsiada oraz zapamiętujemy parent sąsiada na rozważany wierzchołek,
    
        for neighbour, weight in graph.neighbours(v):
            if intree[neighbour] == 0 and weight < distance[neighbour]:
                distance[neighbour] = weight
                parent[neighbour] = v

        #szukam kolejnego wierzchołka który dodam do drzew
        # musimy wykonać przegląd po wszystkich wierzchołkach (technicznie po tych, które nie są w drzewie),
        min_distance = float('Inf')
        next_vertex = None

        for v in graph.vertices():
            #jeśli odległość mniejsza od nieskończoności to znaczy że ją zmieniałem, czyli jest to wierzchołek połączony krawędzią z grafem
            if intree[v] == 0 and distance[v] < float('Inf'):
                    # aktulizuję najkrótsze połączenie
                    if distance[v] < min_distance:
                        min_distance = distance[v]
                        next_vertex = v
        
        #dodaję krawędź
        if next_vertex != None:
            tree.insert_edge(parent[next_vertex], next_vertex, min_distance)
            tree.insert_edge(next_vertex, parent[next_vertex], min_distance)

        v = next_vertex
    tree.printGraph()

def test():
    test_graph = List_Graph()

    for tup in graf:
        v1 = Vertex(tup[0])
        v2 = Vertex(tup[1])
        test_graph.insert_edge(v1,v2, tup[2])
        test_graph.insert_edge(v2, v1, tup[2])
    # test_graph.printGraph()

    #wybieram sobie od jakiej litery mam zacząć rysować drzewo
    MST(test_graph, 'A')
    
test()
