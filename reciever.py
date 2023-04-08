import socket
import decryption_functions
import common_functions
import generate_key

myReceiver = decryption_functions.Receiver()


def reciever_program():

    print("Generate p,q.... \n")

    # generate two prime numbers: p, q
    p, q = common_functions.gererate_pq_primes()

    # Print the values of p and q
    print("p:", p)
    print("q:", q)

    print("Generation done! \n")

    print("Generate e.... \n")
    e = generate_key.generate_e((p-1) * (q-1))
    print("Generation done! \n")

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the sender

    myReceiver.p = int(p)
    myReceiver.q = int(q)
    myReceiver.e = int(e)

    # calculate n
    myReceiver.n = myReceiver.p*myReceiver.q

    print('sending public... \n')
    # send the public key(e, n) to the sender
    public_key = str(myReceiver.e) + " " + str(myReceiver.n)
    client_socket.send(str(public_key).encode())  

    print('sending public key is done. \n')

    while True:
        print('waiting for message...')
        C = client_socket.recv(1024).decode()  # receive cipher from sender

        print('cipher text received: ' + C)  # show in terminal
        decryptedMessage = myReceiver.decryption(C)
        print("original message from sender: ", decryptedMessage)
        client_socket.send(str("Decryption Done!").encode())

    client_socket.close()  # close the connection


if __name__ == '__main__':
    reciever_program()
