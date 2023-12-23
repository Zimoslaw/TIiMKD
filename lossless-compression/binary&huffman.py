from collections import Counter
from bitarray import bitarray
import math


def main():
    file = open('norm_wiki_sample.txt', "r")
    content = file.read()

    text_entropy = entropy(content)

### Binarne ###
    codes = get_codes(content)  # Słownik, każdemu znakowi jest przypisywana liczba

    # Długość słów kodowych
    power = 2
    while math.pow(2, power) < len(codes):
        power += 1
    bit_per_char = power

    compressed = compress_binary(content, bit_per_char, codes)  # Zakodowana, skompresowana zawartość pliku

    # Stopień kompresji binarnej
    compression_grade = (len(content) * 8) / len(compressed)
    # Efektywność kompresji binarnej
    compression_efficiency = text_entropy / bit_per_char

    print(f'Binarna\nStopien kompresji: {compression_grade}\nEfektywnosc kodowania: {compression_efficiency}')

    decompressed = decompress_binary(compressed, bit_per_char, codes)  # Odkodowana zawartość pliku

    # Zapisanie odkodowanej zawartości
    new_file = open("norm_wiki_sample_decoded_binary.txt", "x")
    new_file.write(decompressed)

### Huffman ###
    trees = []  # tablica drzew

    # Tworzenie drzew prawdopodobieństw
    probabilities = get_probability(content)
    for key in probabilities.keys():
        tree = Node(key, probabilities[key])
        trees.append(tree)

    compressed = compress_huffman(content, trees)  # Kompresja, kodowanie tekstu

    average_word_length = get_average_word_length(trees[0], probabilities)

    # Stopień kompresji Huffmana
    compression_grade = (len(content) * 8) / len(compressed)
    # Efektywność kompresji Huffmana
    compression_efficiency = text_entropy / average_word_length

    print(f'Huffmana\nStopien kompresji: {compression_grade}\nEfektywnosc kodowania: {compression_efficiency}')

    decompressed = decompress_huffman(compressed, trees[0])  # Odkodowana zawartość pliku

    # Zapisanie odkodowanej zawartości
    new_file = open("norm_wiki_sample_decoded_huffman.txt", "x")
    new_file.write(decompressed)

    file.close()
    new_file.close()


# Kodowanie binarne
def compress_binary(content, bit_per_char, codes):
    content_new = bitarray()

    for char in content:
        content_new += int_to_bits(codes[char], bit_per_char)

    return content_new


# Dekodowanie binarne
def decompress_binary(compressed, bit_per_char, codes):
    decompressed = ''

    # Podzielenie ciągu bitów skompresowanej treści na cząstki o długości słowa kodującego
    compressed_split = [compressed[i * bit_per_char:(i + 1) * bit_per_char] for i in range((len(compressed) + bit_per_char - 1) // bit_per_char)]

    for char in compressed_split:
        index = bits_to_int(char)
        for key in codes.keys():
            if codes[key] == index:
                decompressed += key
                break

    return decompressed


# Kodowanie Huffmana
def compress_huffman(content, trees):
    compressed = bitarray()

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
        new_tree = Node(left.char + right.char, left.probability + right.probability)
        new_tree.left = left
        new_tree.right = right
        trees.insert(index, new_tree)

    # Kodowanie zawartości według drzewa Huffmana
    for char in content:
        node = trees[0]
        while node.char != char:
            if char in node.left.char:
                compressed.append(1)
                node = node.left
            else:
                compressed.append(0)
                node = node.right

    return compressed


# Dekodowanie Huffmana
def decompress_huffman(compressed, tree):
    decompressed = ''

    node = tree
    for bit in compressed:
        if bit == 0:
            node = node.right
        else:
            node = node.left
        if node.right == 0:
            decompressed += node.char
            node = tree

    return decompressed


# Obliczanie entropii
def entropy(text):

    # Prawdopdodobieństwo (całkowite)
    probabilities = get_probability(text)

    # Obliczanie entropii
    total = 0
    for key in probabilities.keys():
        total -= probabilities[key] * math.log(probabilities[key], 2)

    return total


# Prawdopdobieństwo każdego elemntu z zadanej tablicy
def get_probability(array: list[str]):
    counter = Counter(array)

    s = sum(counter.values())

    for key in counter:
        counter[key] /= s

    return counter


# Tworzeniee słownika
def get_codes(content):
    codes = {}
    index = 0

    for char in content:
        if char not in codes.keys():
            codes[char] = index
            index += 1

    return codes


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


# Zmiana ciągu bitów na liczbę
def bits_to_int(bits):
    n = 0
    bits = bits[::-1]

    for i in range(0, len(bits)):
        n += bits[i] * math.pow(2, i)

    return n


# Obliczanie przewidywanej średniej długości słowa kodowania
def get_average_word_length(tree, probabilities):
    sum = 0
    for char in probabilities.keys():
        length = 0
        node = tree
        while node.char != char:
            if char in node.left.char:
                length += 1
                node = node.left
            else:
                length += 1
                node = node.right
        sum += length * probabilities[char]

    return sum


# Klasa wierzchołka drzewa binarnego
class Node:
    char = ''
    probability = 0
    left = 0
    right = 0

    def __init__(self, char, probability):
        self.char = char
        self.probability = probability


if __name__ == "__main__":
    main()
