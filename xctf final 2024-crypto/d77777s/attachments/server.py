from Crypto.Util.number import *
from Crypto.Cipher import DES
from random import randint
from secret import flag
import os

def pad(msg):
    return msg + bytes([(8 - len(msg)) % 8 for _ in range((8 - len(msg)) % 8)])

key = bytes.fromhex(input("key[hex]:"))
assert len(key) == 8

des = DES.new(key,DES.MODE_ECB)
enc = lambda msg: des.encrypt(msg)

def check(enc): 
    for _ in range(100):
        msg = os.urandom(8)   
        if enc(enc(msg)) == msg: 
            return False
    return True

if not check(enc):
    print("bad key")
    exit()

msg = pad(bytes.fromhex(input("msg[hex]:")))

cip = msg
for _ in range(randint(0,77777)):
    cip = enc(cip)

if cip == msg:
    print("you find it.")
    print(flag)
else:
    print("GG")
