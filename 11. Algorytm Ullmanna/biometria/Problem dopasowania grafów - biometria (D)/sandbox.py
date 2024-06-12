import numpy as np
import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, key):
        self.key = key

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.key == other.key
        return False

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return str(self.key)

class BiometricGraph:
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
        if vertex in self.graph:
            del self.graph[vertex]
        for v in self.graph:
            if vertex in self.graph[v]:
                del self.graph[v][vertex]

    def neighbours(self, vertex):
        return self.graph[vertex].items()

    def get_vertex(self, key):
        for v in self.graph:
            if v.key == key:
                return v
        return None

    def plot_graph(self, v_color='blue', e_color='red'):
        for v in self.graph:
            y, x = v.key
            plt.scatter(x, y, c=v_color)
            for n in self.graph[v]:
                yn, xn = n.key
                plt.plot([x, xn], [y, yn], color=e_color)
        plt.gca().invert_yaxis()
        plt.show()

    def fill_biometric_graph_from_image(self, image):
        height, width = image.shape
        for y in range(height):
            for x in range(width):
                if image[y, x] == 255:  # White pixel
                    v = Vertex((y, x))
                    self.insert_vertex(v)
                    # Check 8-connected neighborhood
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < height and 0 <= nx < width and image[ny, nx] == 255:
                                nv = Vertex((ny, nx))
                                self.insert_edge(v, nv)

    def unclutter_biometric_graph(self):
        to_remove = set()
        new_edges = []
        
        for v in list(self.graph.keys()):
            neighbours = list(self.neighbours(v))
            if len(neighbours) != 2:
                continue
            
            path = [v]
            while len(neighbours) == 2:
                to_remove.add(path[-1])
                for n, _ in neighbours:
                    if n not in path:
                        path.append(n)
                        break
                neighbours = list(self.neighbours(path[-1]))
            
            if len(path) > 1:
                new_edges.append((path[0], path[-1]))
                new_edges.append((path[-1], path[0]))
        
        for v in to_remove:
            self.delete_vertex(v)
        
        for v1, v2 in new_edges:
            self.insert_edge(v1, v2)

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

    def transform_graph(self, tx, ty, theta):
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        new_graph = BiometricGraph()
        
        for v in self.graph:
            x, y = v.key
            new_x = (x + tx) * cos_theta + (y + ty) * sin_theta
            new_y = -(x + tx) * sin_theta + (y + ty) * cos_theta
            new_v = Vertex((new_x, new_y))
            new_graph.insert_vertex(new_v)
        
        for v1 in self.graph:
            for v2 in self.graph[v1]:
                new_v1 = new_graph.get_vertex((v1.key[0] + tx, v1.key[1] + ty))
                new_v2 = new_graph.get_vertex((v2.key[0] + tx, v2.key[1] + ty))
                new_graph.insert_edge(new_v1, new_v2, self.graph[v1][v2])
        
        return new_graph

def match_graphs(graph1, graph2, Ni=10, epsilon=5):
    edges1 = [(v1, v2, np.linalg.norm(np.array(v1.key) - np.array(v2.key))) for v1 in graph1.graph for v2 in graph1.graph[v1]]
    edges2 = [(v1, v2, np.linalg.norm(np.array(v1.key) - np.array(v2.key))) for v1 in graph2.graph for v2 in graph2.graph[v1]]
    
    pairs = []
    for e1 in edges1:
        for e2 in edges2:
            angle1 = np.arctan2(e1[1].key[1] - e1[0].key[1], e1[1].key[0] - e1[0].key[0])
            angle2 = np.arctan2(e2[1].key[1] - e2[0].key[1], e2[1].key[0] - e2[0].key[0])
            pairs.append((e1, e2, abs(angle1 - angle2)))
    
    pairs = sorted(pairs, key=lambda x: x[2])[:Ni]
    best_match = None
    min_distance = float('inf')
    
    for e1, e2, _ in pairs:
        tx = -e2[0].key[0]
        ty = -e2[0].key[1]
        theta = np.arctan2(e1[1].key[1] - e1[0].key[1], e1[1].key[0] - e1[0].key[0]) - np.arctan2(e2[1].key[1], e2[1].key[0])
        
        transformed_graph = graph2.transform_graph(tx, ty, theta)
        
        matched_vertices = 0
        for v1 in graph1.graph:
            for v2 in transformed_graph.graph:
                if np.linalg.norm(np.array(v1.key) - np.array(v2.key)) < epsilon:
                    matched_vertices += 1
                    break
        
        distance = 1 - matched_vertices / (len(graph1.graph) + len(transformed_graph.graph))
        if distance < min_distance:
            min_distance = distance
            best_match = (graph1, transformed_graph)
    
    return best_match

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