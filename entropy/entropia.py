import sys, getopt, math

def main(argv):
    file = ''
    entropy_type = ''
    level = 0
    opts, args = getopt.getopt(argv,"hf:t:n")
    for opt, arg in opts:
        if opt == '-h':
            print ('entropia.py -f <filename> -t <C|W> -n [number]')
            print ('filename - file with text to be analyzed. Text should be in english alphabet.')
            print ('C - characters entropy. W - words entropy')
            print ('number - number of characters/words used in conditional entropy')
            sys.exit()
        elif opt == '-f':
            file = arg
        elif opt == '-t':
            entropy_type = arg
            if entropy_type != 'C' and entropy_type !='W':
                print("Invalid it argument. Expected 'C' or 'W'")
                sys.exit()
        elif opt == '-n':
            level = arg

    content = open(file, 'r')
    
    entropy(content.read(), entropy_type, level)

def entropy(text, type, level):
    # Tworzenie alfabetu
    alphabet = {}
    if type == 'W': # Entropia słów
        text = text.split()

    for c in text:
        if c in alphabet.keys():
            alphabet[c] += 1
            continue
        alphabet[c] = 1

    print(str(alphabet))

    # Prawdopodobieństwa
    for k in alphabet.keys():
        alphabet[k] = alphabet[k]/len(text)

    # Obliczanie entropii
    sum = 0
    for k in alphabet.keys():
        sum += alphabet[k] * math.log(alphabet[k], 2)
    sum *= -1

    print('Entropy =', sum)

if __name__ == "__main__":
   main(sys.argv[1:])