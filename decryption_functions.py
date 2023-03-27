import numpy as np
import encryption_functions
import math


def mod_inverse_solve(a, n):
    (b, x) = extended_euclidean_algo(a, n)
    if b < 0:
        b = (b % n + n) % n  # get rid of -ve numbers
    return b


def extended_euclidean_algo(a, b):
    if b == 0:
        return (1, 0)
    (x, y) = extended_euclidean_algo(b, a % b)
    k = a // b
    return (y, x - k * y)


def decryption(cipherText, p, q, e):

    # phi_n = (p-1)*(q-1)
    # d = mod_inverse_solve(e,   phi_n)

    splited_message = encryption_functions.splitToGroups(cipherText)
    # print(splited_message)
    c_list = encryption_functions.convertToInt(splited_message)
    # print('int c = ', c_list)

    # m = encryption_functions.power_mod_solve(c,  math.floor(d), p * q)
    decryptedMessage = ''
    for c in c_list:
        # m = pow(c, d) % (p*q) #commenttttttt
        # decryptedMessage = decryptedMessage + encryption_functions.convertToString(m) 
        decryptedMessage = decryptedMessage + encryption_functions.convertToString(c) 
    # print('before convert to string encryption:', m)
    # print(m)
    # decryptedMessage = encryption_functions.convertToString(m) # commenntttt
    # print('string m = ', decryptedMessage)
    # decryptedMessage = m
    return decryptedMessage
