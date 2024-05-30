import time
from naive import test_naive
from RabinKarp import test_rabinKarp
from RabinKarp_rollingHash import test_rabinKarp_Rolling


def main():
    with open("test2.txt", encoding='utf-8') as f:
        text = f.readlines()
    S = ' '.join(text).lower()
    W = "time."
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()
    S2 = ' '.join(text).lower()

    # test_naive(S, W)
    # test_rabinKarp(S, W)
    # test_rabinKarp_Rolling(S, W)

    test_naive(S2, W)
    test_rabinKarp(S2, W)
    test_rabinKarp_Rolling(S2, W)


if __name__ == "__main__":
    main()