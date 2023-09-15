from pwn import *
from itertools import product
from hashlib import sha256
def prow(io):
    io.recvuntil(b'XXXX+')
    suffix = io.recvuntil(b')')[:-1]
    io.recvuntil(b"== ")
    hashs = io.recvline().strip().decode()
    for x in product(string.ascii_letters+string.digits,repeat=4):
        if sha256(("".join(x)+suffix.decode()).encode("utf-8")).hexdigest() == hashs:
            ret = ("".join(x))
            io.recvuntil(b'XXXX :')
            print(ret)
            io.sendline(ret.encode())
            return 
io = remote("node4.buuoj.cn",25174)
prow(io)
io.recv()
io.send(b'0,3034')
io.interactive()