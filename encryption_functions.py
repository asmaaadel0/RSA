import common_functions


class Sender:

    # public key
    e = 0,
    n = 0,
    # functions

    # set public key(e, n)
    def set_public_key(self, e, n):
        self.e = e
        self.n = n

    def encryption(self, packet):
        c = pow(int(packet), self.e, self.n)     
        return c
