import string
from numpy import matmul
import numpy
from numpy.lib import math
from sympy import Matrix
from sympy.logic.boolalg import Xnor

# General Functions

def to_number(c):
    if (c.isdigit()):
        return int(c)
    else:
        assert (c in string.ascii_letters)
        return ord(c.lower()) - ord('a')

def to_numberArray(letters):
    numberArray = []
    for i in range(len(letters)):
        numberArray.append(to_number(letters[i]))
    return numberArray

def to_letter(i):
    return chr(i + ord('a'))

def to_letterArray(numbers):
    letterArray = []
    for i in range(len(numbers)):
        letterArray.append(to_letter(numbers[i]))
    return letterArray

def shift(s, key):
    return "".join(to_letter((to_number(c) + key) % 26) for c in s)

def letter_freqs(s):
    return [(c, s.count(c)) for c in string.ascii_letters if c in s]

def sort_freqs(s):
    frequencies = [(c, s.count(c)) for c in string.ascii_letters if c in s]
    lst = len(frequencies)  
    for i in range(0, lst):  
        for j in range(0, lst - i - 1):
            if (frequencies[j][1] < frequencies[j + 1][1]):  
                temp = frequencies[j]  
                frequencies[j] = frequencies[j + 1]
                frequencies[j + 1]= temp  
    return frequencies  

def every_kth_letter(s, k, offset):
    return "".join(c for i, c in enumerate(s) if i % k == offset)

def vigenere(s, k):
    return "".join(shift(c, to_number(k[i % len(k)])) for i, c in enumerate(s))

def coincidences(s, shift):
    return len([x for i, x in enumerate(s) if i + shift < len(s) and x == s[i + shift]])

def gcd(a, b):
    if b == 0:
        return a
    else:
        remainder = a % b
        return gcd(b, remainder)

def gcdLinearCombination(a, b):
    remainderLast = a
    remainder = b
    xLast = 1
    yLast = 0
    x = 0
    y = 1
    while remainder > 0:
        tempRemainderLast = remainderLast
        remainderLast = remainder
        quotient = tempRemainderLast // remainderLast
        remainder = tempRemainderLast % remainderLast
        tempX = x
        x = xLast - quotient * x
        xLast = tempX
        tempY = y
        y = yLast - quotient * y
        yLast = tempY
    return [remainderLast, xLast, yLast]

def modularInverse(a, m):
    linearCombination = gcdLinearCombination(a, m)
    gcd = linearCombination[0]
    x = linearCombination[1]
    if gcd != 1:
        return "DNE"
    return x % m

def stringToMatrix(stringArray, value): #given [h,e,l,l,o], 2 return [[h,e], [l,l], [o]]
    fill = (math.ceil(len(stringArray) / value) * value) - len(stringArray)
    for i in range(fill):
        stringArray.append('')
    return numpy.reshape(stringArray, (math.ceil(len(stringArray)/value), value))

S1 = [(1,0,1), (0,1,0), (0,0,1), (1,1,0), (0,1,1), (1,0,0), (1,1,1), (0,0,0), (0,0,1), (1,0,0), (1,1,0), (0,1,0), (0,0,0), (1,1,1), (1,0,1), (0,1,1)]
S2 = [(1,0,0), (0,0,0), (1,1,0), (1,0,1), (1,1,1), (0,0,1), (0,1,1), (0,1,0), (1,0,1), (0,1,1), (0,0,0), (1,1,1), (1,1,0), (0,1,0), (0,0,1), (1,0,0)]

def round_key(k, i):
    assert len(k) == 9
    return tuple (k[(i+j-1) % 9] for j in range(8))

def tuple_xor(s, t):
    assert len(s) == len(t)
    return tuple(x^y for (x,y) in zip(s,t))

def expander(r):
    return (r[0], r[1], r[3], r[2], r[3], r[2], r[4], r[5])

def encrypt_affine(text, key):
    return ''.join([ chr((( key[0]*(ord(t) - ord('A')) + key[1] ) % 26)  
                  + ord('A')) for t in text.upper().replace(' ', '') ]) 

def decrypt_affine(cipher, key):
    return ''.join([ chr((( modularInverse(key[0], 26)*(ord(c) - ord('A') - key[1]))  
                    % 26) + ord('A')) for c in cipher ])

def encrypt_vigenere(text, key):
    cipher_text = []
    blockKey = []
    for i in range(len(text)):
        blockKey.append(key[i % len(key)]) 
    for i in range(len(text)): 
        x = (ord(text[i]) + ord(blockKey[i])) % 26
        x += ord('A') 
        cipher_text.append(chr(x)) 
    return("" . join(cipher_text)) 

def decrypt_vigenere(cipher, key):
    orig_text = []
    blockKey = []
    for i in range(len(cipher)):
        blockKey.append(key[i % len(key)])  
    for i in range(len(cipher)): 
        x = (ord(cipher[i]) - ord(blockKey[i]) + 26) % 26
        x += ord('A') 
        orig_text.append(chr(x)) 
    return("" . join(orig_text)) 

def encrypt_hill(text, key, mod):
    key = numpy.array(key)
    text = numpy.array(to_numberArray(text))
    blockLength = len(key[0])
    passes = math.ceil(len(text) / blockLength)
    for i in range((passes * blockLength) - len(text)):
        text = numpy.append(text, [0])
    cipher = []
    for i in range(passes):
        textBlock = text[i * blockLength:(i + 1) * blockLength]
        cipherBlock = numpy.matmul(textBlock, key)
        cipherBlock = cipherBlock % mod
        if (mod == 2):
            cipherBlock = [str(z) for z in cipherBlock]
        else:
            cipherBlock = to_letterArray(cipherBlock)
        for j in range(len(cipherBlock)):
            cipher.append(cipherBlock[j]) 
    return (''.join(cipher))

def decrypt_hill(cipher, key, mod):
    key = numpy.array(key)
    inverse_key = Matrix(key).inv_mod(mod)
    inverse_key = numpy.array(inverse_key)
    cipher = numpy.array(to_numberArray(cipher))
    blockLength = len(key[0]) 
    passes = math.ceil(len(cipher) / blockLength)
    for i in range((passes * blockLength) - len(cipher)):
        cipher = numpy.append(cipher, [0])
    text = []
    for i in range(passes):
        cipherBlock = cipher[i * blockLength:(i + 1) * blockLength]
        textBlock = numpy.matmul(cipherBlock, inverse_key)
        textBlock = textBlock % mod
        if (mod == 2):
            textBlock = [str(z) for z in textBlock]
        else:
            textBlock = to_letterArray(textBlock)
        for j in range(len(textBlock)):
            text.append(textBlock[j]) 
    return (''.join(text))

def sdes_f(r, ki):
    e = expander(r)
    ek = tuple_xor(e, ki)
    left_ek_idx = int("".join(str(x) for x in ek[0:4]), 2)
    right_ek_idx = int("".join(str(x) for x in ek[4:8]), 2)
    left_cipher = S1[left_ek_idx]
    right_cipher = S2[right_ek_idx]
    return left_cipher + right_cipher

def do_des(plain, key, num_rounds, decrypt=False):
    L = tuple(int(x) for x in plain[0:6])
    R = tuple(int(x) for x in plain[6:12])
    k = tuple(int(x) for x in key)

    round_order = list(range(1, num_rounds + 1))
    assert len(round_order) == num_rounds

    if decrypt:
        (L, R) = (R, L)
        round_order.reverse()

    for i in round_order:
        Lnew = R
        ki = round_key(k, i)
        Rnew = tuple_xor(L, sdes_f(R, ki))
        (L, R) = (Lnew, Rnew)

    if decrypt:
        (L, R) = (R, L)

    return "".join(str(x) for x in L) + "".join(str(x) for x in R)