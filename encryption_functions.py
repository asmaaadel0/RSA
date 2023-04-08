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

    def encryption(self, message):
        # split the message to groups
        splited_message = common_functions.splitToGroups(message)
        #encode the groups, convert them to integer
        m = common_functions.convertToInt(splited_message)
        cipherText = ''
        # caluclate the cipher Text
        for i in m:
            c = pow(int(i), self.e, self.n)
            cipherText = cipherText + ' ' + str(c)
        cipherText = cipherText[1:]        
        return cipherText
