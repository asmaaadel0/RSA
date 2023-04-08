import common_functions


class Receiver:
    p = 0,
    q = 0,
    n = 0,
    e = 0,
    phi_n = 0,
    d = 0

    # compute private key(d, n)
    def compute_private_key(self):
        self.phi_n = (self.p-1)*(self.q-1)
        self.d = common_functions.mod_inverse_solve(self.e,   self.phi_n)

    def decryption(self, cipherText):
        # compute private key(d, n)
        self.compute_private_key()

        # the cipherText will be a list as string splited with " "
        cipherText = cipherText.split(" ")

        decryptedMessage = ''
        # calculate decrypted Message
        for c in cipherText:
            m = pow(int(c), self.d, (self.n))
            decryptedMessage = decryptedMessage + \
                common_functions.convertToString(m)
        return decryptedMessage
