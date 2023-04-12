import generate_key
import encryption_functions as sender
import decryption_functions as reciever
import common_functions
import time
import matplotlib.pyplot as plt

# generate instanse of sender=> theSender, reciver=> theReceiver
theSender = sender.Sender()
theReceiver = reciever.Receiver()

key_lengths = []
encryption_time = []
decryption_time = []

# -------------------- Generate p,q for n bits ---------------------
# put them in text file to use later
with open('efficiencyPQ.txt', 'w') as f:
    for n in range(27, 3000, 1):
        p, q = common_functions.generate_pq(n)
        f.write(str(p) + "\n")
        f.write(str(q) + "\n")
        f.write("\n")
f.close()

# read message to be encrypted
test_file = open("graphs_msg.txt", "r")
lines = test_file.read().splitlines()
message = lines[0]
test_file.close()  # close the file

# read p & q being used to plot the graph
test_file = open("efficiencyPQ.txt", "r")
lines = test_file.read().splitlines()
i = 0
j = 27
while i < len(lines)-1:
    print(lines[i])
    p = int(lines[i])
    q = int(lines[i+1])
    key_lengths.append(j)
    i += 3
    j += 1
    # generate public key e
    e = generate_key.generate_e((p-1) * (q-1))

    # set values for reciever
    theReceiver.p = int(p)
    theReceiver.q = int(q)
    theReceiver.e = int(e)
    theReceiver.n = theReceiver.p*theReceiver.q
    theReceiver.key_computed = False
    # set public key for the sender
    theSender.set_public_key(e, p*q)
    time1 = 0
    time2 = 0

    splited_message = common_functions.splitToGroups(message)
    # encode the groups, convert them to integer
    m, count = common_functions.convertToInt(splited_message)
    # caluclate the cipher Text
    C = ''
    decryptedMessage = ''
    for ii in m:
        # decrypt the message
        start_time = time.time()
        c = theSender.encryption(ii)
        end_time = time.time()
        time1 = time1 + (end_time - start_time)

        # decrypt the message
        start_time = time.time()
        decryptedc = theReceiver.decryption(c)
        end_time = time.time()
        time2 = time2 + (end_time - start_time)
        decryptedMessage = decryptedMessage + decryptedc


    # store time taken
    encryption_time.append(time1)

    
    # store time taken
    decryption_time.append(time2)

test_file.close()  # close the file
print("time taken:")
print(encryption_time)
print("corresponding key lengths in bits:")
print(key_lengths)
# plotting the key length VS encryption time (efficiency)
plt.plot(key_lengths, encryption_time)
plt.xlabel('Key length (bits)')
plt.ylabel('encryption time (s)')
plt.title('RSA efficiency')
plt.show()

print("time taken:")
print(decryption_time)
print("corresponding key lengths in bits:")
print(key_lengths)
# plotting the key length VS decryption time (efficiency)
plt.plot(key_lengths, decryption_time)
plt.xlabel('Key length (bits)')
plt.ylabel('decryption time (s)')
plt.title('RSA efficiency')
plt.show()