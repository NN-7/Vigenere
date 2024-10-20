# A simple program to generate ciphers and deciphers of the Vigenère cipher.
# It took me about 4 hours to make in total. 2.5 hours of which were spent on the cipher functions. The decipher was
# very simple in theory and most of the code can be copied from the cipher functions with little difference.
# It took 45 minutes to make the decipher, and the rest of the time was spent on debugging.

# The program was built to be dynamic, and it supports any alphabet you could create with any one letter unicode
# characters. It can also support any plain text and key, as well as keyed alphabet, but make sure that any letters
# used in the 3 parameters mentioned are also included in the alphabet, or the program will fail.

import re

# From hereon code for anything needed to cipher/decipher

def print_vigenere_table(Alphabet, VigenereTable):
    # prints the Vigenère table for any miscellaneous reasons.
    output = "   " # spaces to account for leftmost column
    for letter in Alphabet:
        output += f"{letter} "
    # ▲ Adds the letters to the top reference row.

    n = 0
    # ▼ Makes the rest of the rows of the Vigenère table.
    for row in VigenereTable:
        output += f"\n{Alphabet[n]} " # Adds  reference letter for every row.
        n += 1
        for column in row: # Adds the rest of the letters of each row.
            output += f" {column[0]}"
    print(output)
    return output

def generate_letter_reference_dict(Alphabet):
    # makes a dictionary to quickly refer a letter to its index in the Vigenère table.
    ReferenceDict = {}
    n = 0
    for letter in Alphabet:
        ReferenceDict[letter] = n
        n += 1
    # ▲ very simple, just sets every letter as a key in the dictionary and its index in the alphabet as the value.
    return ReferenceDict

def keyed_alphabet_generator(Alphabet, KeyedAlphabetWord): # NOTE: Keyed alphabet word MUST be fully lowercase
    # Makes a keyed alphabet for you if you wish to make the cipher more complicated.
    KeyedAlphabet = KeyedAlphabetWord
    KeyedAlphabet += re.sub(f"[{KeyedAlphabetWord}]", "", Alphabet)
    # ▲ Moves every letter in the keyword from whatever its location is in the alphabet to the front.
    # NOTE: Would not work with duplicate letters.
    return KeyedAlphabet

def letter_mover(Alphabet):
    # Shifts the letter in the front to the end to make a new row for the Vigenère table.
    ShiftedAlphabet = Alphabet[1:] + Alphabet[0]
    # ▲ Makes the new row equal to the every letter in the alphabet plus the first letter,
    # effectively moving it to the end.
    return ShiftedAlphabet

def generate_vigenere_table(Alphabet): # Makes the Vigenère table for the cipher.
    VigenereTable = []
    ShiftedAlphabet = Alphabet

    for n in range(len(Alphabet)):
        VigenereTable += [[]]
        ShiftedAlphabet = letter_mover(ShiftedAlphabet)
        for letter in ShiftedAlphabet:
            VigenereTable[n] += letter
        n += 1
    # ▲ Makes a new row, adds each of the progressively more shifted alphabet to the Vigenère table.
    VigenereTable = VigenereTable[-1:] + VigenereTable[:len(VigenereTable)-1]
    # ▲ The row that should have been at the start was in the end, this moves the last row to the beginning of the list.

    return VigenereTable

def make_keystream(KeyWord, PlainText):
    # Makes the key stream line up with the plain text so it can be ciphered properly.
    NeededLength = len(PlainText)
    KeyLength = len(KeyWord)
    KeyStream = KeyWord
    AddedLength = NeededLength - KeyLength
    if AddedLength > 0:
        # Repeats letters of the key stream until the key stream is
        # as long as the plain text if the key stream is shorter than the plain text.
        AddedLength = NeededLength - KeyLength
        for i in range(AddedLength):
            KeyStream += KeyWord[i%KeyLength]
    else:
        # Repeats the last letter of the plain text until it is as long as the key stream if the key stream is longer
        # than the plain text. If it is the same length, the for loop will end immediately.
        for i in range(AddedLength):
            KeyStream += KeyWord[-1]

    return KeyStream

# From hereon code for ciphering

def get_cipher_letter(VigenereTable, ReferenceDict, KeyLetter, PlainLetter):
    # determines the ciphered letter by its proper row (derived from the key letter)
    # and the column (derived from the plain text letter) from the Vigenère table.
    Row = ReferenceDict[KeyLetter]
    Column = ReferenceDict[PlainLetter]
    CipherLetter = VigenereTable[Row][Column]

    return CipherLetter

def generate_cipher(Alphabet, VigenereTable, ReferenceDict, KeyWord, PlainText):
    # Generates the actual cipher by combining the ciphering functions together.
    KeyStream = make_keystream(KeyWord, PlainText)
    Cipher = ""

    for i in range(len(PlainText)):
        Cipher += get_cipher_letter(VigenereTable, ReferenceDict, KeyStream[i], PlainText[i])
    # Generates each cipher letter and adds it to the cipher.

    return Cipher

def cipher(Alphabet, KeyWord, PlainText): # Just for organization.
    Alphabet = Alphabet.upper()
    KeyWord = KeyWord.upper()
    PlainText = PlainText.replace(" ", "").upper()
    # ▲ Remove the replace statement if you are using spaces as a letter in your alphabet.
    ReferenceDict = generate_letter_reference_dict(Alphabet)
    VigenereTable = generate_vigenere_table(Alphabet)
    Cipher = generate_cipher(Alphabet, VigenereTable, ReferenceDict, KeyWord, PlainText)
    return Cipher

# From hereon code for deciphering

def get_decipher_letter(VigenereTable, ReferenceDict, KeyLetter, CipherLetter):
    # Gets the deciphered letter by checking what column has the
    # Ciphered letter in the row of the respective letter of the key.
    Row = ReferenceDict[KeyLetter]
    Index = VigenereTable[Row].index(CipherLetter)
    ReversedReferenceDict = lambda ReferenceDict: {v:k for k, v in ReferenceDict.items()}
    # ▲ Reverses reference dictionary so numbers refer to letters and not the other way.
    DecipheredLetter = ReversedReferenceDict(ReferenceDict)[Index]
    # ▲ Finds the deciphered letter in the dictionary.
    return DecipheredLetter

def decipher(Alphabet, KeyWord, Cipher):
    # Generates the deciphered text.
    Alphabet = Alphabet.upper()
    KeyWord = KeyWord.upper()
    Cipher = Cipher.upper()
    ReferenceDict = generate_letter_reference_dict(Alphabet)
    VigenereTable = generate_vigenere_table(Alphabet)
    KeyStream = make_keystream(KeyWord, Cipher)
    DecipheredText = ""

    for i in range(len(Cipher)):
        DecipheredText += get_decipher_letter(VigenereTable, ReferenceDict, KeyStream[i], Cipher[i])
    # ▲ Adds the letters to the deciphered text.
    return DecipheredText


# Example & How to:

Alphabet = "abcdefghijklmnopqrstuvwxyz" # 1: Make Alphabet Character
KeyedAlphabetWord = "Plane" # OPTIONAL 1: Make a word for your keyed alphabet
KeyedAlphabet = keyed_alphabet_generator(Alphabet, KeyedAlphabetWord) # OPTIONAL 2: Generate Keyed Alphabet
KeyWord = "FEAST" # 2: Make your key word
PlainText = "Lorem ipsum dolor sit amet consectetur adipiscing elit Nullam finibus lectus a urna consequat" \
            " ac vestibulum magna tristique" # 3: Make plain text

print_vigenere_table(Alphabet, generate_vigenere_table(Alphabet))
# Print Vigenere table here for demonstration, replace Alphabet parameter with KeyedAlphabet if using a keyed alphabet.

print(f"Plain Text: {PlainText}")
Cipher = cipher(Alphabet, KeyWord, PlainText) # 4: Feed parameters into functions.
print(f"Cipher: {Cipher}")
DecipheredText = decipher(Alphabet, KeyWord, Cipher) # 4: Feed parameters into functions.
print(f"Deciphered Text: {DecipheredText}")