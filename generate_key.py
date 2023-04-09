
import random

# generate e, coprime with phi n


def generate_e(num):
    # generate e such that it is co-prime with phi n
    e = random.randint(1, num)
    while not coprimes(e, num):
        e = random.randint(1, num)
    return e

# check if the two numbers is coprimes or not


def coprimes(A, B):
    if (gcd(A, B) == 1):
        return True
    else:
        return False

# calculate gcd of two numbers


def gcd(A, B):
    # base case
    if B == 0:
        return A
    # recursive till b equals to 0
    return gcd(B, A % B)
