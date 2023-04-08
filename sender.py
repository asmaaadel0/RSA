import socket
import encryption_functions
import common_functions

mySender = encryption_functions.Sender()


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

    e = int(conn.recv(1024).decode())  # receive response
    n = int(conn.recv(1024).decode())  # receive response

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

    conn.close()  # close the connection


if __name__ == '__main__':
    sender_program()
