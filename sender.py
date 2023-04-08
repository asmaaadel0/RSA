import socket
import encryption_functions
import decryption_functions
import common_functions
import generate_key

mySender = encryption_functions.Sender()
myReceiver = decryption_functions.Receiver()

def sender_program():

    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    print("Generate p,q....")

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



    print('sending public...')
    # send the public key(e, n) to the sender
    public_key_1 = str(myReceiver.e) + " " + str(myReceiver.n)
    conn.send(str(public_key_1).encode()) 
    print('sending public key is done.', public_key_1)

    # receive the public key(e, n) from reciever 
    public_key = conn.recv(1024).decode()
    public_key = public_key.split(" ")

    e = int(public_key[0])
    n = int(public_key[1])

    print('recieving public key is done.')
    mySender.set_public_key(e, n)

    while True:
        message = input(' enter message -> ')

        splited_message = common_functions.splitToGroups(message)
        m = common_functions.convertToInt(splited_message)
        while (max(m) > n):
            print("max allowed length of message is only ")
            message = input("-> ")
            splited_message = common_functions.splitToGroups(message)
            m = common_functions.convertToInt(splited_message)
        C = mySender.encryption(message)
        conn.send(C.encode())  # send data to the client
        print(conn.recv(1024).decode())

        print('waiting for message...')
        C = conn.recv(1024).decode()  # receive cipher from sender

        print('cipher text received: ' + C)  # show in terminal
        decryptedMessage = myReceiver.decryption(C)
        print("original message from sender: ", decryptedMessage)
        conn.send(str("Decryption Done!").encode())

    conn.close()  # close the connection


if __name__ == '__main__':
    sender_program()
