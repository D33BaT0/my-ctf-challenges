from Crypto.Util.number import *
from Crypto.Cipher import DES
# https://ieeexplore.ieee.org/document/9832875
from pwn import * 
io = remote("192.168.1.107",11420)
io.recv()
io.sendline(b"B0B351C802C83DE0")
io.recv()
io.sendline(b"4739a2f04b7eab28")
io.interactive()


key = long_to_bytes(0xB0B351C802C83DE0)
plain = long_to_bytes(0x4739a2f04b7eab28)
des = DES.new(key,DES.MODE_ECB)

def tmp_enc(des,msg):
    for _ in range(114514):
        msg = des.encrypt(msg)
    return msg

assert tmp_enc(des,plain) == plain

P2 =  long_to_bytes(0x9FE10D2E8C496143)
K2 =  long_to_bytes(0x5D460701328F2962)
des = DES.new(K2,DES.MODE_ECB)
assert des.encrypt(P2) == P2
