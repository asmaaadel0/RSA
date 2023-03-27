import numpy as np
import common_functions


class Receiver:
    p = 0,
    q = 0,
    e = 0,
    phi_n = 0,
    d = 0

    def compute_private_key(self):
        self.phi_n = (self.p-1)*(self.q-1)
        # d = e^-1 mod phi(n)
        self.d = common_functions.mod_inverse_solve(self.e,   self.phi_n)

    def send_public_key(self):
        return self.e

    def decryption(self, cipherText):

        self.compute_private_key()
        cipherText = cipherText.split(" ")
        del cipherText[0]
        # ct = cipherText
        # splited_message = encryption_functions.splitToGroups(cipherText)
        # print(splited_message)
        # c_list = encryption_functions.convertToInt(splited_message)
        # print('int c = ', c_list)

        # m = encryption_functions.power_mod_solve(c,  math.floor(d), p * q)
        decryptedMessage = ''
        for c in cipherText:
            # print('cipher ', cipherText)
            m = pow(int(c), self.d) % (self.p*self.q)  # commenttttttt
            print(cipherText)
            # m = pow(int(ct), d) % (p*q) #commenttttttt
            print('m = ', m, 'c = ', c)
            decryptedMessage = decryptedMessage + \
                common_functions.convertToString(m)
            # decryptedMessage = decryptedMessage + encryption_functions.convertToString(c)
        # print('before convert to string encryption:', m)
        # print(m)
        # decryptedMessage = encryption_functions.convertToString(m) # commenntttt
        # print('string m = ', decryptedMessage)
        # decryptedMessage = m
        return decryptedMessage
