from Tools import *

# Cryptography Attacks

# Shift Cipher using frequency analysis with multiple steps to guess 'e' with frequency analysis. Will print out 'steps' potential plaintexts.
# ETAOIN are most common characters.
def shiftCipherFrequencyAttack(code, steps, plaintextGuess):
    frequencies = sort_freqs(code)
    for i in range(steps):
        mostCommonChar = frequencies[i][0]
        shiftValue = -(to_number(mostCommonChar) - to_number(plaintextGuess))
        plaintext = shift(code, shiftValue)
        print("Shift of " + str(-(shiftValue)) + ": " + plaintext)


