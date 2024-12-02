from sage.all import *
from sage.rings.finite_rings.hom_finite_field import FiniteFieldHomomorphism_generic
from Crypto.Util.number import * 
from base64 import b64encode
from random import * 
from secret import flag
import signal

def _handle_timeout(signum, frame):
    raise TimeoutError('function timeout')

timeout = 66
signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(timeout)

def qary_trans_to_int(x, q):
    return sum([int(x[i]) * q**i for i in range(len(x))])

def encode(f, q):
    try:
        return b64encode(long_to_bytes(qary_trans_to_int(f.polynomial().coefficients(sparse = False), q)))
    except:
        return b64encode(long_to_bytes(qary_trans_to_int(f.coefficients(sparse = False), q)))

def generate_irreducible_polynomial(R, n):
    while True: 
        f = R.random_element(degree=n) 
        while f.degree() != n:
            f = R.random_element(degree=n) 
        if f.is_irreducible():
            return f

def generate_sparse_irreducible_polynomial(R, n): 
    x = R.gen()
    while True:
        g = sum(choice([-1, 0, 1]) * x**i for i in range(randint(1, n//2 + 1)))
        if (x**n + g + 1).is_irreducible():
            return x**n + g + 1

def random_polynomial(R, n, beta):  
    return sum(randrange(-beta, beta) * R.gen()**i for i in range(randint(0, n))) + R.gen()**n  

q = 333337
n = 128
beta = 333 
chance = 111
polyns = beta//chance
bound  = 106
R = PolynomialRing(GF(q),'x')

F = generate_irreducible_polynomial(R,n).monic()

k1 = GF(q**n, name = 'a', modulus = generate_sparse_irreducible_polynomial(R,n).monic())
k2 = GF(q**n, name = 'b', modulus = F)

phi = FiniteFieldHomomorphism_generic(Hom(k1, k2)) 

print("F:", encode(F,q).decode())

win_count = 0
for _ in range(chance):
    opt = randint(0, 1)
    if opt:
        As = [phi(random_polynomial(k1,n,beta)) for i in range(polyns)] 
    else:
        As = [k2.random_element() for i in range(polyns)]
    
    for i in range(polyns):
        print(f"As[{i}]: {encode(As[i],q).decode()}")

    opt_guess = input("Guess the option[0/1]: ")
    if int(opt_guess) != opt:
        print("Wrong guess!")
    else:
        win_count += 1
        print("Correct guess!")

if win_count >= bound:
    print("You are so smart! Here is your flag:")
    print(flag)
else:
    print("No flag for you!")
