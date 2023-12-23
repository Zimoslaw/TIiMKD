from collections import Counter
from bitarray import bitarray
import math


def main():
    file = open('test.txt', "r")
    content = file.read()

    text_entropy = entropy(content)



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