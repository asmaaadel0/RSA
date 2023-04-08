import generate_key
import encryption_functions as sender
import decryption_functions as reciever
import time
import matplotlib.pyplot as plt

theSender = sender.Sender()
theReceiver = reciever.Receiver()

key_lengths = []
encryption_time = []
decryption_time = []
# read message to be encrypted
test_file = open("graphs_msg.txt", "r")
lines = test_file.read().splitlines()
message = lines[0]
test_file.close()  # close the file

# read Os & Qs being used to plot the graph
test_file = open("efficiencyPQ.txt", "r")
lines = test_file.read().splitlines()
i = 0
while i < len(lines)-1:
    # read the message and the public key
    p = int(lines[i])
    q = int(lines[i+1])
    key_lengths.append(len(bin(p*q).replace("0b", "")))
    i += 3
    # generate public key e
    e = generate_key.generate_e((p-1) * (q-1))

    theReceiver.p = int(p)
    theReceiver.q = int(q)
    theReceiver.e = int(e)
    theReceiver.n = theReceiver.p*theReceiver.q

    theSender.set_public_key(e, p*q)

    # encrypt the message
    start_time = time.time()
    cipher_text = theSender.encryption(message)
    end_time = time.time()
    # store time taken
    encryption_time.append(end_time - start_time)

    # decrypt the message
    start_time = time.time()
    message = theReceiver.decryption(cipher_text)
    end_time = time.time()
    # store time taken
    decryption_time.append(end_time - start_time)

test_file.close()  # close the file
print("time taken:")
print(encryption_time)
print("corresponding key lengths in bits:")
print(key_lengths)
# plotting the key length VS encryption time (efficiency)
plt.plot(key_lengths, encryption_time)
plt.xlabel('key length in bits')
plt.ylabel('encryption time')
plt.title('RSA efficiency')
plt.show()

print("time taken:")
print(decryption_time)
print("corresponding key lengths in bits:")
print(key_lengths)

# plotting the key length VS decryption time (efficiency)
plt.plot(key_lengths, encryption_time)
plt.xlabel('key length in bits')
plt.ylabel('decryption time')
plt.title('RSA efficiency')
plt.show()