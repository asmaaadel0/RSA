import common_functions


class Receiver:
    p = 0,
    q = 0,
    n = 0,
    e = 0,
    phi_n = 0,
    d = 0
    key_computed = False

    # compute private key(d, n)
    def compute_private_key(self):
        self.phi_n = (self.p-1)*(self.q-1)
        self.d = common_functions.mod_inverse_solve(self.e,   self.phi_n)

    def decryption(self, c):
        # compute private key(d, n)
        if(self.key_computed == False):
            self.compute_private_key()
            self.key_computed = True

        m = pow(int(c), self.d, (self.n))
        decryptedM = common_functions.convertToString(m)
        return decryptedM
