import common_functions
import generate_key
import encryption_functions as sender
import decryption_functions as reciever
import time
import matplotlib.pyplot as plt
import sympy

# --------------------------------- Mathematical attack ------------------------


def mathematicalAttack(C, n, e):
    C = C.split(" ")
    recovered = ''
    # generate instans of reciever (attacker)
    Eve = reciever.Receiver()

    # # since n is composite then one of its factors is <=sqrt(n)
    for p in range(2, int((n**0.5)+1)):
        if n%p == 0:
            Eve.q = n//p
            Eve.e = e
            Eve.p = p
            break   

    # sympy.factorint(n) function get the prime factoriztion quickly
    # Eve.q, Eve.p = sympy.factorint(n)    
    Eve.e = e
    Eve.n = Eve.p*Eve.q
    Eve.key_computed = False
    for c in C:
        recovered = recovered + Eve.decryption(c)
    
    return recovered

while True:
    time_or_test = input(
        "To test attacks press 1, To test the key length vs attack time press 2: ")
    p = 0
    q = 0
    if time_or_test == "1":

        # -------------------- Generate e,n,C for the attacks ------------
        # generate instanse of sender=> alice, reciver=> bob
        Bob = reciever.Receiver()
        Alice = sender.Sender()

        # generate random primes p, q
        p, q = common_functions.gererate_pq_primes()

        # Print the values of p and q
        print("p gererated: ", p)
        print("q gererated: ", q)

        # set generated p, q to bob (reciever)
        Bob.p = p
        Bob.q = q
        Bob.n = p*q

        # generate e that coprime with p, q
        Bob.e = generate_key.generate_e((Bob.p-1) * (Bob.q-1))

        e = Bob.e
        p = Bob.p
        q = Bob.q

        # -------------------- Takes msg from user in the allowed range -------------------
        msg = input("Enter message: ")

        # Sender: Alice ==> public key (e, n)
        Alice.set_public_key(Bob.e, Bob.p*Bob.q)


        splited_message = common_functions.splitToGroups(msg)
        # encode the groups, convert them to integer
        m, count = common_functions.convertToInt(splited_message)
        # caluclate the cipher Text
        C = ''
        decryptedMessage = ''
        for i in m:
            c = Alice.encryption(i)
            d = Bob.decryption(c)
            decryptedMessage = decryptedMessage + d
            C = C + " " + str(c)
        C = C[1:]
        # write data in file that attacker will intercept
        with open('attacks_test.txt', 'w') as f:
            f.write(
                "it's the cipher text, and public key==> (e, n) that attacker want to attack" + "\n")
            f.write(str(C) + "\n")
            f.write(str(Bob.e) + "\n")
            f.write(str(Bob.p*Bob.q))
        f.close()

        attacker_data = open('attacks_test.txt', "r")
        lines = attacker_data.read().splitlines()
        i = 1
        while i < len(lines)-1:
            C = lines[i]
            e = int(lines[i+1])
            n = int(lines[i+2])
            i += 4
        attacker_data.close()

        # #---------------------------- Mathematical Attack --------------
        recovered = mathematicalAttack(C, n, e)

        # write attack results and original message
        with open('mathematicalAttack_Results.txt', 'w') as f:
            f.write("Original message: " + msg + "\n")
            f.write("Recovered message: " + recovered + "\n")
            f.close()
        if(decryptedMessage == recovered):    
            print("The attack is done, hard luck next time!")


    # ---------------------------- Plotting -------------------------------

    elif time_or_test == "2":
        # read message for attack
        test_file = open("graphs_msg.txt", "r")
        lines = test_file.read().splitlines()
        msg = lines[0]
        test_file.close()

        # -------------------- Generate p,q for n bits ---------------------
        # put them in text file to use later
        # with open('keylengthVsTimeAttack.txt', 'w') as f:
        #     for n in range(1, 65, 2):
        #         p, q = common_functions.generate_pq(n)
        #         f.write(str(p) + "\n")
        #         f.write(str(q) + "\n")
        #         f.write("\n")
        # f.close()

        # ---------------------------------------------------
        # store key_lengths, time_to_attack in lists to compare and plot later
        key_lengths = []
        time_to_attack = []
        # generate instanse of sender=> alice, reciver=> bob
        Alice = sender.Sender()
        Bob = reciever.Receiver()

        # access data generated in text file
        Bob_data = open("keylengthVsTimeAttack.txt", "r")
        lines = Bob_data.read().splitlines()
        # for jumping in lines
        i = 0
        # for printing only
        j = 1

        # store c, e, n in lists only to save results in a txt file
        C_list = []
        e_list = []
        n_list = []

        while i < len(lines)-2:
            # access p, q for the reciever
            Bob.p = int(lines[i])
            Bob.q = int(lines[i+1])

            # generate e that coprime with p, q
            Bob.e = generate_key.generate_e((Bob.p-1) * (Bob.q-1))

            # Sender: Alice ==> public key (e, n)
            Alice.set_public_key(Bob.e, Bob.p*Bob.q)

            splited_message = common_functions.splitToGroups(msg)
            # encode the groups, convert them to integer
            m, count = common_functions.convertToInt(splited_message)

            # caluclate the cipher Text
            C = ''
            for ii in m:
                c = Alice.encryption(ii)
                C = C + " " + str(c)
            C = C[1:]

            # key_lengths.append(len(bin(n).replace("0b", "")))
            key_lengths.append(j)

            # calculate time
            start_time = time.time()
            recovered = mathematicalAttack(C, Bob.p*Bob.q, Bob.e)
            end_time = time.time()
            print('number of bits = ', j, '- Take time = ', end_time - start_time)

            # store time
            time_to_attack.append(end_time - start_time)

            # ----------------- to only save results in a txt file
            C_list.append(C)
            e_list.append(Bob.e)
            n_list.append(Bob.p*Bob.q)
            # --------------------------------------------
            j += 2
            i += 3

        Bob_data.close()

        # write c, e, n in text fie
        with open('dataForAttacker.txt', 'w') as f:
            for k in range(len(C_list)):
                f.write(str(C_list[k]) + "\n")
                f.write(str(e_list[k]) + "\n")
                f.write(str(n_list[k])+"\n")
                f.write("\n")
        f.close()

        # plot Key length vs Time to attack
        fig, ax = plt.subplots()
        # ax.set_xticklabels(key_lengths)
        ax.plot(key_lengths, time_to_attack, linewidth=2.0)
        ax.set_title("Key length(bits) vs Time to attack")
        ax.set_xlabel("Key length(bits)")
        ax.set_ylabel("Time to attack (s)")
        plt.show()
    
    else:
        print("Please choose 1, 2 ")
