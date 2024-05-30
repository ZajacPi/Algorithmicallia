  Y, X = I.shape
  g = List_Graph()
  for y in range(Y):
    for x in range(X):
      xID = getID(X, y, x)
      if x > 0:
        weight = abs(I[y, x] - I[y, x-1])
        g.insert_edge(xID, xID - 1, weight)
      if x > 0 and y > 0:
        weight = abs(I[y, x] - I[y-1, x-1])
        g.insert_edge(xID, xID - X - 1, weight)
      if x < X - 1 and y > 0:
        weight = abs(I[y, x] - I[y-1, x+1])
        g.insert_edge(xID, xID - X + 1,weight)
      if x < X - 1:
        weight = abs(I[y, x] - I[y, x+1])
        g.insert_edge(xID, xID + 1,weight)
      if y > 0:
        weight = abs(I[y, x] - I[y-1, x])
        g.insert_edge(xID, xID - X, weight)
      if x > 0 and y < Y - 1:
        weight = abs(I[y, x] - I[y+1, x-1])
        g.insert_edge(xID, xID + X - 1, weight)  
      if x < X - 1 and y < Y - 1:
        weight = abs(I[y, x] - I[y+1, x+1])
        g.insert_edge(xID, xID + X + 1,weight)
      if y < Y - 1:
        weight = abs(I[y, x] - I[y+1, x])
        g.insert_edge(xID, xID + X, weight)