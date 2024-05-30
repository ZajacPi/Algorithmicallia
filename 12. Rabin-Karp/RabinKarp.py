import time
def hash(word, template, d=256, q=101):
    hw = 0
    N = len(template)
    for i in range(N):  # N - to długość wzorca
        hw = (hw*d + ord(word[i])) % q  # dla d będącego potęgą 2 można mnożenie zastąpić shiftem uzyskując pewne przyspieszenie obliczeń
    return hw

def rabinKarp(S, W):
    t_start = time.perf_counter()
    counter = 0
    comparisons = 0
    dot = "."
    hW = hash(W, W)
    N = len(W)
    M = len(S)
    positions = []
    for m in range(0, M-N+1):
            hS = hash(S[m: N+m], W)
            comparisons += 1

            if hS == hW:
                found = S[m : m+N]
                template =W[0 : N]
                if found == template:
                    positions.append(m)
                    counter += 1
   
    t_stop = time.perf_counter()
    calc_time =  t_stop-t_start

    return counter, calc_time, positions, comparisons


def test_rabinKarp(text, template):
    S = text
    W = template
    counter, time, positions, comparisons = rabinKarp(S, W)
    print("Metoda Rabina Karpa bez rolling-hash")
    print("#########################################")
    print("Czas obliczeń:", "{:.7f}".format(time))
    print(f"Ilość znalezionych wzorców:{counter}")
    print(f"Wzorce na pozycjach:{positions}")
    print(f"Ilość porównań: {comparisons}")
    print()

def main():
    with open("test.txt", encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()
    W = "time."

    test_rabinKarp(S, W)
    #fajnie by było gdyby po znalezieniu indeksu pozycji cofało się i printowało całe zdanie  w którym zostało znalezione
    # for i in positions:
    #     print(S[i:])
    
if __name__ == "__main__":
    main()