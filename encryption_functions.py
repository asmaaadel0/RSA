import numpy as np


def splitToGroups(message):
    splited_message = []
    for i in range(0, len(message), 5):
        splited_message.append(message[i:i+5].lower())
    if (len(splited_message[-1]) != 5):
        end = splited_message[-1]
        for i in range(len(splited_message[-1]), 5):
            end = end + ' '
        splited_message[-1] = end
    splited_message = np.asarray(splited_message)
    return splited_message


def convertToInt(splited_message):
    numbers = []
    for group in splited_message:
        plaintext_number = 0
        number = 0
        i = 4
        for char in group:
            if (ord(char) in range(48, 57)):
                number = ord(char) - 48
            elif (ord(char) in range(97, 122)):
                number = ord(char) - 87
            else:
                number = 36
            plaintext_number = plaintext_number + 37**i * number
            i = i - 1
        numbers.append(plaintext_number)
    return numbers[0]


def convertToString(number):
    string = ''
    char = ''
    while number > 0:
        if (number % 37 in range(0, 9)):
            char = str(number % 37)
        elif (number % 37 in range(10, 35)):
            char = chr(number % 37 + 87)
        else:
            char = chr(32)
        number //= 37
        string += char
    return string[::-1]


def power_mod_solve(m, e, n):
    if e == 0:
        return 1 % n
    elif e == 1:
        return m % n
    else:
        b = power_mod_solve(m, e // 2, n)
        b = b * b % n
    if e % 2 == 0:
        return b
    else:
        return b * e % n


def encryption(message, p, q, e):
    splited_message = splitToGroups(message)
    m = convertToInt(splited_message)
    print(m)
    c = power_mod_solve(m, e, p * q)
    print(c)
    cipherText = convertToString(c)
    return cipherText
