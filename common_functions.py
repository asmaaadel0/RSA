import numpy as np
import random
import sympy
import generate_key

# split message to groups each group in 5 chars, if it's not, add spaces


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

# encoding each group convert it to integer


def convertToInt(splited_message):
    numbers = []
    for group in splited_message:
        plaintext_number = 0
        number = 0
        i = 4
        for char in group:
            if (ord(char) in range(47, 58)):
                number = ord(char) - 48
            elif (ord(char) in range(97, 123)):
                number = ord(char) - 87
            else:
                number = 36
            plaintext_number = plaintext_number + 37**i * number
            i = i - 1
        numbers.append(plaintext_number)
    return numbers

# decoding the integer groups convert it back to string


def convertToString(number):
    string = ''
    char = ''
    while number > 0:
        if (pow(number, 1, 37) in range(0, 10)):
            char = str(pow(number, 1, 37))
        elif (pow(number, 1, 37) in range(10, 36)):
            char = chr(pow(number, 1, 37) + 87)
        else:
            char = chr(32)
        number //= 37
        string += char
    return string[::-1]

# to calculate inverse of e (d)


def mod_inverse_solve(a, n):
    (b, x) = extended_euclidean_algo(a, n)
    if b < 0:
        b = pow((pow(b, 1, n) + n), 1, n)   # get rid of -ve numbers
    return b


def extended_euclidean_algo(a, b):
    if b == 0:
        return (1, 0)
    (x, y) = extended_euclidean_algo(b, pow(a, 1, b))
    k = a // b
    return (y, x - k * y)

# prime factorization, generate p, q from n for attack


def generate_pq(n):
    p = random.getrandbits(int(n/2))
    q = random.getrandbits(int(n/2))
    while not sympy.isprime(p):
        p = random.getrandbits(int(n/2))
    while not sympy.isprime(q) or p == q:
        q = random.getrandbits(int(n/2))
    return p, q

# generate p, q primes numbers


def gererate_pq_primes():
    # any range, I choose this!
    p = sympy.randprime((20000), (200000))
    while True:
        # q = sympy.randprime(2**(2047), 2**(20048)-1)
        q = sympy.randprime((20000), (200000))
        if p != q:
            break
    return p, q

def configReceiving(myReceiver, conn):
    print("Generate p,q....")

    # generate two prime numbers: p, q
    p, q = gererate_pq_primes()

    # Print the values of p and q
    print("p:", p)
    print("q:", q)

    print("Generation done!")

    print("Generate e....")
    e = generate_key.generate_e((p-1) * (q-1))
    print("Generation done!")

    myReceiver.p = int(p)
    myReceiver.q = int(q)
    myReceiver.e = int(e)
    # calculate n
    myReceiver.n = myReceiver.p*myReceiver.q



    print('sending public...')
    # send the public key(e, n) to the sender
    public_key_1 = str(myReceiver.e) + " " + str(myReceiver.n)
    conn.send(str(public_key_1).encode()) 
    print('sending public key is done.')

def configSending(mySender, client_socket):
    print('recieving public...')
    # receive the public key(e, n) from reciever 
    public_key = client_socket.recv(1024).decode()
    public_key = public_key.split(" ")

    e = int(public_key[0])
    n = int(public_key[1])

    print('recieving public key is done.')
    mySender.set_public_key(e, n)  

def sendMessage(mySender, client_socket):
        message = input(' enter message -> ')
        C = mySender.encryption(message)
        client_socket.send(C.encode())  # send data to the client
        print(client_socket.recv(1024).decode())

def receiveMessage(myReceiver, conn):
        print('waiting for message...')
        C = conn.recv(1024).decode()  # receive cipher from sender

        print('cipher text received: ' + C)  # show in terminal
        decryptedMessage = myReceiver.decryption(C)
        print("original message from sender: ", decryptedMessage)
        conn.send(str("Decryption Done!").encode())        