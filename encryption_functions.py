import numpy as np
import common_functions


class Sender:
    # public key
    p = 0,
    q = 0,
    e = 0,
    # functions

    def set_public_key(self, p, q, e):
        self.p = p
        self.q = q
        self.e = e

    def encryption(self, message):
        splited_message = common_functions.splitToGroups(message)
        m = common_functions.convertToInt(splited_message)
        cipherText = ''
        for i in m:
            c = pow(int(i), self.e) % (self.p * self.q)  # commenntttt
            print('m = ', i, 'c = ', c)
            # c = pow(10, e) % (p*q)
            # j = convertToString(c) # commenntttt
            # print(i)
            # j = convertToString(c)
            cipherText = cipherText + ' ' + str(c)
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
        # return str(c)
        return cipherText
