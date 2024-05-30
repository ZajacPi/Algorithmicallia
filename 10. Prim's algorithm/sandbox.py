import cv2
import numpy as np

class Vertex:
    def __init__(self, key, color_=None):
        self.key = key
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
            if node.key == vertex_id:
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

    def printGraph(g):
        print("------GRAPH------")
        for v in g.vertices():
            print(v, end = " -> ")
            for (n, w) in g.neighbours(v):
                print(n, w, end=";")
            print()
        print("-------------------")
    
# algorytm prima
##############################################################      
def MST(graph, first):
    tree = List_Graph()
    mst_edges = [] 
    v = first

    intree = {}
    parent = {}
    distance = {}

    for vertex in graph.vertices():
        intree[vertex] = 0
        parent[vertex] = None
        distance[vertex] = float('Inf')

    while v != None and intree[v] == 0:
        tree.insert_vertex(v)
        intree[v] = 1

        for neighbour, weight in graph.neighbours(v):
            if intree[neighbour] == 0 and weight < distance[neighbour]:
                distance[neighbour] = weight
                parent[neighbour] = v

        min_distance = float('Inf')
        next_vertex = None

        for v in graph.vertices():
            if intree[v] == 0 and distance[v] < float('Inf'):
                    if distance[v] < min_distance:
                        min_distance = distance[v]
                        next_vertex = v
        
        if next_vertex != None:
            tree.insert_edge(parent[next_vertex], next_vertex, min_distance)
            tree.insert_edge(next_vertex, parent[next_vertex], min_distance)
            mst_edges.append((parent[next_vertex], next_vertex, min_distance))

        v = next_vertex
    # tree.printGraph()
    return tree, mst_edges

    

# trawersacja grafu z wykorzystaniem stosu
def traverse(I, graph, start, color):
    stack = [start]
    visited = set()
    Y, X = I.shape

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            # z napotkanych wierzchołków odcczytujemy współrzędne piksela
            x = node % X
            y = node // X
            #wpisuję pod nie kolor
            I[y, x] = color

            for neighbor, _ in graph.neighbours(node):
                if neighbor not in visited:
                    stack.append(neighbor)
    return I


def segmentation(I):

  Y, X = I.shape
  g = List_Graph()
  for y in range(Y):
    for x in range(X):
      xID = X * y + x
      if x > 0:
        # lewy sąsiad
        g.insert_edge(xID, xID - 1, abs(I[y, x] - I[y, x-1]))

      if x < X - 1:
        # prawy sąsiad
        g.insert_edge(xID, xID + 1, abs(I[y, x] - I[y, x+1]))
      
      if y > 0:
        # górny sąsiad
        g.insert_edge(xID, xID - X, abs(I[y, x] - I[y-1, x]))

      if y < Y - 1:
        # dolny sąsiad
        g.insert_edge(xID, xID + X, abs(I[y, x] - I[y+1, x]))

      if x > 0 and y > 0:
        # lewy górny sąsiad
        g.insert_edge(xID, xID - X - 1, abs(I[y, x] - I[y-1, x-1]))

      if x < X - 1 and y > 0:
        # prawy górny sąsiad
        g.insert_edge(xID, xID - X + 1, abs(I[y, x] - I[y-1, x+1]))
      
      if x > 0 and y < Y - 1:
        # lewy dolny sąsiad
        g.insert_edge(xID, xID + X - 1, abs(I[y, x] - I[y+1, x-1]))  
      if x < X - 1 and y < Y - 1:
        # prawy dolny sąsiad
        g.insert_edge(xID, xID + X + 1, abs(I[y, x] - I[y+1, x+1]))
      
        
  # MST zwraca listę mst_edges =[parent, vertex, weight] no i tree czyli graf prima
  tree, mst_edges = MST(g, 0)
  
  # muszę znaleźć największą krawędź i ją usunąć
  max_edge = max(mst_edges, key=lambda e: e[2])

  #usuwam krawędź z grafu wykorzystując metodę klasy
  tree.delete_edge(max_edge[0], max_edge[1])

  #tworzę macierz wynikową
  IS = np.zeros((Y, X), dtype='uint8')
  #trawersuję przez oba drzewa zaczynając od wierzchołków krawędzi którą usunąłem, ustawiam kolor na 100 i 200
  IS = traverse(IS, tree, max_edge[0], 100)
  IS = traverse(IS, tree, max_edge[1], 200)

  cv2.imshow("Wynik",IS)
  cv2.waitKey() 


def main():
  I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE).astype(int)
  segmentation(I)
main()