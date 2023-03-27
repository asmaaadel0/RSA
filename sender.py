import socket
import encryption_functions


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

    # j = 0
    # p = 19
    # q = 17
    # e = 7
    # while j < 3:
    #     s_messg = conn.recv(1024).decode()
    #     print(s_messg)
    #     if j == 0:
    #         p = int(s_messg)
    #     if j == 1:
    #         q = int(s_messg)
    #     if j == 2:
    #         e = int(s_messg)
    #     j += 1

      
    # p = int(input(' enter p -> '))
    # q = int(input(' enter q -> '))
    # e = int(input(' enter e -> '))
    p = 17
    q = 11
    e = 7

    conn.send(str(p).encode())  # send data to the client
    conn.send(str(q).encode())  # send data to the client
    conn.send(str(e).encode())  # send data to the client



    # print(p, q, e)  
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        # data = conn.recv(1024).decode()
        # if not data:
        # if data is not received break
        # break
        # print("from connected user: " + str(data))
        message = input(' enter message -> ')
        C = encryption_functions.encryption(message, p, q, e)
        conn.send(C.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    sender_program()
