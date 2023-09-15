from Crypto.Util.number import *
from random import randrange
from Crypto.Cipher import AES
from sympy.ntheory.residue_ntheory import nthroot_mod
from secret import flag

i = lambda x: pow(x, q-2, q)

def pad(m,lenth):
    return m + bytes([i for i in range(lenth-int(len(m)%lenth))])

def add(P,Q):
	if P[0] != Q[0] and P[1] != Q[1]:
		t = ((Q[1]-P[1]) * inverse(Q[0]-P[0],q)) %q
	else:
		t = ((3*P[0]*P[0]+AA)*inverse(2*P[1],q))%q
	x3 = t*t - P[0] - Q[0]
	y3 = t*(P[0] - x3) - P[1]
	return (x3%q, y3%q)

def mul(t, A, B=0):
    if not t: return B
    return mul(t//2, add(A,A), B if not t&1 else add(B,A) if B else A)

nbit = 128

while 1:
    qa = randrange(0,2**31) * 2
    qb = getPrime(nbit - 32)
    if isPrime(qa * qb + 1):
        q = qa * qb + 1
        break

print("Send the `y' element of two points in your desired elliptic curve:  ")
ans = input().encode()

try:
    y1, y2 = [int(_) % q for _ in ans.split(b',')]
except:
    print( "Your parameters are not valid! Bye!!")

AA = (y1**2 - y2**2 - 2022**3 + 2023**3) * inverse(-1, q) % q
BB = (y1**2 - 2022**3 - AA * 2022) % q

while 1:
    Gx = randrange(0,q - 1)
    try:
        Gy = int(nthroot_mod((Gx**3 + AA * Gx + BB) % q,2,q))
        print(pow(Gy,2,q) == (Gx**3 + AA * Gx + BB) % q)
        break
    except:
        continue

G = (Gx,Gy)
m = randrange(0,q-1)
C = mul(m,G)
aes = AES.new(m.to_bytes(16, 'big'), AES.MODE_CBC, bytes(16))
enc_flag = aes.encrypt(pad(flag,16))

print(f'The parameters and encrypted flag are:')
print(f'q = {q}')
print(f'G = ({Gx}, {Gy})')
print(f'm * G = ({C[0]}, {C[1]})')
print(f'encrypt flag = ({enc_flag})')