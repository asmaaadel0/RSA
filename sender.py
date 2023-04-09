import socket
import encryption_functions
import decryption_functions
import common_functions

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

    common_functions.configReceiving(myReceiver, conn)

    common_functions.configSending(mySender, conn)

    while True:
        
        common_functions.sendMessage(mySender, conn)

        common_functions.receiveMessage(myReceiver, conn)


    conn.close()  # close the connection


if __name__ == '__main__':
    sender_program()
