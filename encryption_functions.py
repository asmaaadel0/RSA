import numpy as np
import common_functions


class Sender:

    # public key
    e = 0,
    n = 0,
    # functions

    def set_public_key(self, e, n):
        self.e = e
        self.n = n

    def encryption(self, message):
        splited_message = common_functions.splitToGroups(message)
        m = common_functions.convertToInt(splited_message)
        cipherText = ''
        for i in m:
            c = pow(int(i), self.e, self.n)
            print('m = ', i, 'c = ', c)
            cipherText = cipherText + ' ' + str(c)
        return cipherText
