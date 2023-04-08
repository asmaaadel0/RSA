import numpy as np
import common_functions


class Receiver:
    p = 0,
    q = 0,
    n = 0,
    e = 0,
    phi_n = 0,
    d = 0

    def compute_private_key(self):
        self.phi_n = (self.p-1)*(self.q-1)
        self.d = common_functions.mod_inverse_solve(self.e,   self.phi_n)

    def send_public_key(self):
        return self.e

    def decryption(self, cipherText):

        self.compute_private_key()
        cipherText = cipherText.split(" ")

        self.n = self.p*self.q
        decryptedMessage = ''
        for c in cipherText:
            m = pow(int(c), self.d, (self.n))
            decryptedMessage = decryptedMessage + \
                common_functions.convertToString(m)
        return decryptedMessage
