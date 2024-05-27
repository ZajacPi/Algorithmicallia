import numpy as np
def exist(matrix, neighboursP, neighboursG):
  for x in neighboursP:
    exist = False
    for y in neighboursG:
      if matrix[x][y]:
        exist = True
    if not exist:
      return False
  return True

def prune(matrix, G : 'Graph', P : 'Graph', row):
  Y, X = matrix.shape
  change = True
  while change:
    change = False
    for i in range(row, Y):
      for j in range(X):
        if matrix[i][j] == 0:
          continue
        
        neighboursP = [P.getVertexID(x) for x, _ in P.neighbours(i)]
        neighboursG = [G.getVertexID(y) for y, _ in G.neighbours(j)]
        e = exist(matrix, neighboursP, neighboursG)
        if not e:
          matrix[i][j] = 0
          change = True
          break
        
  return matrix
             
def ullmann3(G , P):
  Y = len(P.vertices())
  X = len(G.vertices())
  M = np.zeros((Y, X))
  matrices = []
  usedCols = [False] * X
  calls = 0
  # counting M0
  M0 = np.zeros((Y,X), dtype=int)
  for i in range(Y):
    degVi = len(P.neighbours(i))
    for j in range(X):
      degVj = len(G.neighbours(j))
      if degVi <= degVj:
        M0[i, j] = 1
  
  def backtrack(matrix, row):
    nonlocal matrices, Y, X, G, P, calls
    calls += 1
    # stop condition
    if (row == Y):
      if np.all(P.matrix == matrix @ np.transpose(matrix @ G.matrix)):
        matrices.append(matrix)
      return
    prune(matrix, G, P, row)
    for col in range(X):
      if not usedCols[col] and matrix[row, col]:
        newM = deepcopy(matrix)
        usedCols[col] = True
        newM[row, 🙂 = 0
        newM[row, col] = 1
        backtrack(newM, row + 1)
        usedCols[col] = False
  backtrack(M0, 0)
  return matrices, calls