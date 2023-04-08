import socket
import decryption_functions
import sympy
import generate_key
import time
import random

myReceiver = decryption_functions.Receiver()


def reciever_program():


    print("Generate p,q.... \n")
    p = sympy.randprime((2047), (20048)-1)
    while True:
        q = sympy.randprime((2047), (20048)-1)
        if p != q:
            break

    # Print the values of p and q
    print("p:", p)
    print("q:", q)

    # p = 40351
    # q = 42323
    # e = 3823

    print("Generation done! \n")

    e = generate_key.generate_e((p-1) * (q-1))

    print("public key is validated you can start the communication .. ")
    print(p, q, e)

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    # client_socket.send(str(p).encode())  # send data to the client
    myReceiver.p = int(p)
    # time.sleep(1)

    # client_socket.send(str(q).encode())  # send data to the client
    myReceiver.q = int(q)
    # time.sleep(1)

    client_socket.send(str(e).encode())  # send data to the client
    myReceiver.e = int(e)
    time.sleep(1)

    client_socket.send(str(p*q).encode())  # send data to the client

    print('sending public key is done.')

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
