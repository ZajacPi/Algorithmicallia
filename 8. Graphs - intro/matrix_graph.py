import polska
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
        self.graph = [[]]
        self.initial = initial_matrix_value
        self.vert = []
 
    def insert_vertex(self, vertex):
        if vertex not in self.vert:
            #dodaję do listy wierzchołków
            self.vert.append(vertex)

            for i in self.graph:
                #do tylu ile jestsąsiadów dodaję na początek puste łaczenie
                i.append(self.initial)
            #nowy rząd
            new_row = [self.initial] * len(self.vert)
            self.graph.append(new_row)

#dla macierzy domyślne edge ma być równe 1
    def insert_edge(self, vertex1, vertex2, edge=1):
        if vertex1 not in self.graph:
            self.insert_vertex(vertex1)
        if vertex2 not in self.graph:
            self.insert_vertex(vertex2)
        #muszę sprawdzić gdzie leżą, czyli sprawdzić ich indeksy w liście wierzchołków
        idx1 = 0
        idx2 = 0
        while self.vert[idx1] != vertex1: 
            idx1 += 1
        while self.vert[idx2] != vertex2: 
            idx2 += 1
        # idx1 = self.vert.index(vertex1)
        # idx2 = self.vert.index(vertex2)
        #w dwóch miejscach macierzy zaznaczam
        self.graph[idx1][idx2] = edge
        self.graph[idx2][idx1] = edge

    def delete_vertex(self, vertex):
        del_idx = 0
        #szukam indeksu
        while self.vert[del_idx] != vertex: 
            del_idx += 1
        #usuwam w każdym rzędzie
        for row in self.graph:
            row.pop(del_idx) 
        #usuwam z grafu i z listy wierzchołków
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

    def neighbours(self, vertex_id):
        idx = 0
        while self.vert[idx] != vertex_id: 
            idx += 1        
        result = []
        for i, val in enumerate(self.graph[idx]):
            if val != self.initial:
                result.append((self.vert[i], val))
        return result 
       
    def vertices(self):
        #po prostu lista z konstruktora
        return self.vert
    
    def get_vertex(self, vertex_id):
        #dla macierzy sąsiedztwa zwraca węzeł o indeksie vertex_id, dla listy sąsiedztwa zwraca po prostu vertex_id
        #nad tym sie zastanowić
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
# def test_matrix_graph():
#     # Create some vertices
#     v1 = Vertex("A")
#     v2 = Vertex("B")
#     v3 = Vertex("C")

#     # Create a graph
#     graph = Matrix_graph()

#     # Insert vertices into the graph
#     graph.insert_vertex(v1)
#     graph.insert_vertex(v2)
#     graph.insert_vertex(v3)

#     # Insert edges between vertices
#     graph.insert_edge(v1, v2)
#     graph.insert_edge(v2, v3)

#     # Display the vertices
#     print("Vertices:", [str(v) for v in graph.vert])

#     # Display the adjacency matrix
#     print("Adjacency Matrix:")
#     for row in graph.graph:
#         print(row)

# # Test the Matrix_graph class
# test_matrix_graph()

def test2():
    data = polska.graf
    g = Matrix_graph()

    for tup in data:
        v1 = Vertex(tup[0])
        v2 = Vertex(tup[1])
        g.insert_edge(v1,v2)

    g.delete_vertex(g.get_vertex('K')) 
    g.delete_edge(g.get_vertex('W'), g.get_vertex('E'))
    polska.draw_map(g)
# test()
test2()