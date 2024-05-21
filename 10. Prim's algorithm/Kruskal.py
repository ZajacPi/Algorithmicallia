from graf_mst import graf
from prim import List_Graph, Vertex
class MST:
    def __init__(self, n):
        self.parent = []
        self.size = []
        for i in range(n): 
            #najpierw każdy wierzchołek jest swoim rodzicem
            self.parent.append(i)
            #każdy wierzchołek jest drzewem o wielkości 1
            self.size.append(1)

    #szukanie korzenia
    def find(self, v):
        if self.parent[v] == v:
            return v
        else:
            return self.find(self.parent[v])
        
    # zwaraca true jeśli mają ten sam korzeń
    def same_component(self, s1, s2):
        root1 = self.find(s1)
        root2 = self.find(s2)
        return root1 == root2
    
    def union_sets(self, s1, s2):
        root1 = self.find(s1)   
        root2 = self.find(s2)

        if self.size[root1]> self.size[root2]:
            self.parent[root2] = root1
def test():
    n = 5
    edges = [(1,2),(1,4), (1,5), (4,5)]
    check = [(1,2),(2,3),(4,5), (1,4)]
    vertices = []

    for i in range(n+1):
        vertices.append(i)
    mst_test = MST(n)

    for v1, v2 in edges:
        mst_test.union_sets(v1, v2)
    for v1, v2 in check:
        print(mst_test.same_component(v1,v2))

def Kruskal(edges):
    sorted_edges = sorted(edges, key=lambda edge: (edge[2], edge[0], edge[1]))
    graph = List_Graph()
    for tup in edges:
        v1 = Vertex(tup[0])
        v2 = Vertex(tup[1])
        graph.insert_edge(v1,v2, tup[2])
        graph.insert_edge(v2, v1, tup[2])

    parent = []
    size = []
    n = graph.size()
            
    for i in range(len(sorted_edges)): 
        #najpierw każdy wierzchołek jest swoim rodzicem
        parent.append(i)
        size.append(1)

    print(parent)

    for edge in edges:
        if not same_component(edge[0], edge[1]):
            union_sets(edge[0], edge[1])




def main():
    test_graph = List_Graph()

    for tup in graf:
        v1 = Vertex(tup[0])
        v2 = Vertex(tup[1])
        test_graph.insert_edge(v1,v2, tup[2])
        test_graph.insert_edge(v2, v1, tup[2])
    # test_graph.printGraph()

    #wybieram sobie od jakiej litery mam zacząć rysować drzewo
    MST(test_graph, 'A')
    
# main()
test()
