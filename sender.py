import socket
import numpy as np
def splitToGroups(message):
    splited_message = []
    for i in range(0,len(message),5):
      splited_message.append(message[i:i+5].lower())
    if(len(splited_message[-1]) != 5):
        end = splited_message[-1]
        for i in range(len(splited_message[-1]), 5):
            end = end + ' '
        splited_message[-1] = end    
    splited_message = np.asarray(splited_message)
    return splited_message  

def convertToInt(splited_message):
    numbers = []
    for group in splited_message:
        plaintext_number = 0
        number = 0
        i = 4
        for char in group:
            if(ord(char) in range(48, 57)):
              number = ord(char) - 48
            elif(ord(char) in range(97, 122)):
              number = ord(char) - 87
            else:
              number = 36
            plaintext_number = plaintext_number + 37**i * number
            i = i - 1
        numbers.append(plaintext_number)
    return numbers    
    

def encryption(message):
    splited_message = splitToGroups(message)
    converted_message = convertToInt(splited_message)
    return message

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
    while True:
        data = input(' -> ')
        # receive data stream. it won't accept data packet greater than 1024 bytes
        # data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        # print("from connected reciever: " + str(data))
        # data = input(' -> ')
        data = encryption(data)
        conn.send(data.encode())  # send data to the reciever

    conn.close()  # close the connection


if __name__ == '__main__':
    sender_program()