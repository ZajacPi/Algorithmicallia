import polska
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
    def __init__(self, initial_matrix_value = 0):
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
    
    # funkcja pomocnicza do wyświetlania w konsoli aktualnego wyglądu grafu
    def display(self):
        print("Graph:")
        for vertex in self.graph.items():
            print(f"{vertex}\n")
            # print(", ".join(edges))
        

    
class Matrix_graph:
    def __init__(self, initial_matrix_value = 0):
        self.graph = [[]]
        self.initial = initial_matrix_value
        self.vert = []
 
    def insert_vertex(self, vertex):
        if vertex not in self.vert:
            #dodaję do listy wierzchołków
            self.vert.append(vertex)

            #do tylu ile jestsąsiadów dodaję na początek puste łaczenie
            for i in self.graph:
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
    
        #w obydwu miejscach macierzy zaznaczam łączenie
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
        #zmieniam na domyślną wartość
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
        #dla macierzy sąsiedztwa zwraca węzeł o indeksie vertex_id
          for node in self.vert:
            if node.key == str(vertex_id):
                return node
    
    def is_empty(self):
      return len(self.vert)==0
        
    
def help_test():
    # print(polska.slownik)
    test = List_Graph()
    for vertex, neighbour in polska.graf:
        if vertex not in test.graph:
            test.insert_vertex(vertex)
        test.insert_edge(vertex, neighbour, None)
    test.delete_edge('Z', 'P')
    test.delete_vertex('Z')
    test.display()

def test2():
    data = polska.graf

    # wybór pomiędzy rodzajem grafu
    g = List_Graph()
    # g = Matrix_graph()

    for tup in data:
        v1 = Vertex(tup[0])
        v2 = Vertex(tup[1])
        g.insert_edge(v1,v2)

    mazowieckie = g.get_vertex('K')
    g.delete_vertex(mazowieckie) 
    g.delete_edge(g.get_vertex('W'), g.get_vertex('E'))
    polska.draw_map(g)
    
# help_test()
test2()