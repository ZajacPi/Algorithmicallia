import time

def naive(text, template):
    counter = 0
    S = 0
    W = 0
    dot = '.'
    positions = []
    comparisons = 0
    found_position = 0
    t_start = time.perf_counter()
    while S != len(text):
        if text[S] == template[W]:
            W += 1
            comparisons += 1
            if W == len(template)-1:
                #sprawdzam czy nie wyjdę poza zakres, jeśli na smaym końcu będzie wzorzec
                if S+1<len(text) and text[S+1] == dot:
                    counter += 1
                    positions.append(found_position+1) 
                W = 0
        else:
            W = 0
            found_position = S

        S+=1

    t_stop = time.perf_counter()
    calc_time = t_stop - t_start
    return counter, calc_time, positions, comparisons

    
def test_naive(text, template):
    S = text
    W = template
    counter, time, positions, comparisons = naive(S, W)
    print("Metoda naiwna")
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
    test_naive(S, W)

    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()
    S2 = ' '.join(text).lower()
    test_naive(S2, W)

if __name__ == "__main__":
    main()