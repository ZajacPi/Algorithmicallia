import cv2
import numpy as np
from prim import List_Graph, MST

# Read the image in grayscale
I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)
X, Y = I.shape

# Create the graph
graph = List_Graph()

# Add edges with weights as the difference in pixel values
for j in range(Y):
    for i in range(X):
        key = X * j + i
        neighbors = [
            (X * (j - 1) + (i - 1), I[j - 1, i - 1]) if j > 0 and i > 0 else None,  # LU
            (X * (j - 1) + i, I[j - 1, i]) if j > 0 else None,                     # UP
            (X * (j - 1) + (i + 1), I[j - 1, i + 1]) if j > 0 and i < X - 1 else None,  # RU
            (X * j + (i - 1), I[j, i - 1]) if i > 0 else None,                     # LEFT
            (X * j + (i + 1), I[j, i + 1]) if i < X - 1 else None,                 # RIGHT
            (X * (j + 1) + (i - 1), I[j + 1, i - 1]) if j < Y - 1 and i > 0 else None,  # LD
            (X * (j + 1) + i, I[j + 1, i]) if j < Y - 1 else None,                 # DOWN
            (X * (j + 1) + (i + 1), I[j + 1, i + 1]) if j < Y - 1 and i < X - 1 else None  # RD
        ]
        for neighbor in neighbors:
            if neighbor:
                n_key, value = neighbor
                weight = abs(I[j, i] - value)
                graph.insert_edge(key, n_key, weight)

# Compute the MST
mst_edges, mst_tree = MST(graph, 0)

# Find the edge with the maximum weight
max_edge = max(mst_edges, key=lambda e: e[2])
mst_edges.remove(max_edge)

# Create an empty image for visualization
IS = np.zeros((Y, X), dtype='uint8')

def traverse_tree(tree, start_node, color, visited, IS):
    stack = [start_node]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            y, x = divmod(node, X)
            IS[y, x] = color
            for neighbor in tree.neighbours(node):
                if neighbor not in visited:
                    stack.append(neighbor)

# Use the two nodes connected by the removed edge as starting points
visited = set()
traverse_tree(mst_tree, max_edge[0], 100, visited, IS)
traverse_tree(mst_tree, max_edge[1], 200, visited, IS)

# Display the result
cv2.imshow("Wynik", IS)
cv2.waitKey()
