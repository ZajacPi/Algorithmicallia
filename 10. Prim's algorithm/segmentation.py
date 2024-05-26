from prim import List_Graph, MST
import cv2
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
        graph.insert_edge(key, left)
        graph.insert_edge(key, right)
        graph.insert_edge(key, up)
        graph.insert_edge(key, down)
        graph.insert_edge(key, LD)
        graph.insert_edge(key, RD)
        graph.insert_edge(key, LU)
        graph.insert_edge(key, RU)

# graph.printGraph()
MST(graph, 0)