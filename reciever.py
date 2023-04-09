import socket
import encryption_functions
import decryption_functions
import common_functions

mySender = encryption_functions.Sender()
myReceiver = decryption_functions.Receiver()

def reciever_program():

    

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the sender

    common_functions.configSending(mySender, client_socket)

    common_functions.configReceiving(myReceiver, client_socket)

    while True:
        
        common_functions.receiveMessage(myReceiver, client_socket)

        common_functions.sendMessage(mySender, client_socket)


    client_socket.close()  # close the connection


if __name__ == '__main__':
    reciever_program()
