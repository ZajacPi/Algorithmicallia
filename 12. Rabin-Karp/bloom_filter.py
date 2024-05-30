import numpy as np
import time
import math
targets = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however', 'popular', 'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself', 'present', 'deliver', 'welcome', 'baggins', 'further']
def hash1(word, N, d, q):
    hw = 0
    for i in range(N):  # N - to długość wzorca
        hw = (hw*d + ord(word[i])) % q  # dla d będącego potęgą 2 można mnożenie zastąpić shiftem uzyskując pewne przyspieszenie obliczeń
    return hw

def rabinKarp_Rolling(S, W, d, q):
    t_start = time.perf_counter()
    h = 1
    N = len(W)
    M = len(S)
    hS = None
    for i in range(N-1): 
        h = (h*d) % q 

    hW = hash1(W, N, d, q)
    positions = []
    counter = 0
    comparisons = 0
    collisions = 0
    for m in range(0, M-N+1):
        if hS == None:
            hS = hash1(S[m: N+m], N, d, q)
        else:
            # test_hs = hash(S[m: N+m], N, d, q) do debuggowania,powinno wyjść tyle samo ile hash z użyciem rollingu
            hS = (d*(hS - ord(S[m-1]) * h) + ord(S[m + N-1])) % q
            if hS < 0:
                hS += q
        comparisons += 1
        #teraz w filtrze blooma ustawiam obliczony numer bitu na wysoki
        if hS == hW:
            found = S[m : m+N]
            template =W[0 : N]
            if found == template:
                positions.append(m)
                counter += 1
            else:
                collisions += 1
   
    t_stop = time.perf_counter()
    calc_time =  t_stop-t_start

    return counter, calc_time, positions, comparisons, collisions


def bloom_Filter():
   
    print()

def test_bloom():

    bloom_Filter()

def main():
    n = 20 #liczba elementów w filtrzze cztli liczba wyszukiwanych wzroców
    P = 0.001 #dopuszczalne prawdopodobieństwo pomyłki
    b = math.ceil(-n*np.log(P)/(np.log(2))**2) #rozmiar tablicy
    k = math.ceil((b/n)*np.log(2)) #ilość funkcji haszujących, otrzymuję wartość 10
    test_bloom()
    
if __name__ == "__main__":
    main()