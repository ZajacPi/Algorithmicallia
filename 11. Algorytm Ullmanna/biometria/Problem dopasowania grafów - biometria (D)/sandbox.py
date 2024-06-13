import matplotlib as plt
import cv2
import os
import numpy as np
import copy

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
        
    def get_edges(self):
        edges = []
        for v1 in self.graph:
            for v2 in self.graph[v1]:
                edges.append((v1, v2))
        return edges

    
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

####################################################
def fill_biometric_graph_from_image(I, graph):
    #skanuję wiersz po wierszu i każdy napotkany biały piklsel dodaję do grafu jako0 wierzchołek
    X, Y = I.shape
    for i in range(X):
        for j in range(Y):
            #sprawdzam czy biały
            if I[i, j] == 255:
                v = Vertex((i, j))
                graph.insert_vertex(v)
                #dodatkowo analizuję jego otoczenie, ale od drugiego rzędu i wiersza do przedostatniego wiersza
                if i != 0:
                    for idx in [j-1, j, j+1]:
                        if 0 <= idx < Y and I[i-1, idx] == 255:
                            v2 = graph.get_vertex((i-1, idx))
                            graph.insert_edge(v2, v)
                if j != 0 and I[i, j-1] == 255:
                    v2 = graph.get_vertex((i, j-1))
                    graph.insert_edge(v2, v)

def unclutter_biometric_graph(graph):
    to_delete = []
    to_add = []
    for v in graph.vertices():
        neighbours = graph.neighbours(v)
        # jeżeli podczas iterowania po grafie napotkamy na wierzchołek z dwoma krawędziami, 
        # nic nie robimy - i tak dotrzemy do niego na którymś etapie śledzenia        
        if len(neighbours) == 2:
            continue
        prev = v
        current = neighbours[0][0]
        
        #jeżeli lista sąsiadów równa 2 to nie reprezentuje pkt charakterystycznego
        # przechodzimy przez kolejne wierzchołki, dopóki nie dotrzemy do wierzchołka o liczbie
        # krawędzi różnej od dwóch (kolejnego punktu charakterystycznego) - wówczas kończymy śledzenie, a zbiór krawędzi “do dodania” uzupełniamy o 
        # dwie nowe krawędzie, łączące punkt wyjściowy śledzenia z napotkanym punktem końcowym i vice versa
        while len(graph.neighbours(current)) == 2:
            nodes = graph.neighbours(current)
            to_delete.append(current)
            #zabezpieczenie przed nieskończoną pętlą
            if nodes[0][0] == prev:
                prev, current = current, nodes[1][0]
            else:
                prev, current = current, nodes[0][0]
        to_add.append((v, current))
    #usuwam wierzchołki ze zbioru do usunięcia i dodaje te ze zbiodu do dodania
    for v in to_delete:
        graph.delete_vertex(v)
    for v1, v2 in to_add:
        graph.insert_edge(v1, v2)

def merge_near_vertices(graph, thr):
    vertices = graph.vertices()
    to_merge = set()
    new_vertices = []
    new_edges = []
    #iteruję żeby stworzyć listę list wierzchołków do połączenia
    for i, v1 in enumerate(vertices):
        # jeśli jest połączony to nic nie robię
        if v1 in to_merge:
            continue
        detected = [v1]
        for j in range(i + 1, len(vertices)):
            v2 = vertices[j]
            #jeśli odległość mniejsza niż zakres to dodaję do listy do połączenia
            if np.sqrt((v1.key[0]- v2.key[0])** 2 + (v1.key[1] - v2.key[1])**2) < thr:
                detected.append(v2)
                to_merge.add(v2)
        # po przejściu przez cały graf, rozpoczynamy proces łączenia wykrytych wierzchołków - iterujemy po naszej liście list
        if len(detected) > 1:
            # średnia arytmetyczna współrzędnych wszystkich wierzchołków, żeby znaleść wypośrodkowane
            mid_x = np.mean([v.key[0] for v in detected])
            mid_y = np.mean([v.key[1] for v in detected])
            new_vertex = Vertex((mid_x, mid_y))
            new_vertices.append(new_vertex)
            #iteruję po krawędziach wychodzących z wierzchołków i sprawdzam destynacje
            for v in detected:
                for n, edge in graph.neighbours(v):
                    # odrzucam wszystkie które prowadzą do tych z listy detected, reszte zapamiętuje
                    if n not in detected:
                        new_edges.append((new_vertex, n, edge))
                        new_edges.append((n, new_vertex, edge))
                        
    # usuwam te z listy do połączenia i dołączam nowy znaleziony z destynacjami
    for v in to_merge:
        graph.delete_vertex(v) 
    for v in new_vertices:
        graph.insert_vertex(v)
    for v1, v2, edge in new_edges:
        graph.insert_edge(v1, v2, edge)
        
def rotateGraph(graph, tx, ty, angle):
    #każdy wierzchołek przesuwam wg podanych wzorów
  for v in graph.vertices():
    y, x = v.key
    newX =  (x + tx) * np.cos(angle) + (y + ty) * np.sin(angle)
    newY = -(x + tx) * np.sin(angle) + (y + ty) * np.cos(angle)
    v.key = (newY, newX)
    
def distance_and_angle (v1, v2):
    return np.sqrt((v1.id[0] - v2.key[0]) ** 2 + (v1.key[1] - v2.key[1]) ** 2), np.arctan2((v1.key[0] - v2.key[0]) , (v1.key[1] - v2.key[1]))

def Sab(la, lb, theta_a, theta_b):
    return 2 * np.sqrt((la - lb) ** 2 + (theta_a - theta_b) ** 2) / (la + lb)

def dk(g0, gp0, C):
    return 1 - C / np.sqrt(len(g0.vertices()) * len(gp0.vertices()))

def process_graph_pair(graph1, graph2, e2, eps):
    t2Y, t2X = (-e2[0].key[0], -e2[0].key[1])
    _, theta2 = distance_and_angle(e2[0], e2[1])
    graph2_copy = copy.deepcopy(graph2)
    rotateGraph(graph2_copy, t2X, t2Y, theta2) #obracam
    
    visited = {i: False for i in range(len(graph2.vertices()))}
    C = 0
    for v1 in graph1.vertices():
        for i, v2 in enumerate(graph2_copy.vertices()):
            distance, _ = distance_and_angle(v1, v2)
            #sprawdzam czy sie nadaje porównując do najmniejszego
            if distance < eps and not visited[i]:
                visited[i] = True
                C += 1
                break
    return graph2_copy, C
   
def biometric_graph_registration(graph1, graph2, Ni, eps):
    #sortuję krawędzie i wybieram Ni par z najmniejszą odleglością
    edges1 = [(v1, v2) for v1 in graph1.vertices() for v2 in graph1.neighbours(v1)]
    edges2 = [(v1, v2) for v1 in graph2.vertices() for v2 in graph2.neighbours(v1)]
    distances = []

    for v1, v2 in edges1:
        for ve1, ve2 in edges2:
            l1, theta_a = distance_and_angle(v1, v2)
            l2, theta_b = distance_and_angle(ve1, ve2)
            sab = Sab(l1, l2, theta_a, theta_b)
            distances.append((sab, v1, v2, ve1, ve2))
    distances.sort()
    best_pairs = distances[:Ni]

    min_dk = float('inf')#muszę dać dużą liczbę do porównania na początek
    bestGraphs = None
    #teraz algorytm
    for Sab, e1_v1, e1_v2, e2_v1, e2_v2 in best_pairs:
        graph2_copy, C = process_graph_pair(graph1, graph2, (e2_v1, e2_v2), eps)
        distance = dk(graph1, graph2_copy, C)
        if distance < min_dk:
            min_dk = distance
            bestGraphs = (graph1, graph2_copy)

        graph2_copy, C = process_graph_pair(graph1, graph2, (e2_v2, e2_v1), eps)
        distance = dk(graph1, graph2_copy, C)
        if distance < min_dk:
            min_dk = distance
            bestGraphs = (graph1, graph2_copy)

    return bestGraphs

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