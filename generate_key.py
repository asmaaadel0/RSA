
import random


def isPrime(num):
    # If given number is greater than 1
    if num > 1:
        # Iterate from 2 to n / 2
        for i in range(2, int(num/2)+1):
            # If num is divisible by any number between
            # 2 and n / 2, it is not prime
            if (num % i) == 0:
                return False
        else:
            return True
    else:
        return False


def generate_e(num):
    # generate e such that it is co-prime with phi n
    e = random.randint(1, num)
    while not coprimes(e, num):
        e = random.randint(1, num)
    return e


def coprimes(A, B):
    if (gcd(A, B) == 1):
        return True
    else:
        return False


def gcd(A, B):
    # base case
    if B == 0:
        return A
    # recursive till b equals to 0
    return gcd(B, A % B)

def validate_e(e ,phi):
    if coprimes(e, phi) and e < phi and e > 1:
        return 1
    else:
        return 0  
