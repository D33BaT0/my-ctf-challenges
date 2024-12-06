import os
import signal
from Crypto.Cipher import DES as pyDES
from secret import flag
from des import DES  

def _handle_timeout(signum, frame):
    raise TimeoutError('function timeout')

timeout = 15
signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(timeout)

def _test():
    key = os.urandom(8)
    des = pyDES.new(key, pyDES.MODE_ECB)
    mydes = DES(key, rounds=16)
    mydes_backdoored = DES(key, rounds=16, backdoor = 0xdeadbeef)
    for _ in range(200):
        plaintext = os.urandom(8)
        ciphertext = des.encrypt(plaintext) 
        assert (mydes.encrypt_block(plaintext) == ciphertext) 
        assert (mydes_backdoored.encrypt_block(plaintext) != ciphertext) 

def main():  
    seed = int(input('🌱 '))
    key = os.urandom(8)

    cipher = DES(key, rounds = 48, backdoor = seed)

    m0 = os.urandom(8)
    c0 = cipher.encrypt_block(m0)
    print(f'🤐 {c0.hex()}')

    for _ in "🥵 You Only Live Once!"[0]:
        m = bytes.fromhex(input('💬 '))
        if m == m0: 
            print(f'🏁 {flag}')
            exit()
        c = cipher.encrypt_block(m)
        print(f'🤫 {c.hex()}')

if __name__ == '__main__':
    _test()
    main()
