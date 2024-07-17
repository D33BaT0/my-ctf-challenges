from binascii import hexlify, unhexlify
from cypher import ToyCypher,b2i,genplain
from secret import flag
from random import Random
import os 
import signal

def _handle_timeout(signum, frame):
    raise TimeoutError('function timeout')

timeout = 10
signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(timeout)


print("You want to play.Let's play!🤡")
key = os.urandom(6)
toycipher = ToyCypher(b2i(key))
rng = Random()
rng.seed(int.from_bytes(os.urandom(20),'big'))

state1times = 0x01
state2times = 0x32

while 1:
    op = input(":👾O👾:")[:1].upper()

    if op == "G":
        if state1times == 0x00: continue
        cip = "".join([hexlify(toycipher.enc(genplain(rng))).decode() for i in range(0x139)]) 
        state1times -= 1
        print("😈:",cip)

    elif op == "E":
        if state2times == 0x00: continue
        msg = unhexlify(input("You will not kill my allies💕:")[:16])
        cip = hexlify(toycipher.enc(msg)).decode()
        print("Open up the sky👽:", cip)
        state2times -= 1
    
    elif op == "F":
        guess_cip = input("Seek them out:")[:16]
        real_ciph = hexlify(toycipher.enc(genplain(rng))).decode()
        if guess_cip == real_ciph:
            print("I know you exactly where you are!🚩:" + flag.decode())
        else:
            print("Get out of my way!⚡")
            exit(0)

