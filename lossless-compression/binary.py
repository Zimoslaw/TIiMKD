from collections import Counter
from bitarray import bitarray
import math


def main():
    file = open('norm_wiki_sample.txt', "r")
    content = file.read()

    text_entropy = entropy(content)

    codes = get_codes(content)  # Słownik, każdemu znakowi jest przypisywana liczba

    # Długość słów kodowych
    power = 2
    while math.pow(2, power) < len(codes):
        power += 1
    bit_per_char = power

    compressed = compress(content, bit_per_char, codes)  # Zakodowana, skompresowana zawartość pliku

    # Stopień kompresji
    compression_grade = (len(content) * 8) / len(compressed)
    # Efektywność kompresji
    compression_efficiency = text_entropy / bit_per_char

    print(f'Binarna\nStopien kompresji: {compression_grade}\nEfektywność kompresji: {compression_efficiency}')

    decompressed = decompress(compressed, bit_per_char, codes)  # Odkodowana zawartość pliku

    # Zapisanie odkodowanej zawartości
    new_file = open("norm_wiki_sample_decompressed.txt", "x")
    new_file.write(decompressed)

    file.close()
    new_file.close()


# Kompresja
def compress(content, bit_per_char, codes):
    content_new = bitarray()

    for char in content:
        content_new += int_to_bits(codes[char], bit_per_char)

    return content_new


# Dekompresja
def decompress(compressed, bit_per_char, codes):
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


if __name__ == "__main__":
    main()
