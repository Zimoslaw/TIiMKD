import sys
import getopt
import math


def main(argv):
    file = ''
    entropy_type = ''
    level = 0
    opts, args = getopt.getopt(argv, "hf:t:n:")
    for opt, arg in opts:
        if opt == '-h':
            print('Usage:')
            print('entropia.py -f <filename> -t <C|W> -n [number]')
            print('Parameters:')
            print('filename - file with text to be analyzed. Text should be in english alphabet.')
            print('C - characters entropy. W - words entropy')
            print('number - number of characters/words used in conditional entropy')
            print('Parameter -n is optional.')
            sys.exit()
        elif opt == '-f':
            file = arg
        elif opt == '-t':
            entropy_type = arg
            if entropy_type != 'C' and entropy_type != 'W':
                print("Invalid it argument. Expected 'C' or 'W'")
                sys.exit()
        elif opt == '-n':
            level = int(arg)

    content = open(file, 'r')

    entropy(content.read(), entropy_type, level)


def entropy(text, type, level):
    # Tworzenie alfabetu
    alphabet = {}
    alphabet_secondary = {}
    if type == 'W':  # Entropia słów
        text = text.split() # Alfabet zamiast z liter składać się będzie ze słów

    unique_elements = list(text)
    for c in range(0, len(unique_elements)):
        char = unique_elements[c]
        if c + level < len(unique_elements):

            if level > 0: # Pomocniczy alfabet
                if char in alphabet_secondary.keys():
                    alphabet_secondary[char] += 1
                else:
                    alphabet_secondary[char] = 1

            for i in range(1, level + 1):
                char += unique_elements[c+i]

            if char in alphabet.keys():
                alphabet[char] += 1
                continue
            alphabet[char] = 1

    print(str(alphabet))

    # Prawdopodobieństwo elementu / Prawdopodobieństwo wspólne
    probabilities = {}
    for k in alphabet.keys():
        probabilities[k] = alphabet[k] / len(text)

    # Prawdopodobieństwo warunkowe
    #if level > 0:


    # Obliczanie entropii
    sum = 0
    for k in probabilities.keys():
        sum += probabilities[k] * math.log(probabilities[k], 2)
    sum *= -1

    print('Entropy =', sum)


if __name__ == "__main__":
    main(sys.argv[1:])
