import numpy as np
import time
import math

from RabinKarp_rollingHash import rabinKarp_Rolling, test_rabinKarp_Rolling
primeNumbers = [167,3943,2591,7681,239,109,53,113,241,191,193,97,127,263,229,79,83,251,181,139]
powersOf2 = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]

def hash(word, N, q=101, d = 256):
    hw = 0
    for i in range(N):  # N - to długość wzorca
        hw = (hw*d + ord(word[i])) % q  # dla d będącego potęgą 2 można mnożenie zastąpić shiftem uzyskując pewne przyspieszenie obliczeń
    return hw

def create_bloomFilterArray(S, W, qd_list, b,  d = 256):
    bloom_array = np.zeros(b, dtype=bool) #kiedy wartości są boolean to zajmuje najmniej miejsca
    h = 1
    N = len(W)
    M = len(S)
    #tworzę listę gdzie będę wpisywał bity do uzupełnienia
    hashes = []

    for m in range(0, M-N+1):
        #pierwsze hashowanie ładnie pokazuje ideę: zamiast pisania wielu funkcji haszujących będę wywoływał tą samą ale z różnymi liczbami pierwszymi
        #uzupełniam pierwszą listę haszy, które potem będę aktualizował dla konkretnego q
        if m == 0:
            for q, d in qd_list:
                hashes.append(hash(S[0: N], N, q, d))
        else:  
            for idx, qd in enumerate(qd_list):
                q = qd[0]
                d = qd[1]
                #metoda pow jest szybsza
                h = pow(d, N-1, q)
                #żeby wziąć poprzedni hasz dla konkretnego q pobieram go ze starej listy hashy
                hS = (d * (hashes[idx] - ord(S[m-1]) * h) + ord(S[m + N-1])) % q
                if hS < 0:
                    hS += q
                hashes[idx] = hS
            
        #teraz w filtrze blooma ustawiam każdy obliczony numer bitu na wysoki
        for i in hashes:
            # bloom_array[i] = 1
            bloom_array[i%b] = True


    return bloom_array

def check_instance(bloom_array, word, q_list):
    hashes = []
    for q, d in q_list:
        hashes.append(hash(word, len(word), q, d))
    for i in hashes:
        if bloom_array[i] != 1:
            return False
    return True

def test_bloom(S, W, q_list, b):
    bloom_array = create_bloomFilterArray(S, W, q_list, b)
    if check_instance(bloom_array, W, q_list):
        print(f"Filtr wykazał, że wzorzec: {W} pojawia się w tekście, sprawdzam metodą Rabina Karpa\n")
        test_rabinKarp_Rolling(S, W)
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
    qd_list = [(primeNumbers[i], powersOf2[i // 2]) for i in range(k)]


    with open("no_time.txt", encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()
    W = "time."
    test_bloom(S, W, qd_list, b)


    # with open("lotr.txt", encoding='utf-8') as f:
    #     text = f.readlines()
    # S = ' '.join(text).lower()
    # for W in targets:
    #     test_bloom(S, W, q_list, b)
    
if __name__ == "__main__":
    main()