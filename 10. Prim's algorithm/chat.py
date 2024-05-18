class Vertex:
    def __init__(self, key):
        self.id = key
        self.neighbours = []  # List of tuples (neighbour, weight)
        self.distance = float('Inf')
        self.parent = None
        self.intree = 0  # Boolean flag to check if the vertex is in the MST

    def __str__(self):
        return str(self.id)
    
class Graph:
    def __init__(self):
        self.vertices_dict = {}

    def add_vertex(self, key):
        new_vertex = Vertex(key)
        self.vertices_dict[key] = new_vertex
        return new_vertex

    def get_vertex(self, key):
        if key in self.vertices_dict:
            return self.vertices_dict[key]
        return None

    def add_edge(self, from_key, to_key, weight):
        if from_key not in self.vertices_dict:
            self.add_vertex(from_key)
        if to_key not in self.vertices_dict:
            self.add_vertex(to_key)
        
        self.vertices_dict[from_key].neighbours.append((self.vertices_dict[to_key], weight))
        self.vertices_dict[to_key].neighbours.append((self.vertices_dict[from_key], weight))

    def vertices(self):
        return self.vertices_dict.values()

    def neighbours(self, vertex):
        return vertex.neighbours

    def printGraph(self):
        for v in self.vertices():
            print(f'Vertex {v.id}:', end='')
            for neighbour, weight in v.neighbours:
                print(f' -> {neighbour.id} (weight {weight})', end='')
            print()


def MST(graph, start_key):
    tree = Graph()
    start_vertex = graph.get_vertex(start_key)
    start_vertex.distance = 0
    
    while True:
        min_distance = float('Inf')
        next_vertex = None
        
        for vertex in graph.vertices():
            if vertex.intree == 0 and vertex.distance < min_distance:
                min_distance = vertex.distance
                next_vertex = vertex
        
        if next_vertex is None:
            break
        
        tree.add_vertex(next_vertex.id)
        next_vertex.intree = 1
        
        if next_vertex.parent is not None:
            tree.add_edge(next_vertex.parent.id, next_vertex.id, next_vertex.distance)
        
        for neighbour, weight in graph.neighbours(next_vertex):
            if neighbour.intree == 0 and weight < neighbour.distance:
                neighbour.distance = weight
                neighbour.parent = next_vertex

        print('Main graph:')
        graph.printGraph()
        print('Tree:')
        tree.printGraph()
    
    return tree
if __name__ == "__main__":
    g = Graph()
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 3)
    g.add_edge('B', 'C', 1)
    g.add_edge('B', 'D', 3)
    g.add_edge('C', 'D', 1)
    g.add_edge('C', 'E', 5)
    g.add_edge('D', 'E', 6)
    
    tree = MST(g, 'A')
    
    print('Final Minimum Spanning Tree:')
    tree.printGraph()