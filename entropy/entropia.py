import sys
import getopt
import math


def main(argv):
    file = '' # Ścieżka do pliku
    entropy_type = '' # Typ entropii (znaków lub słów)
    level = 0 # Rząd entropii
    opts, args = getopt.getopt(argv, "hf:t:n:")
    for opt, arg in opts:
        if opt == '-h':
            print('Stosowanie:')
            print('entropia.py -f <nazwa_pliku> -t <C|W> -n [liczba]')
            print('Parametry:')
            print('nazwa_pliku - ścieżka do pliku zawierającego tekst do analizy')
            print('C - entropia znaków. W - entropia słów')
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


def entropy(file, text, type, level):
    # Tworzenie alfabetu
    alphabet = {}
    alphabet_secondary = {}
    if type == 'W':  # Entropia słów
        text = text.split() # Alfabet zamiast z liter składać się będzie ze słów

    elements = list(text) # Lista wszystkich znaków/słów tekstu
    char_number = len(elements)  # Ilość wszystkich elementów
    for c in range(0, char_number):
        char = elements[c]

        # Pomocniczy alfabet dla rzędów większych niż 0
        if level > 0:
            if char in alphabet_secondary.keys():
                alphabet_secondary[char] += 1
            else:
                alphabet_secondary[char] = 1

        if c + level < len(elements):

            # Tworzenie elementu według rzędu
            for i in range(1, level + 1):
                char += ' ' + elements[c+i]

            # Obliczanie ilości danego elementu
            if char in alphabet.keys():
                alphabet[char] += 1
                continue
            alphabet[char] = 1

    # Prawdopodobieństwo elementu / Prawdopodobieństwo wspólne
    probabilities = {}
    for key in alphabet.keys():
        probabilities[key] = alphabet[key] / char_number

    # Prawdopodobieństwo warunkowe
    probabilities_conditional = {}
    if level > 0:
        for key in alphabet.keys():
            probabilities_conditional[key] = 1
            l = 0
            chars = key.split()
            for char in chars:
                probabilities_conditional[key] *= alphabet_secondary[char] / (char_number - l)
                l += 1

    # Obliczanie entropii
    sum = 0
    for key in probabilities.keys():
        if level == 0:
            sum += probabilities[key] * math.log(probabilities[key], 2)
        else:
            sum += probabilities[key] * math.log(probabilities_conditional[key], 2)
    sum *= -1

    if level == 0:
        if type == 'C':
            print('Entropia znaków tekstu z pliku', file, '=', sum)
        else:
            print('Entropia słów tekstu z pliku', file, '=', sum)
    else:
        if type == 'C':
            print('Entropia warunkowa znaków', level, 'stopnia tekstu z pliku', file, '=', sum)
        else:
            print('Entropia warunkowa słów', level, 'stopnia tekstu z pliku', file, '=', sum)


if __name__ == "__main__":
    main(sys.argv[1:])
