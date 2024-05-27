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

    # def neighbours(self, vertex_id):
    #     idx = 0
    #     while self.vert != vertex_id: 
    #         idx += 1        
    #     result = []
    #     for i, val in enumerate(self.graph[idx]):
    #         if val != self.initial:
    #             result.append((self.vert[i], val))
    #     return result 

    # def neighbours(self, vertex):
    #     if chr(vertex+64) in self.vert:
    #         idx = self.vert.index(vertex)
    #         result = []
    #         for i, val in enumerate(self.graph[idx]):
    #             if val != self.initial:
    #                 result.append((self.vert[i], val))
    #         return result
    #     return []
    def neighbours(self, index):
        result = []
        for i in range(len(self.graph[index])):
            if self.graph[index][i] != self.initial:
                result.append(i)

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
    
    def __eq__(self, other):
        return 
    
    def printGraph(self):
        print("Vertices:", [str(v) for v in self.vert])
        print("Adjacency Matrix:")
        for row in self.graph:
            print(" ".join(map(str, row)))