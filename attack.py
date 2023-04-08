import common_functions
import generate_key
import encryption_functions as sender
import decryption_functions as reciever
import time
import sympy
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
    recovered = Eve.decryption(C)
    return recovered


time_or_test = input(
    "To test attacks press 1, to test the key length vs time press 2: ")
p = 0
q = 0
if time_or_test == "1":
    # type = input("For MA press 1, For CCA press 2: ")

    # -------------------- Generate e,n,C for the attacks ------------
    Bob = reciever.Receiver()
    Alice = sender.Sender()

    p, q = common_functions.gererate_pq_primes()

    # Print the values of p and q
    print("p:", p)
    print("q:", q)

    Bob.p = p
    Bob.q = q

    Bob.e = generate_key.generate_e((Bob.p-1) * (Bob.q-1))

    e = Bob.e
    p = Bob.p
    q = Bob.q
    # -------------------- Takes msg from user in the allowed range -------------------
    msg = input("Enter message: ")

    splited_message = common_functions.splitToGroups(msg)
    m = common_functions.convertToInt(splited_message)

    while (max(m) > p*q):
        print("max allowed length of message is only ")
        msg = input("Enter message: ")
        splited_message = common_functions.splitToGroups(msg)
        m = common_functions.convertToInt(splited_message)

    #Sender: Alice
    Alice.set_public_key(Bob.e, Bob.p*Bob.q,)

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
    # if type == "1":

    recovered = mathematicalAttack(C, n, e)

    # write attack results and original message
    with open('mathematicalAttack_Results.txt', 'w') as f:
        f.write("Original message: " + msg + "\n")
        f.write("Recovered message: " + recovered + "\n")
        f.close()

    if (msg == recovered):
        print("The attack is done, hard luck next time!")


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
        Alice.set_public_key(Bob.e, Bob.p*Bob.q)
        C = Alice.encryption(msg)

        e = Bob.e
        n = Bob.p*Bob.q

        key_lengths.append(len(bin(n).replace("0b", "")))

        start_time = time.time()

        recovered = mathematicalAttack(C, n, e)

        end_time = time.time()
        time_to_attack.append(end_time - start_time)
        print(i+1, '- time = ', end_time - start_time )

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
