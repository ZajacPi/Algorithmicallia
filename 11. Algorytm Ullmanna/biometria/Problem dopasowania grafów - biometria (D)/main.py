import matplotlib as plt
import cv2
import os
import numpy as np

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

class BiometricGraph:
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

def plot_graph(self, v_color, e_color):
      for idx, v in enumerate(self.vertex):
            y, x = v.key
            plt.scatter(x, y, c=v_color)
            for n_idx, _ in self.neighbours(idx):
                yn, xn = self.getVertex(n_idx).key
                plt.plot([x, xn], [y, yn], color=e_color)

def fill_biometric_graph_from_image(I, graph):
    #skanuję wiersz po wierszu i każdy napotkany biały piklsel dodaję do grafu jako0 wierzchołek
    X, Y = I.shape
    for i in range(X):
        for j in range(Y):
            if I[i, j] == 255:
                v = Vertex(i, j)# jak dodać? współrzędne?
                graph.insert(v) 
                #dodatkowo analizuję jego otoczenie, ale od drugiego rzędu i wiersza do przedostatniego wiersza
                if i != 0 and j != 0 and j != Y:
                    up = [j-1, j, j+1]
                    for idx in up:
                        #i-1 bo wierszy wyżej
                        if  I[i-1, idx] == 255:
                            v2 = graph.get_vertex((i-1, idx))
                            graph.insert_edge(v2, v)
                #teraz ten z lewej (jeśli nie jest na krawędzi)
                if i != 0 and I[i, j-1] == 255:
                    v2 = graph.get_vertex(i, j-1)
                    graph.insert_edge(v2, v)


def unclutter_biometric_graph(graph):
    to_delete = []
    for v in graph.vertices:
        neighbours = graph.neighbours(v)
        # jeżeli ich liczba jest różna od dwóch, to jest to jeden ze wspomnianych wcześniej punktów charakterystycznych (koniec, rozgałęzienie, przecięcie) - zostawiamy go w grafie i rozpoczynamy śledzenie wychodzących z niego naczyń krwionośnych
        if len(neighbours) != 2:
            prev = v # poprzedni wierzchołek
            for node, edge in neighbours:
                #jeżeli lista sąsiadów równa 2 o nie reprezentuje pkt charakterystycznego
                while len(graph.neighbours(node)) == 2:
                    nodes = graph.neighbours(node)
                    to_delete.append(node)
                #zabezpieczenie przed nieskończoną pętlą
                if nodes[0][0] == prev:
                    node, prev = nodes[1][0], node
                else:
                    node, prev = nodes[0][0], node


def merge_near_vertices(self, threshold):
    vertices = list(self.graph.keys())
    merged = set()
    new_vertices = []
    new_edges = []

    for i, v1 in enumerate(vertices):
        if v1 in merged:
            continue
        cluster = [v1]
        for j in range(i + 1, len(vertices)):
            v2 = vertices[j]
            if np.linalg.norm(np.array(v1.key) - np.array(v2.key)) < threshold:
                cluster.append(v2)
                merged.add(v2)
        if len(cluster) > 1:
            avg_x = np.mean([v.key[0] for v in cluster])
            avg_y = np.mean([v.key[1] for v in cluster])
            new_vertex = Vertex((avg_x, avg_y))
            new_vertices.append(new_vertex)
            for v in cluster:
                for n, edge in self.neighbours(v):
                    if n not in cluster:
                        new_edges.append((new_vertex, n, edge))
                        new_edges.append((n, new_vertex, edge))
    
    for v in merged:
        self.delete_vertex(v)
    
    for v in new_vertices:
        self.insert_vertex(v)
    
    for v1, v2, edge in new_edges:
        self.insert_edge(v1, v2, edge)
def transform(graph, )
def biometric_graph_registration():
    pass

def main():
    data_path = "./Images"
    img_level = "easy"
    img_list = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]

    input_data = []
    for img_name in img_list:
        if img_name[-3:] == "png":
            if img_name.split('_')[-2] == img_level:
                print("Processing ", img_name, "...")

                img = cv2.imread(os.path.join(data_path, img_name))
                img_1ch = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, img_bin = cv2.threshold(img_1ch, 127, 255, cv2.THRESH_BINARY)
               
                graph = BiometricGraph()
                fill_biometric_graph_from_image(img_bin, graph)                
                unclutter_biometric_graph(graph)    
                merge_near_vertices(graph, thr=5)

                input_data.append((img_name, graph))
                print("Saved!")

    for i in range(len(input_data)):
        for j in range(len(input_data)):
            graph1_input = input_data[i][1]
            graph2_input = input_data[j][1]

            graph1, graph2 = biometric_graph_registration(graph1_input, graph2_input, Ni=50, eps=10)

            plt.figure()
            graph1.plot_graph(v_color='red', e_color='green')

            graph2.plot_graph(v_color='gold', e_color='blue')
            plt.title('Graph comparison')
            plt.show()

if __name__ == "__main__":
    main()