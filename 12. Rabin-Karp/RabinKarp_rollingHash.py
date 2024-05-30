import time
from naive import naive
def hash(word, N, d, q):
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

    hW = hash(W, N, d, q)
    positions = []
    counter = 0
    comparisons = 0
    collisions = 0
    for m in range(0, M-N+1):
        if hS == None:
            hS = hash(S[m: N+m], N, d, q)
        else:
            # test_hs = hash(S[m: N+m], N, d, q) do debuggowania,powinno wyjść tyle samo ile hash z użyciem rollingu
            hS = (d*(hS - ord(S[m-1]) * h) + ord(S[m + N-1])) % q
            if hS < 0:
                hS += q
        comparisons += 1

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

def test_rabinKarp_Rolling(text, template, q=101, d=256):
    S = text
    W = template
    counter, time, positions, comparisons, collisions = rabinKarp_Rolling(S, W, d, q)
    print("Metoda Rabina Karpa używając rolling-hash")
    print("#########################################")
    print("Czas obliczeń:", "{:.7f}".format(time))
    print(f"Ilość znalezionych wzorców:{counter}")
    print(f"Wzorce na pozycjach:{positions}")
    print(f"Ilość porównań: {comparisons}")
    print(f"Ilość kolizji z wynikających z hashowania: {collisions}")
    print()

def main():
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()
    W = "time."

    test_rabinKarp_Rolling(S, W)


if __name__ == "__main__":
    main()
