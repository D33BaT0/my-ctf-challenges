from Crypto.Util.number import getPrime 
from sympy import nextprime
from secret import FLAG
import numpy as np
import random
import signal
import os


def _handle_timeout(signum, frame):
    raise TimeoutError('function timeout')

timeout = 450
signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(timeout)

def uniform_sample(n, bound, SecureRandom):
    return [SecureRandom.randrange(-bound, bound) for _ in range(n)]

def choice_sample(n, L, SecureRandom):
    return [SecureRandom.choice(L) for i in range(n)]

n = 197
m = 19700
q = getPrime(20)

e_L = [random.randrange(0, q-1) for i in range(2)]
R_s = random.SystemRandom()
R_e = random.SystemRandom()

s = np.array(uniform_sample(n, q//2, R_s))
e = np.array(choice_sample(m,  e_L, R_e))

seed = os.urandom(16)
R_A = random
R_A.seed(seed)
A = np.array([uniform_sample(n, q, R_A) for _ in range(m)])
b = (A.dot(s) + e) % q

print(f"{q = }")
print(f"{e_L = }")
print(f"{seed.hex() = }")
print(f"{b.tolist() = }") 

s_ = input("Give me s: ")
if s_ == str(s.tolist()):
    print("Congratulations! You have signed in successfully.")
    print(FLAG)
else:
    print("Sorry, you cannot sign in.")