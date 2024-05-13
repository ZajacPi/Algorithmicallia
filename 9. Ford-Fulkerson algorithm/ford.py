#NIESKOŃCZONE
import numpy as np
class Edge:
    def __init__(self, capacity_, residual_):
        # waga krawędzi
        self.capacity = capacity_
        #czy krawędź jest rzezcywista czy resztowa
        self.isResidual = residual_
        if residual_ == True:
            # aktualny rzeczywisty przepływ
            self.flow = 0
            # przepływ resztowy
            self.residual = 0
        else:
             # aktualny rzeczywisty przepływ 
            self.flow = 0
            # przepływ resztowy
            self.residual = capacity_

    def __repr__(self):
        return f"{self.capacity} {self.flow} {self.residual} {self.isResidual}"

#kod z poprzednich ćwiczeń tworzący graf używając słowników        
class Vertex:
    def __init__(self, key):
        self.key = key
    def __eq__(self, other):
        # porównuje węzły wg klucza - czyli wybranego pola identyfikującego węzeł, sprawdzam czy neighbour jest Vertex
        if isinstance(other, Vertex):
            return self.key == other.key
        return False
    
    def __hash__(self):
        #wykorzystywaną przez słownik, zwracająca klucz.
        return hash(self.key)
    
    def __str__(self):
        # ma zwracać klucz (literę reprezentującą województwo)
        return str(self.key)
    
class List_Graph:
    def __init__(self):
        self.graph = {} 
 
    #dodanie nowego węxłu to po prostu stworzenie nowego słownika sąsiadów w grafie. Sprawdzam czy był już wstawiony
    def insert_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = {}


    def insert_edge(self, vertex1, vertex2, edge=None):
        #wstawia do słownika konkretnej krawędzi sąsiada i krawędź pomiędzy nimi, dzisiaj są to po prostu None
        #zakładam że oba już istnieją? Tu jest problem bo może się okazać że daję sąsiada którego jeszcze nie stwozyłem
        if vertex1 not in self.graph:
            self.insert_vertex(vertex1)
        if vertex2 not in self.graph:
            self.insert_vertex(vertex2)

        self.graph[vertex1][vertex2] = edge
        #wstawaim wirtualne krawędzie resztowe na potrzebę obliczeń
        self.graph[vertex2][vertex1] = Edge(edge.capacity, True)

    def delete_vertex(self, vertex):
        #tworzę listę sąsiadów do wyeliminowania
        neighbours = self.neighbours(vertex)
        #trzeba usunąć z listy sąsiadów dla węzłów których jest sąsiadem, nie iteruję całego słownika bo przecież wiem z czym jest połączone
        for neighbour in neighbours:
            del self.graph[neighbour[0]][vertex]
        #usuwam z listy węzłów
        del self.graph[vertex]

    def delete_edge(self, vertex1, vertex2):
        del self.graph[vertex1][vertex2]
        del self.graph[vertex2][vertex1]

    def neighbours(self, vertex_id):
        #dla węzłów przyległych do węzła identyfikowanego przez vertex_id generuje listę par (vertex_id, edge)
        return list(self.graph[vertex_id].items())
    
    def vertices(self):
        # generuje listę węzłów grafu (a w zasadzie ich id)
        return list(self.graph.keys())
    
    def get_vertex(self, vertex_id):
        #dla macierzy sąsiedztwa zwraca węzeł o indeksie vertex_id, dla listy sąsiedztwa zwraca po prostu vertex_id
        for node in self.graph:
            if node.key == str(vertex_id):
                return node
    
    def is_empty(self):
        if not self.graph():
            return True
        else:
            return False
    
    # funkcja pomocnicza do wyświetlania w konsoli aktualnego wyglądu grafu, przerobić na print graph
    def display(self):
        print("Graph:")
        for vertex in self.graph.items():
            print(f"{vertex}\n")
            # print(", ".join(edges))
    def printGraph():
        pass

    # z tego wszystkiego bym jedną funkcję zrbił
    #szukanie trasy (find augmented path)
    def BFS(self):
        visited = []
        parent = {}
        queue = []
        node = next(iter(self.graph.keys()))
        queue.append(node)
        visited.append(node)

        while len(queue) != 0:
            node = queue.pop(0)
            neighbours = self.neighbours(node)
            for i, j in neighbours:
                #to jest działające bst ale trzeba jeszcze sprawdzać czy przepływ resztowy < 0 
                # if i not in visited:
                #     visited.append(i)
                # queue.append(i)
            # return visited
                if i not in visited and self.graph[node][i].residual>0:
                    visited.append(i)
                    parent[node] = i
                    queue.append(i)
        return parent

    #bottleneck calculation
    def min_capacity(self, parent_dict):
        #zmiennne przechowujące ustawiam na ostatni element i jakąć dużą liczbę
        keys =  self.vertices()
        current = keys[-1]
        min_flow = np.cfloat('Inf')
        #jeśli ostatni nie ma rodzica to zwracamy zero, jak sprawdzić czy ostatni element ma rodzica?
        #Iteruję po elementach aż znajdę ten którego szukam i zwracam odpowiadający mu klucz, jak nie znajdzie to zostanie None
        parent = None
        for key, value in parent_dict.items():
            if value == current:
                parent = key
                break
        if parent == None:
            return 0
        
        while current != keys[0]:
            for key, value in parent_dict.items():
                if value == current:
                    #czy aktualny resztowy przepływ jest mniejszy od najmniejszego?
                    current_residual = self.graph[key][current].residual
                    if  current_residual < min_flow:
                        min_flow = current_residual
                    current = key
        return min_flow
    

    def augumentation(self, parent_dict, min_flow):
        keys =  self.vertices()
        current = keys[-1]
        while current != keys[0]:
            for key, value in parent_dict.items():
                if value == current:
                    current_edge = self.graph[key][current]
                    if not current_edge.isResidual:
                        current_edge.flow += min_flow
                        current_edge.residual -= min_flow
                        #w krawędzu porzeciwnej przepływ resztowy zwiększamy o tyle samo
                        opposite_edge = self.graph[current][key] 
                        opposite_edge.residual += min_flow

                    else:
                        current_edge.residual -= min_flow
                        #w krawędzu porzeciwnej przepływ resztowy zwiększamy o tyle samo
                        opposite_edge = self.graph[current][key] 
                        opposite_edge.flow -= min_flow
                        opposite_edge.residual += min_flow
                    current = key
    def Ford_Fukelson(self):
        # Zaczynamy od przeszukania BFS grafu, sprawdzenia, czy istnieje ścieżka od wierzchołka początkowego do końcowego,
        # oraz obliczenia dla niej minimalnego przepływu. Potem w pętli while, jeśli minimalny przepływ > 0, 
        # będą się wykonywać następujące kroki:augmentacja ścieżki,BFS,obliczanie nowej wartości minimalnego przepływu.
        # Na koniec należy zwrócić sumę przepływów przez krawędzie wchodzące do wierzchołka końcowego.
        parents = self.BFS()
        min_flow = self.min_capacity(parents)
        flows = 0
        if min_flow == 0:
            # brak przepływu do ostatniego elementu
            return None
        while min_flow > 0:
            self.augumentation(parents, min_flow)
            parents = self.BFS()
            min_flow = self.min_capacity(parents)   
        #trzeba zwrócić sumę przepływów wpływających do ostatniego węzła
        keys =  self.vertices()
        last_vertex = keys[-1]
    
        for key, neighbours in self.graph.items():
            if last_vertex in neighbours.keys():
                flows += neighbours[key][last_vertex].flow

        return flows

        

def test(graph):
        test_graph = List_Graph()
        for v1, v2, capacity in graph:
            test_graph.insert_edge(v1,v2, Edge(capacity, False))
    
        test_graph.display()
        parents = test_graph.BFS()
        print(parents)
        min_flow = test_graph.min_capacity(parents)
        print(min_flow)

        test_graph.augumentation(parents, min_flow)
        test_graph.display()

def test2(graph):
    test_graph = List_Graph()
    for v1, v2, capacity in graph:
        test_graph.insert_edge(v1,v2, Edge(capacity, False))
    test_graph.display()

    print(test_graph.Ford_Fukelson)
    
def main():
    graf_0 = [ ('s','u',2), ('u','t',1), ('u','v',3), ('s','v',1), ('v','t',2)]
    # Wynik 3
    # test(graf_0)
    test2(graf_0)


    graf_1 = [ ('s', 'a', 16), ('s', 'c', 13), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9), ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4) ]
    # UWAGA: nie uwzględniamy widocznej na rysunku krawędzi ('a', 'c', 10), zakładamy, ze jej nie ma.
    # # Wynik 23

    graf_2 = [ ('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6), ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    # Wynik 5
main()