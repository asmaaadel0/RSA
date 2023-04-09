import socket
import encryption_functions
import decryption_functions
import common_functions
import generate_key

mySender = encryption_functions.Sender()
myReceiver = decryption_functions.Receiver()

def reciever_program():

    

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the sender

    print("Generate p,q.... \n")

    # generate two prime numbers: p, q
    p, q = common_functions.gererate_pq_primes()

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

    print('recieving public...')
    # receive the public key(e, n) from reciever 
    public_key = client_socket.recv(1024).decode()
    public_key = public_key.split(" ")

    e = int(public_key[0])
    n = int(public_key[1])

    print('recieving public key is done.')

    print('sending public...')
    # send the public key(e, n) to the sender
    public_key = str(myReceiver.e) + " " + str(myReceiver.n)
    client_socket.send(str(public_key).encode())  
    print('sending public key is done.')


    mySender.set_public_key(e, n)
    while True:
        print('waiting for message...')
        C = client_socket.recv(1024).decode()  # receive cipher from sender

        print('cipher text received: ' + C)  # show in terminal
        decryptedMessage = myReceiver.decryption(C)
        print("original message from sender: ", decryptedMessage)
        client_socket.send(str("Decryption Done!").encode())


        message = input(' enter message -> ')
        C = mySender.encryption(message)
        client_socket.send(C.encode())  # send data to the client
        print(client_socket.recv(1024).decode())

    client_socket.close()  # close the connection


if __name__ == '__main__':
    reciever_program()
