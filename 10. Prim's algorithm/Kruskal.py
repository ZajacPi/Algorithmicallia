from graf_mst import graf
from prim import List_Graph, Vertex
class MST:
    def __init__(self, n):
        self.parent = []
        self.size = []
        for i in range(n+1): 
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
     
    # dołączam mniejsze poddrzewo do większego 
    def union_sets(self, s1, s2):
        root1 = self.find(s1)   
        root2 = self.find(s2)

        if self.size[root1] >= self.size[root2]:
            self.parent[root2] = root1
            self.size[root1] += self.size[root2]

        else:
            self.parent[root1] = root2
            self.size[root2] += self.size[root1]

def test():
    n = 5
    check = [(1,2),(2,3),(4,5), (1, 3)]
    mst_test = MST(n)
  
    mst_test.union_sets(1, 2)
    mst_test.union_sets(4, 5)
    for v1, v2 in check:
        print(mst_test.same_component(v1,v2))
    mst_test.union_sets(3, 1)
    print(mst_test.same_component(1,3))
    #test passed


def Kruskal(edges):
 

    # sprawdzam ile mam wierzchołków tworząc set które stworzy listę unikalnych wierzchołków
    verteces = set()
    for edge in edges:
        verteces.add(edge[0])
        verteces.add(edge[1])
    n = len(verteces)

    #sortuję krawędzie rosnąco
    sorted_edges = sorted(edges, key=lambda edge: (edge[2], edge[0], edge[1]))
    tree = MST(n)
    mst_edges = []

    for edge in sorted_edges:
        #zmieniam na ascii tak, aby zaczynały się od 0. W ten sposób każda litera alfabetu ma swoje ściśle określone miejsce w liście
        v1 = ord(edge[0])-65
        v2 = ord(edge[1])-65
        if not tree.same_component(v1, v2):
            tree.union_sets(v1, v2)
            mst_edges.append(edge)

    # tworzę graf z utworzonej listy krawędzi
    mst_graph = List_Graph()
    for tup in mst_edges:
        v1 = Vertex(tup[0])
        v2 = Vertex(tup[1])
        mst_graph.insert_edge(v1,v2, tup[2])
        mst_graph.insert_edge(v2, v1, tup[2])

    mst_graph.printGraph()
    return mst_edges

def main():
   print(f"Krawędzie MST: {Kruskal(graf)}")
    
main()
# test()
