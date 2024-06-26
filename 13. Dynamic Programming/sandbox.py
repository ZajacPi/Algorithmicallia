def suffix_array(word):
    suffixes = []
    for i in range(len(word) + 1):
        suffixes.append((i, word[i:]))
    suffixes.sort(key=lambda x: x[1])
    suffix_array = [i for i, suf in suffixes]
    return suffix_array

def binary_search(word, pattern, suffix_array):
    #indeksy początku i końca
    left, right = 0, len(suffix_array) - 1
    result = -1

    while left <= right:
        #znajduję środek
        mid = (left + right) // 2
        #przy pomocy tablicy odtwarzam suffix
        suffix = word[suffix_array[mid]:]

        if suffix.startswith(pattern):
            result = suffix_array[mid]  # update result to store the original index
            right = mid - 1  # continue searching in the left half to find the first occurrence
        elif suffix < pattern:
            left = mid + 1
        else:
            right = mid - 1
    return result

def test_suffix_array(word, patterns):
    S_array = suffix_array(word)
    for pattern in patterns:
        found = binary_search(word, pattern, S_array)
        if found != -1:
            print(f"Znaleziono wzorzec '{pattern}' na pozycji {found}")
            print(word[found:found+len(pattern)])
        else:
            print(f"Wzorzec '{pattern}' nie został znaleziony")

def main():
    test_suffix_array('banana', ['ana', 'na', 'ban'])

if __name__ == '__main__':
    main()
