from collections import Counter
from bitarray import bitarray
import math
import time
import sys

# Uruchamianie:
# python lzw.py [nazwa pliku] [ograniczenie długości słownika. 0 = brak ograniczenia]
# np. python lzw.py lena.bmp 4096
def main(argv):
    file = open(argv[0], "rb")
    content = file.read()
    file.close()

    start = time.time()

    # Kompresja LZW
    lzw_compressed, codes = compress_lzw(content, int(argv[1]))
    lzw_elapsed = time.time() - start

    # Kodowanie binarne i zapisywanie zakodowanego pliku (LZW)
    lzw_bin_compressed = compress_binary(lzw_compressed, codes)
    lzw_bin_file = open('cmp_lzw_' + argv[0], "wb")
    lzw_bin_file.write(lzw_bin_compressed)
    lzw_bin_file.close()
    lzw_bin_elapsed = time.time() - start

    # Kompresja Huffmana i zapisywanie skompresowanego pliku (LZW + Huffman)
    lzw_huff_compressed = compress_huffman(lzw_compressed)
    lzw_huff_file = open('cmp_lzw_huff_' + argv[0], "wb")
    lzw_huff_file.write(lzw_huff_compressed.tobytes())
    lzw_huff_file.close()
    lzw_huff_elapsed = time.time() - start - lzw_bin_elapsed + lzw_elapsed

    # Dekodowanie
    lzw_decompressed = decompress_lzw(lzw_compressed)
    # Zapisanie zdekompresowanego pliku
    file2 = open('decmp_lzw_' + argv[0], "wb")
    file2.write(lzw_decompressed)
    file2.close()

    print(f'Współczynnik kompresji dla "{argv[0]}" (LZW): {1 - (len(lzw_bin_compressed)) / len(content)} (czas: {lzw_bin_elapsed}s)')
    print(f'Współczynnik kompresji dla "{argv[0]}" (LZW + Huffman): {1 - (len(lzw_huff_compressed.tobytes()) / len(content))} (czas: {lzw_huff_elapsed}s)')


def compress_lzw(content, limit):
    codes = {}
    compressed = []

    # Inicjalizacja kodu
    c_index = 0  # Indeks słownika kodu
    for i in range(256):
        if str(i) not in codes:
            codes[str(i)] = i
            c_index += 1

    # Kompresja
    s = str(content[0])
    for i in range(len(content) - 1):
        c = str(content[i + 1])

        if s + ',' + c not in codes:
            compressed.append(codes[s])
            if limit != 0:  # Ograniczenie wielkości słownika
                if c_index < limit:
                    codes[s + ',' + c] = c_index
                    c_index += 1
            else:  # Bez ograniczenia długości słownika
                codes[s + ',' + c] = c_index
                c_index += 1
            s = c
        else:
            s = s + ',' + c
    compressed.append(codes[s])

    return compressed, codes


def decompress_lzw(compressed):
    codes = {}
    bytes = ''

    # Inicjalizacja kodu
    c_index = 0
    for i in range(256):
        if i not in codes:
            codes[str(i)] = str(i)
            c_index += 1

    # Dekodowanie
    C = str(compressed[0])
    OLD = str(compressed[0])
    bytes += codes[OLD]
    for i in range(len(compressed) - 1):
        NEW = str(compressed[i + 1])

        if NEW in codes:
            WORD = codes[NEW]
        else:
            WORD = codes[OLD] + ',' + C

        bytes += ',' + WORD

        WORD = WORD.split(',')
        C = WORD[0]

        codes[str(c_index)] = codes[OLD] + ',' + C
        c_index += 1

        OLD = NEW

    decompressed = []
    bytes = bytes.split(',')
    for b in bytes:
        decompressed.append(int(b).to_bytes(1, sys.byteorder))

    return b''.join(decompressed)


# Kodowanie binarne
def compress_binary(content, codes):
    content_new = bitarray()

    # Długość słów kodowych
    power = 2
    while math.pow(2, power) < len(codes):
        power += 1
    bit_per_char = power

    # Kodowanie
    for char in content:
        content_new += int_to_bits(char, bit_per_char)

    return content_new.tobytes()


# Kodowanie Huffmana
def compress_huffman(content):
    compressed = bitarray()
    trees = []  # tablica drzew

    # Tworzenie drzew prawdopodobieństw
    probabilities = get_probability(content)
    for key in probabilities.keys():
        tree = Node([key], probabilities[key])
        trees.append(tree)

    # Tworzenie drzewa Huffmana
    while len(trees) > 1:
        left = trees[0]
        # Poszukiwanie drzewa z najmniejszym prawdopodobieństwem
        for tree in trees:
            if tree.probability < left.probability:
                left = tree
        index = trees.index(left)
        trees.remove(left)

        right = trees[0]
        # Poszukiwanie drzewa z drugim najmniejszym pradopodobieństwem
        for tree in trees:
            if tree.probability < right.probability:
                right = tree
        trees.remove(right)

        # Tworzenie nowego drzewa z drzew z najmniejszym prawdodpodobieństwem
        chars = []
        for c in left.char:
            chars.append(c)
        for c in right.char:
            chars.append(c)
        new_tree = Node(chars, left.probability + right.probability)
        new_tree.left = left
        new_tree.right = right
        trees.insert(index, new_tree)

    # Kodowanie zawartości według drzewa Huffmana
    for char in content:
        node = trees[0]
        while node.char != [char]:
            if char in node.left.char:
                compressed.append(1)
                node = node.left
            else:
                compressed.append(0)
                node = node.right

    return compressed


# Dekodowanie Huffmana
def decompress_huffman(compressed, tree):
    decompressed = []

    node = tree
    for bit in compressed:
        if bit == 0:
            node = node.right
        else:
            node = node.left
        if node.right == 0:
            decompressed.append(node.char)
            node = tree

    return decompressed


# Prawdopdobieństwo każdego elemntu z zadanej tablicy
def get_probability(array: list[int]):
    counter = Counter(array)

    s = sum(counter.values())

    for key in counter:
        counter[key] /= s

    return counter


# Zamiana liczby na ciąg bitów
def int_to_bits(n, length):
    bits = ''
    while n > 0:
        if n % 2 == 0:
            bits += '0'
        else:
            bits += '1'
        n = int(n/2)

    while len(bits) < length:
        bits += '0'

    return bits[::-1]


# Klasa wierzchołka drzewa binarnego
class Node:
    char = 0
    probability = 0
    left = 0
    right = 0

    def __init__(self, char, probability):
        self.char = char
        self.probability = probability


if __name__ == "__main__":
    main(sys.argv[1:])
