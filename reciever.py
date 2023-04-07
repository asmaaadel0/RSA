import socket
import decryption_functions
import sympy
import generate_key
import time

myReceiver = decryption_functions.Receiver()


def reciever_program():

    # test_file = open("test_cases.txt", "r")
    # lines = test_file.read().splitlines()
    # i = 0
    # e = ""
    # while i < len(lines)-1:
    #     # read the message and the public key
    #     if lines[i] != "" or lines[i] != " ":
    #         p = int(lines[i])
    #     if lines[i+1] != "" or lines[i] != " ":
    #         q = int(lines[i+1])
    #     if (i+2) <= (len(lines)-1):
    #         e = lines[i+2]
    #     i += 3
    # test_file.close()  # close the file

    p = int(input(' enter p -> '))
    q = int(input(' enter q -> '))

    p = 6353
    q = 8641
    # e = 3823

    print("Validate p,q.... \n")

    # check that p and q are primes
    if not sympy.isprime(p):
        print(" p must be prime")
        exit()

    if not sympy.isprime(q):
        print(" q must be prime")
        exit()

    e = generate_key.generate_e((p-1) * (q-1))

    print("public key is validated you can start the communication .. ")
    print(p, q, e)

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    time.sleep(1)

    client_socket.send(str(p).encode())  # send data to the client
    myReceiver.p = int(p)
    time.sleep(1)

    client_socket.send(str(q).encode())  # send data to the client
    myReceiver.q = int(q)
    time.sleep(1)

    client_socket.send(str(e).encode())  # send data to the client
    myReceiver.e = int(e)

    print('sending p, q done.')

    while True:
        # client_socket.send(message.encode())  # send message
        C = client_socket.recv(1024).decode()  # receive response

        print('cipher text received: ' + C)  # show in terminal
        decryptedMessage = myReceiver.decryption(C)
        print("original message from sender: ", decryptedMessage)

        # message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    reciever_program()
