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
        # print(group)
        for char in group:
            # print('ord(char)', ord(char))
            if (ord(char) == 48):
                number = 37 #should be removed
            elif (ord(char) in range(47, 58)):
                number = ord(char) - 48
                # print('number', number)
            elif (ord(char) in range(97, 123)):
                number = ord(char) - 87
                # print('number = ', number)
            else:
                number = 36
            plaintext_number = plaintext_number + 38**i * number #should be 37
            i = i - 1
        numbers.append(plaintext_number)
        # print('numbers = ', numbers)
    return numbers


def convertToString(number):
    string = ''
    char = ''
    while number > 0:
        if (number % 38 == 37):
            char = str(0) #should be removed
        elif (number % 38 in range(0, 10)): #should be 37
            char = str(number % 38) #should be 37
            # print('number = ', char)
        elif (number % 38 in range(10, 36)): #should be 37
            char = chr(number % 38 + 87) #should be 37
        else:
            char = chr(32)
        number //= 38 #should be 37
        string += char
        # print('string = ', string[::-1])
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
    cipherText = ''
    for i in m:
        # c = pow(int(i), e) % (p*q) # commenntttt
        # j = convertToString(c) # commenntttt
        # print(i)
        j = convertToString(i)
        print(j)
        cipherText = cipherText + j
    # print('int m = ', m)
    # print('convertToInt encryption', m)
    # c = power_mod_solve(m, e, p * q)

    # c = pow(m, e) % (p*q) # commenntttt
    # print('before convert to string encryption:', c)
    # cipherText = convertToString(c) # commenntttt
    # print('string c= ', cipherText)

    # print(cipherText)
    # print(cipherText)
    # cipherText = c
    return cipherText
