import numpy as np
import time
#funkcja zwracająca odległość pomiędzy dwoma punktami (długość boku)
def distance(points, i, j):
    x1, y1 = points[i]
    x2, y2 = points[j]
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

def triangle_cost(points, i, j, k):
    return distance(points, i, j) + distance(points, j, k) + distance(points, k, i)

def triangulation(points):
    #osobno funckja rekurencyjna
    return  __triangulation(points, 0, len(points)-1)
                               
def __triangulation(points, i, j):
    #przypadek kończący rekurencję, mniej niż 3 punkty czyli różnica indeksów <2
    if j-i < 2:
        return 0
    minimal_cost = float('inf')
    #przechodzę po wszystkich punktach wielokąta
    for k in range(i + 1, j):
        #po kolei: lewy wielokąt, prawy wielokąt, koszt aktualnego trójkąta
        cost = (__triangulation(points, i, k) +__triangulation(points, k, j) +triangle_cost(points, i, k, j))
        #uaktualniam znaleziony minimalny koszt
        minimal_cost = min(cost, minimal_cost)
    return minimal_cost


def dynamic_triangulation(points):
    n = len(points)
    #tworzę tablicę pomocniczą, początkowo wypełnioną zerami
    costs = np.zeros((n, n))
    #przechodzę przez wszystkie możiwe rozmiary wielokątów, czyli od 2 do n-punktowego
    for size in range(2, n):
        for i in range(n-size):
            j = i + size
            #znów początkowo ustawiam na nieskończoność
            costs[i][j] = float('inf')
            for k in range(i+1, j):
                cost = costs[i][k] + costs[k][j] + triangle_cost(points, i, k, j)
                costs[i][j] = min(cost, costs[i][j])
    #ostatni element pierwszego wiersza to wynik
    return costs[0][n-1]


def test(points1, points2):
    print("Wersja rekurencyjna")
    t_start = time.perf_counter()
    min_cost = triangulation(points1)
    t_stop = time.perf_counter()
    calc_time =  t_stop-t_start
    print(f"Koszt: {min_cost}, Czas: {calc_time}")

    t_start = time.perf_counter()
    min_cost = triangulation(points2)
    t_stop = time.perf_counter()
    calc_time =  t_stop-t_start
    print(f"Koszt: {min_cost}, Czas: {calc_time}\n")

def test_dynamic(points1, points2):
    print("Wersja z programowaniem dynamicznym")
    
    t_start = time.perf_counter()
    min_cost = dynamic_triangulation(points1)
    t_stop = time.perf_counter()
    calc_time =  t_stop-t_start
    print(f"Koszt: {min_cost}, Czas: {calc_time}")
    
    t_start = time.perf_counter()
    min_cost = dynamic_triangulation(points2)
    t_stop = time.perf_counter()
    calc_time =  t_stop-t_start
    print(f"Koszt: {min_cost}, Czas: {calc_time}")

def main():
    points_1 = [[0, 0], [1, 0], [2, 1], [1, 2], [0, 2]]
    points_2 = [[0, 0], [4, 0], [5, 4], [4, 5], [2, 5], [1, 4], [0, 3], [0, 2]]

    test(points_1, points_2)
    test_dynamic(points_1, points_2)

if __name__ == "__main__":
    main()