from aes import AES 

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a * 2, b)])

class HAeSH:
    def __init__(self, key):
        self.state = b'\x00' * 16 
        self.key = key
        self.blocks = []
    
    def update(self, block, backdoor = None):
        assert len(block) == 16 or len(block) == 24 or len(block) == 32, "🚫 Block length should be 16,24,32"
        self.blocks.append(block)
        mid_state = xor(self.state, block) 
        if len(self.blocks) > 1:
            assert mid_state not in self.blocks, "🚫 Block repetition detected"
        self.state = xor(self.state, 
                         AES(mid_state, backdoor).
                         encrypt_block(self.key))

    def digest(self):
        return self.state

test = False

block1 = bytes.fromhex("ca 45 20 ea 26 11 ac 9c 30 3c c2 06 7c 39 55 e2 7e 2f d9 46 84 1f b2 3e 96 2a 82 ef 21 00 57 6c")
block2 = bytes.fromhex("35 45 20 ea 26 11 ac 9c cf 3c c2 06 7c 39 55 e2 94 5a ac d9 84 1f b2 3e 7c 5f f7 70 21 00 57 6c")
key    = bytes.fromhex("83 66 63 dc b1 bc 61 82 30 38 ab f7 14 c3 d4 6a") 
hash = HAeSH(key)
hash.update(block1, True)
ret = hash.digest()
block2 = xor(ret, block2)
# print(key.hex())
# print(block1.hex())
# print(block2.hex())
if test:
    hash.update(block2, True)
    # print(hash.digest())
else:
    from pwn import * 
    io = remote("8.147.132.32",38529)
    io.recvuntil("🔑: ".encode()) 
    io.sendline(key.hex().encode()) 
    io.recvuntil(f"🥢[e]: ".encode())
    io.sendline(block1.hex().encode()) 
    io.recvuntil("Quit? (y/n): ".encode())
    io.sendline(b"n")  
    io.recvuntil(f"🥢[S]: ".encode())
    io.sendline(block2.hex().encode())
    io.recvuntil("Quit? (y/n): ".encode())
    io.sendline(b"y")
    if io.recvuntil("🔓 Success!\n".encode()):
        flag = io.recvuntil(b"}").decode()
        print(flag)
    else:
        print("Failed") 
    io.close()

