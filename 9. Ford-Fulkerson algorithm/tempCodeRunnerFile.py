for neighbour, edge in neighbours:
                if neighbour not in visited and edge.residual > 0:
                    visited.append(neighbour)
                    #tutaj problemy
                    parent[neighbour] = node
                    queue.append(neighbour)