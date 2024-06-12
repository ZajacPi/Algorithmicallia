import numpy as np
import time
import math

def hash(word, N, q=101, d = 256):
    hw = 0
    for i in range(N):  # N - to długość wzorca
        hw = (hw*d + ord(word[i])) % q  # dla d będącego potęgą 2 można mnożenie zastąpić shiftem uzyskując pewne przyspieszenie obliczeń
    return hw

def bloom_filter_check (bloom_array, targets, S, q_list, N, b):
    h = 1
    M = len(S)
    #tworzę listę gdzie będę wpisywał bity do uzupełnienia
    found = {}
    #teraz używam rollong hash, więc robię listę poprzednich hashy
    hashes = np.zeros(len(q_list))
    false_positives = []

    for m in range(0, M-N+1):
        check = True
        analysing = S[m: m + N]
        if m == 0:
            for i, q in enumerate(q_list):
                hS = hash(S[0: N], N, q)
                hashes[i] = hS
                if bloom_array[hS] == False:
                    check = False
        else:  
            for i, q in enumerate(q_list):
                #metoda pow jest szybsza
                h = pow(256, N-1, q)
                #żeby wziąć poprzedni hasz dla konkretnego q pobieram go ze starej listy hashy
                hashes[i] = ((256 * (hashes[i]- ord(S[m-1]) * h) + ord(S[m + N-1])) % q)
                if hashes[i] < 0:
                    hashes[i] += q
                if bloom_array[int(hashes[i])] == False:
                    check = False
        #teraz sprawdzam czy filtr blooma potwierdza, a pote czy fałszywa pozytywna
        if check:
            false_pos = True
            for word in targets:
                if word == S[m: m + N]:
                    if word in found:
                        found[word] += 1
                    else:
                        found[word] = 1
                    false_pos = False
            if false_pos:
                false_positives.append(S[m: m + N])

    return found, false_positives

def create_bloom_array(W, q_list, b):
    bloom_array = np.zeros(b, dtype=bool) #kiedy wartości są boolean to zajmuje najmniej miejsca
    for word in W:
        for q in q_list:
            #każde słowo z szukanych haszuję k różnymi funkcjami haszującymi 
            bloom_array[hash(word, len(word), q)] = True
    return bloom_array

def test_bloom(S, W, qd_list, b, N):
    bloom_array = create_bloom_array(W, qd_list, b)
    found, false_positives= bloom_filter_check(bloom_array, W, S, qd_list, N, b)
    if len(found)>0:
            print(f"Filtr wykazał, że wzorce pojawiają się w tekście:\n")
            for word, count in found.items():
                print(f"{word} -> {count} razy")        
            print(f"Ilość fałszywych pozytywnych: {len(false_positives)} \n {false_positives}")
    else:
        print(f"Filtr wykazał, że wzorzec {W} nie występuje w tekście")

def main():
    targets = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however', 'popular', 'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself', 'present', 'deliver', 'welcome', 'baggins', 'further']

    n = len(targets) #liczba elementów w filtrzze cztli liczba wyszukiwanych wzroców
    N = len(targets[0])
    P = 0.001 #dopuszczalne prawdopodobieństwo pomyłki
    b = math.ceil(-n*np.log(P)/(np.log(2))**2) #rozmiar tablicy, otrzymuję warotść 288
    k = math.ceil((b/n)*np.log(2)) #ilość funkcji haszujących, otrzymuję wartość 10
    
    #tworzę listę dziesięciu różnych liczb pierwszych
    # q_list = [101, 113, 127, 151, 167, 173, 179, 181, 191, 197]
    q_list = [239, 241, 251, 257, 263, 269, 271, 277, 281, 283]
    #użycie większych liczbn pierwszych drastycznie zmniejsza liczbę fałszywych pozytywnych


    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()
    W = targets
    test_bloom(S, W, q_list, b, N)

if __name__ == "__main__":
    main()