import socket
import generate_key


def reciever_program():

    # test_file = open("test_cases.txt", "r")
    # lines = test_file.read().splitlines()
    # i = 0
    # e = ""
    # while i < len(lines)-1:
    #     # read the message and the public key
    #     if lines[i] != "" or lines[i] != " ":
    #         p = int(lines[i])
    #     if lines[i+1] != "" or lines[i] != " ":
    #         q = int(lines[i+1])
    #     if (i+2) <= (len(lines)-1):
    #         e = lines[i+2]
    #     i += 3
    # test_file.close()  # close the file

    print("Validate p,q.... \n")

    # p = 19
    # q = 17
    # e = 7

    # check that p and q are primes
    # if not generate_key.isPrime(p):
    #     print(" p must be prime")
    #     exit()

    # if not generate_key.isPrime(q):
    #     print(" q must be prime")
    #     exit()

    # generate public key e if not given
    # if e == "" or e == " ":
    #     e = generate_key.generate_e((p-1) * (q-1))
    # else:
    #     e = int(e)
    #     if not (generate_key.validate_e(e, (p-1) * (q-1))):
    #         print(
    #             "invalid e, e must be co-prime with phi(n), less than phi(n) and greater than 1 ")
    #         exit()

    # print("public key is validated you can start the communication .. ")
    # print(p, q, e)

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    # publick_key = [p, q, e]

    # j = 0
    # while j < 3:
    #     messg = str(publick_key[j])
    #     client_socket.send(messg.encode())
    #     print(messg)
    #     j += 1
    # client_socket.send(messg.encode())
    # message = input(" -> ")  # take input
    p = client_socket.recv(1024).decode()  # receive response
    q = client_socket.recv(1024).decode()  # receive response
    e = client_socket.recv(1024).decode()  # receive response

    # print(p, q, e)

    while True:
        # client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        

        print('Received from server: ' + data)  # show in terminal

        # message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    reciever_program()

