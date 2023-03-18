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