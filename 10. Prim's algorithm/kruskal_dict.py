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
    
    def printGraph(g):
        print("------GRAPH------")
        for v in g.vertices():
            print(v, end = " -> ")
            for (n, w) in g.neighbours(v):
                print(n, w, end=";")
            print()
        print("-------------------")

    #szukanie korzenia
    def find(self, parent, v):
        if parent[v] == v:
            return v
        else:
            return self.find(parent, parent[v])

    # def union_sets(self, parent, s1, s2):
    #     root1 = self.find(s1)   
    #     root2 = self.find(s2)

    #     if parent[s1] == parent[s2]:
    #         pass

    def same_component(self, parent, s1, s2):
        root1 = self.find(parent, s1)
        root2 = self.find(parent, s2)
        return root1 == root2
    
    def union(self, size, parent, u, v):
        root1 = self.find(parent, u)   
        root2 = self.find(parent, v)

        if size[u] >= size[v]:
            parent[v] = u
        else:
            parent[u] = v
        return parent        

    def Kruskal(self):

        parent = {}
        size = {}
        n = 0

        # sorted_dict = {key: self.graph[key] for key in sorted(self.graph)}
        # print(sorted_dict)
                
        # for v in sorted_dict: 
        #     #najpierw każdy wierzchołek jest swoim rodzicem i każde poddrzewo wielkości 1
        #     parent[v] = v
        #     size[v] = 1

        for v in self.vertices(): 
            #najpierw każdy wierzchołek jest swoim rodzicem
            parent[v] = v 
            size[v] = 1 

        # tworzę listę krawędzi i ją segreguję od największej do najmniejszej
        edges = []
        for v in self.vertices():
            for neighbor, weight in self.neighbours(v):
                if (neighbor, v) not in edges and (v, neighbor) not in edges:
                    edges.append((v, neighbor, weight))
        sorted_edges = sorted(edges, key=lambda edge: edge[2])

        # print(edges)
        print(sorted_edges)
        print(parent)
        # print(self.find(parent, 3))

        for edge in sorted_edges:
            if not self.same_component(parent, edge[0], edge[1]):
                parent = self.union(size, parent, edge[1], edge[0])

        print(parent)


def test():
    test_graph = List_Graph()
    # v1 = Vertex(ord('A'))
    # v2 = Vertex(ord('B'))
    # v3 = Vertex(ord('C'))
    # v4 = Vertex(ord('D'))
    # v5 = Vertex(ord('E'))
    v1 = Vertex(1)
    v2 = Vertex(2)
    v3 = Vertex(3)
    v4 = Vertex(4)
    v5 = Vertex(5)
    test_graph.insert_vertex(v3)
    test_graph.insert_edge(v1, v2, 10)
    test_graph.insert_edge(v4, v5, 4)
    test_graph.insert_edge(v3, v4, 6)
    test_graph.printGraph()
    # test_graph.find(ord('B'))
    test_graph.Kruskal()

def main():
    test_graph = List_Graph()

    for tup in graf:
        v1 = Vertex(tup[0])
        v2 = Vertex(tup[1])
        test_graph.insert_edge(v1,v2, tup[2])
        test_graph.insert_edge(v2, v1, tup[2])
    # test_graph.printGraph()

    #wybieram sobie od jakiej litery mam zacząć rysować drzewo
    test_graph.Kruskal()
    
# main()
test()
