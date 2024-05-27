import numpy as np
import copy

def ullmann_V2(używane, G, P, M, aktualny_wiersz=0, izomorfizmy=None, calls=1):
    if izomorfizmy is None:
        izomorfizmy = []

    liczba_wierszy = len(M)

    # Check isomorphism
    if aktualny_wiersz == liczba_wierszy:
        MG = np.dot(M, G)
        check = np.dot(MG, M.T)
        if np.array_equal(check, P):
            izomorfizmy.append(np.copy(M))
        return izomorfizmy, calls

    for c in range(len(M[0])):
        if not używane[c] and M[aktualny_wiersz][c] != 0:
            używane[c] = True
            M0 = np.copy(M)
            M0[aktualny_wiersz, :] = 0
            M0[aktualny_wiersz, c] = 1
            izomorfizmy, calls = ullmann_V2(używane, G, P, M0, aktualny_wiersz + 1, izomorfizmy, calls)
            calls += 1
            używane[c] = False

    return izomorfizmy, calls

# Example usage
G = np.array([
    [0, 1, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 0, 1],
    [0, 0, 0, 1, 1, 0]
])

P = np.array([
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
])

# Initialize the matching matrix M and the used columns list
M = np.zeros((P.shape[0], G.shape[0]))
używane = [False] * G.shape[0]

# Find isomorphisms
izomorfizmy, calls = ullmann_V2(używane, G, P, M)
print("Found isomorphisms:", len(izomorfizmy))
print("Number of recursive calls:", calls)
for izomorfizm in izomorfizmy:
    print(izomorfizm)