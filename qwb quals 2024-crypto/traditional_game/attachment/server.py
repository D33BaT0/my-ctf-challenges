from Crypto.Util.number import getPrime,bytes_to_long
from secret import secret,flag
import random
import time
import os
import signal

def _handle_timeout(signum, frame):
    raise TimeoutError('function timeout')

timeout = 300
signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(timeout)

random.seed(secret + str(int(time.time())).encode())

class RSA:
    def __init__(self):
        self.p = getPrime(512)
        self.q = getPrime(512)
        self.e = getPrime(128)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.d = pow(self.e, -1, self.phi)  

    def get_public_key(self):
        return (self.n, self.e)
    
    def get_private_key(self, blind_bit=None, unknown_bit=None):
        if blind_bit is not None and unknown_bit is not None:
            blind = getPrime(blind_bit)
            d_ = ((int(self.d >> unknown_bit) // blind * blind) << unknown_bit) + int(self.d % blind)
            return (d_, blind)
        else:
            return (self.d, 0)
    
    def encrypt(self, m):
        if type(m) == bytes:
            m = bytes_to_long(m)
        elif type(m) == str:
            m = bytes_to_long(m.encode())
        return pow(m, self.e, self.n)
    
    def game(self,m0,m1,b):   
        return self.encrypt([m0,m1][b]) 


rsa = RSA()
token = os.urandom(66) 

print( "[+] Welcome to the game!")
print(f"[+] rsa public key: {rsa.get_public_key()}")

coins = 100
price = 100
while coins > 0:
    print("=================================")
    b = random.randint(0,1)
    c = rsa.game(
        b'bit 0:' + os.urandom(114), 
        b'bit 1:' + os.urandom(114), 
        b)
    print("[+] c:",c)
    guessb = int(input("[-] b:"))
    coins -= 1
    if guessb == b:
        price -= 1
        print("[+] correct!") 
    else: 
        print("[+] wrong!") 

if price != 0: 
    print("[-] game over!")
    exit()

blind_bit = 40
unknown_bit = 365

d_,blind = rsa.get_private_key(blind_bit, unknown_bit)

print( "[+] Now, you have permission to access the privkey!")
print(f"[+] privkey is: ({d_},{blind}).")
print(f"[+] encrypt token is: {rsa.encrypt(bytes_to_long(token))}")

guess_token = bytes.fromhex(input("[-] guess token:"))
if guess_token == token:
    print("[+] correct token, here is your flag:",flag)
else:
    print("[-] wrong token")