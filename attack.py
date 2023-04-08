import common_functions
import generate_key
import encryption_functions as sender
import decryption_functions as reciever
import time
import matplotlib.pyplot as plt

# --------------------------------- Mathematical attack ------------------------


def mathematicalAttack(C, n, e):
    recovered = ''
    Eve = reciever.Receiver()
    # since n is composite then one of its factors is <=sqrt(n)
    for p in range(2, int((n**0.5)+1)):
        if n % p == 0:
            Eve.q = n//p
            Eve.e = e
            Eve.p = p
            break

    # stringC = ''
    # print(C)
    # for c in C:
    # print(c)
    # stringC = stringC + " " + c

    # print(stringC)
    recovered = Eve.decryption(C)
    return recovered

# --------------------------------- CCA ------------------------


def CCA(C, n, e):
    # M => C
    # generate r that is co-prime with n
    r = generate_key.generate_e(n)
    # compute C dash that will be sent to Bob using cipher text of the required msg
    # C` = C r^e mod n
    C = C.split(" ")
    del C[0]
    C_dash = []
    for c in C:
        C_dash.append(int(c) * pow(r, e) % n)
    print('C_dash = ', C_dash)
    cipherText = ''
    for i in C_dash:
        cipherText = cipherText + ' ' + str(i)
    print('cipherText = ', cipherText)
    # Bob decrypts C dash and sends it back to Eve
    # Y = (C * r^e)^ d mod n

    Y = Bob.decryption(cipherText)
    print("Y before split to groups = ", Y)
    Y = common_functions.splitToGroups(Y)
    print("Y after split to groups = ", Y)
    Y = common_functions.convertToInt(Y)
    # Now, Eve can get the message: Y = (M^e * r^e)^d mod n => as d = e^-1 mod n
    # so Y= M * r mod n =>  M = Y *(r^-1) mod n so it's very easy to obtain messages
    # M = common_functions.power_mod_solve((Y * cf.mod_inverse_solve(r, n)), 1, n)
    # Y = Y.split(" ")
    print("y = ", Y)
    recovered = ''
    for y in Y:
        M = int(y) * common_functions.mod_inverse_solve(r, n) % n
        recovered = recovered + common_functions.convertToString(M)
        print('M = ', M, 'recovered = ', recovered)
    return recovered

def  ChosenPlainTextAttack():
    d=0
    return None

time_or_test = input(
    "To test attacks press 1, to test the key length vs time press 2: ")
p = 0
q = 0
if time_or_test == "1":
    type = input("For MA press 1, For CCA press 2: ")

    # -------------------- Generate e,n,C for the attacks ------------
    Bob = reciever.Receiver()
    Alice = sender.Sender()
    Bob_data = open("bob_data.txt", "r")
    lines = Bob_data.read().splitlines()
    i = 0
    while i < len(lines)-1:
        Bob.p = int(lines[i])
        Bob.q = int(lines[i+1])
        i += 3
    Bob_data.close()
    Bob.e = generate_key.generate_e((Bob.p-1) * (Bob.q-1))
    e = Bob.e
    p = Bob.p
    q = Bob.q
    # -------------------- Takes msg from user in the allowed range -------------------
    msg = input("Enter message: ")
    splited_message = common_functions.splitToGroups(msg)
    m = common_functions.convertToInt(splited_message)
    # allowed, max = cf.is_key_enough(Bob.p*Bob.q, msg)
    while (max(m) > p*q):
        print("max allowed length of message is only ")
        msg = input("Enter message: ")
        splited_message = common_functions.splitToGroups(msg)
        m = common_functions.convertToInt(splited_message)
        # allowed, max = cf.is_key_enough(Bob.p*Bob.q, msg)
    #Sender: Alice
    Alice.set_public_key(Bob.p, Bob.q, Bob.e)
    # cipher_text = Alice.encryption(msg)
    # C = common_functions.convertToInt(cipher_text)
    C = Alice.encryption(msg)
    # write data in file that attacker will intercept
    with open('attacks_test.txt', 'w') as f:
        f.write(str(C) + "\n")
        f.write(str(Bob.e) + "\n")
        f.write(str(Bob.p*Bob.q))
    f.close()

    attacker_data = open('attacks_test.txt', "r")
    lines = attacker_data.read().splitlines()
    i = 0
    while i < len(lines)-1:
        C = lines[i]
        e = int(lines[i+1])
        n = int(lines[i+2])
        i += 4
    attacker_data.close()

    # #---------------------------- Mathematical Attack --------------
    if type == "1":

        recovered = mathematicalAttack(C, n, e)

        # write attack results and original message
        with open('mathematicalAttack_Results.txt', 'w') as f:
            f.write("Original message: " + msg + "\n")
            f.write("Recovered message: " + recovered + "\n")
            f.close()

        print("The attack is done, hard luck next time!")

    # ------------------------------ CCA ATTACK -----------------

    elif type == "2":

        recovered = ChosenPlainTextAttack(C, n, e)

        # write attack results and original message
        with open('ChosenPlainTextAttackResult.txt', 'w') as f:
            f.write("Original message: " + msg + "\n")
            f.write("Recovered message: " + recovered + "\n")
            f.close()

        print("The attack is done, hard luck next time!")

    else:
        print("please choose 1 or 2")


# ---------------------------- Plotting -------------------------------

elif time_or_test == "2":
    test_file = open("graphs_msg.txt", "r")
    lines = test_file.read().splitlines()
    msg = lines[0]
    test_file.close()  # close the file

    # -------------------- Generate p,q for n bits ---------------------
    with open('keylengthVsTimeAttack.txt', 'w') as f:
        for n in range(8, 65, 2):
            p, q = common_functions.generate_pq(n)
            f.write(str(p) + "\n")
            f.write(str(q) + "\n")
            f.write("\n")
    f.close()

    # ---------------------------------------------------

    key_lengths = []
    time_to_attack = []
    Alice = sender.Sender()
    Bob = reciever.Receiver()

    Bob_data = open("keylengthVsTimeAttack.txt", "r")
    lines = Bob_data.read().splitlines()
    i = 0
    C_list = []
    e_list = []
    n_list = []
    while i < len(lines)-2:
        Bob.p = int(lines[i])
        Bob.q = int(lines[i+1])

        Bob.e = generate_key.generate_e((Bob.p-1) * (Bob.q-1))
        e = Bob.e
        #Sender: Alice
        Alice.set_public_key(Bob.p, Bob.q, Bob.e)
        cipher_text = Alice.encrypt(msg)
        C = common_functions.convertToInt(cipher_text)

        e = Bob.e
        n = Bob.p*Bob.q

        key_lengths.append(len(bin(n).replace("0b", "")))

        start_time = time.time()

        recovered = mathematicalAttack(C, n, e)

        end_time = time.time()
        time_to_attack.append(end_time - start_time)

        # ----------------- to only save results in a txt file
        C_list.append(C)
        e_list.append(e)
        n_list.append(n)
        # --------------------------------------------

        i += 3

    Bob_data.close()

    with open('dataForAttacker.txt', 'w') as f:
        for k in range(len(C_list)):
            f.write(str(C_list[k]) + "\n")
            f.write(str(e_list[k]) + "\n")
            f.write(str(n_list[k])+"\n")
            f.write("\n")
    f.close()

    fig, ax = plt.subplots()
    ax.set_xticklabels(n_list)
    ax.plot(key_lengths, time_to_attack, linewidth=2.0)
    ax.set_title("Key length vs Time to attack")
    ax.set_xlabel("Key value")
    ax.set_ylabel("Time to attack")
    plt.show()

else:
    print("Please choose 1 or 2")
