import numpy as np

def rekurencyjnie(P, T, i, j, D, parents):
    if i == 0:
        return j
    if j == 0:
        return i

    if D[i][j] != 0:
        return D[i][j]
    
    zamian = rekurencyjnie(P, T, i-1, j-1, D, parents) + (P[i-1] != T[j-1])
    wstawien = rekurencyjnie(P, T, i, j-1, D, parents) + 1
    usuniec = rekurencyjnie(P, T, i-1, j, D, parents) + 1

    D[i][j] = min(zamian, wstawien, usuniec)
    
    if D[i][j] == zamian:
        parents[i][j] = 'S' if P[i-1] != T[j-1] else 'M'
    elif D[i][j] == wstawien:
        parents[i][j] = 'I'
    else:
        parents[i][j] = 'D'
    
    return D[i][j]

def search_path(parents):
    X, Y = parents.shape
    operations = []
    i = X - 1
    j = Y - 1
    found = parents[i][j]
    while found != 'X':
        operations.append(found)
        if found == 'M' or found == 'S':
            i -= 1
            j -= 1
        elif found == 'D':
            i -= 1
        elif found == 'I':
            j -= 1
        found = parents[i][j]
    result = ''.join(reversed(operations))
    return result

def goal_cell(P, T, D):
    i = len(P) - 1
    j = 0
    for k in range(1, len(T)):
        if D[i][k] < D[i][j]:
            j = k
    return j

def search_subtext(P, T):
    lenP = len(P)
    lenT = len(T)
    
    D = np.zeros((lenP + 1, lenT + 1))
    for x in range(lenP + 1):
        D[x][0] = x
    for x in range(lenT + 1):
        D[0][x] = x

    parents = np.full((lenP + 1, lenT + 1), 'X', dtype=str)
    for x in range(1, lenP + 1):
        parents[x][0] = 'D'
    for x in range(1, lenT + 1):
        parents[0][x] = 'I'

    for i in range(1, lenP + 1):
        for j in range(1, lenT + 1):
            zamian = D[i-1][j-1] + (P[i-1] != T[j-1])
            wstawien = D[i][j-1] + 1
            usuniec = D[i-1][j] + 1
            D[i][j] = min(zamian, wstawien, usuniec)

            if D[i][j] == zamian:
                parents[i][j] = 'S' if P[i-1] != T[j-1] else 'M'
            elif D[i][j] == wstawien:
                parents[i][j] = 'I'
            else:
                parents[i][j] = 'D'

    j = goal_cell(P, T, D)
    cost = D[lenP, j]
    path = search_path(parents)
    
    return j, cost, path

# Example usage:
P = "ban"
T = "monkeyssbanana"
index, cost, path = search_subtext(P, T)
print(f"The best match ends at index {index} with cost {cost}")
print(f"Edit operations: {path}")
