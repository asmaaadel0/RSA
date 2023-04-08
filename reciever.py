import socket
import decryption_functions
import common_functions
import generate_key
import time

myReceiver = decryption_functions.Receiver()


def reciever_program():


    print("Generate p,q.... \n")

    p, q = common_functions.gererate_pq_primes();

    # Print the values of p and q
    print("p:", p)
    print("q:", q)

    # p = 40351
    # q = 42323
    # e = 3823

    print("Generation done! \n")

    print("Generate e.... \n")
    e = generate_key.generate_e((p-1) * (q-1))
    print("Generation done! \n")

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    myReceiver.p = int(p)
    myReceiver.q = int(q)

    print('sending public...')
    client_socket.send(str(e).encode())  # send data to the client
    myReceiver.e = int(e)
    time.sleep(1)

    client_socket.send(str(p*q).encode())  # send data to the client

    print('sending public key is done.')

    while True:
        print('waiting for message...')
        # client_socket.send(message.encode())  # send message
        C = client_socket.recv(1024).decode()  # receive response

        print('cipher text received: ' + C)  # show in terminal
        decryptedMessage = myReceiver.decryption(C)
        print("original message from sender: ", decryptedMessage)

    client_socket.close()  # close the connection


if __name__ == '__main__':
    reciever_program()
