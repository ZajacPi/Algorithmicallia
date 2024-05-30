from prim import List_Graph, Vertex, MST
import cv2
import numpy as np

def traverse_tree(tree, start_node, color, visited, IS):
    stack = [start_node]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            y, x = divmod(node, X)
            IS[y, x] = color
            for neighbor, _ in tree.neighbours(node):
                if neighbor not in visited:
                    stack.append(neighbor)

I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)

graph = List_Graph()
X, Y = I.shape
for i in range(1, X+1):
    for j in range(1, Y+1):
        key = X*j+i
        left = X*(j-1)+i
        right = X*(j+1)+i
        up = X*j+i+1
        down = X*j+i-1
        LD = X*(j+1)+i-1
        RD = X*(j-1)+i+1
        LU = X*(j-1)+i-1
        RU = X*(j+1)+i+1
        graph.insert_edge(Vertex(key), Vertex(left), abs(I[i, j] - I[y, x-1]))
        graph.insert_edge(Vertex(key), Vertex(right))
        graph.insert_edge(Vertex(key), Vertex(up))
        graph.insert_edge(Vertex(key), Vertex(down))
        graph.insert_edge(Vertex(key), Vertex(LD))
        graph.insert_edge(Vertex(key), Vertex(RD))
        graph.insert_edge(Vertex(key), Vertex(LU))
        graph.insert_edge(Vertex(key), Vertex(RU))

# graph.printGraph()
mst_edges, tree = MST(graph, 0)

#szukam największej krawędzi i ją usuwam
max_edge = max(mst_edges, key=lambda e: e[2])
mst_edges.remove(max_edge)

IS = np.zeros((Y, X), dtype='uint8')
visited = set()

traverse_tree(tree, max_edge[0], 100, visited, IS)
traverse_tree(tree, max_edge[1], 200, visited, IS)

# Display the result
cv2.imshow("Wynik", IS)
cv2.waitKey()