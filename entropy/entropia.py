from collections import Counter
import sys
import getopt
import math


def main(argv):
    file = ''  # Ścieżka do pliku
    entropy_type = ''  # Typ entropii (znaków lub słów)
    level = 0  # Rząd entropii
    opts, args = getopt.getopt(argv, "hf:t:n:")
    for opt, arg in opts:
        if opt == '-h':
            print('Stosowanie:')
            print('entropia.py -f <nazwa_pliku> -t <C|W> -n <liczba>')
            print('Parametry:')
            print('nazwa_pliku - ścieżka do pliku zawierającego tekst do analizy')
            print('C - entropia znaków (characters). W - entropia słów (words)')
            print('liczba - rząd entropi warunkowej. 0 oznacza entropię niewarunkową')
            sys.exit()
        elif opt == '-f':
            file = arg
        elif opt == '-t':
            entropy_type = arg
            if entropy_type != 'C' and entropy_type != 'W':
                print("Nieprawidłowa wartość argumentu -t. Oczekiwano 'C' lub 'W'")
                sys.exit()
        elif opt == '-n':
            level = int(arg)

    content = open(file, 'r')

    entropy(file, content.read(), entropy_type, level)


def entropy(file, text, entropy_type, level):
    if entropy_type == 'W':  # Entropia słów
        text = text.split(" ")  # Alfabet zamiast z liter składać się będzie ze słów
        text = tuple(text)

    if level == 0:
        # Prawdopdodobieństwo (całkowite)
        probabilities = get_probability(text)
    else:
        # fragmenty n-tego rzędu
        alphabet = [text[i: i + level + 1] for i in range(len(text) - level)]
        # Prawdopdobieństwo fragmentów n-tego rzędu
        probabilities = get_probability(alphabet)
        # Prawdopdobieństwo fragmentów (n-1)-tego rzędu
        probabilities_secondary = get_probability([char[:-1] for char in alphabet])

        probabilities_conditional = {}

        # Prawdopodobieństwo warunkowe
        for char in alphabet:
            probabilities_conditional[char] = probabilities[char] / probabilities_secondary[char[:-1]]

    # Obliczanie entropii
    total = 0
    if level == 0:
        for key in probabilities.keys():
            total -= probabilities[key] * math.log(probabilities[key], 2)
    else:
        for key in probabilities.keys():
            total -= probabilities[key] * math.log2(probabilities_conditional[key])

    if level == 0:
        if entropy_type == 'C':
            print('Entropia znakow tekstu z pliku', file, '=', total)
        else:
            print('Entropia slow tekstu z pliku', file, '=', total)
    else:
        if entropy_type == 'C':
            print('Entropia warunkowa znakow', level, 'rzedu tekstu z pliku', file, '=', total)
        else:
            print('Entropia warunkowa slow', level, 'rzedu tekstu z pliku', file, '=', total)


# Prawdopdobieństwo każdego elemntu z zadanej tablicy
def get_probability(array: list[str]):
    counter = Counter(array)

    s = sum(counter.values())

    for key in counter:
        counter[key] /= s

    return counter


if __name__ == "__main__":
    main(sys.argv[1:])
