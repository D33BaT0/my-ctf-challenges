import os 
from des import DES as DESS 
from tmp2des import _initial_permutate,_final_permutate,_exchange_blocks,E,\
        S_BOXES,P

def find_brute_seed():
    plaintext = os.urandom(8) 
    
    key1 = os.urandom(8)
    key2 = os.urandom(8)
    
    while 1:
        seed1 = int.from_bytes(os.urandom(6), "big") 
        mydes_backdoored1 = DESS(key1, rounds=48, backdoor = seed1)
        mydes_backdoored2 = DESS(key2, rounds=48, backdoor = seed1)
        c1 = mydes_backdoored1.encrypt_block(plaintext)
        if c1 == mydes_backdoored2.encrypt_block(plaintext):
            print(seed1)
            for _ in range(100):
                assert c1 ==  DESS(os.urandom(8), rounds=48, backdoor = seed1).encrypt_block(plaintext)
            break
import time
for _ in range(100):
    start_time = time.time()
    find_brute_seed() 
    end_time = time.time()
    print(f"Time: {end_time - start_time} seconds")
# 5170914533036723911


seed = 5170914533036723911
test = True
if test:
    m0 = os.urandom(8)
    key = os.urandom(8)
    mydes_backdoored  = DESS(key, rounds = 48, backdoor = seed)
    c0 = mydes_backdoored.encrypt_block(m0)
else:
    from pwn import *
    io = remote("8.147.132.32",38529) 
    io.sendlineafter("🌱 ".encode(),str(seed).encode())
    io.recvuntil("🤐 ".encode())
    c0 = bytes.fromhex(io.recvline().decode().strip())

### test
"""
mydes_backdoored2 = DES (key, rounds = 48, backdoor = seed)
print(len(mydes_backdoored2.operations))
# print(c0)
c1operation = mydes_backdoored2.operations
# delete addroundkey
newc1operation = []
for i in c1operation:
    if i[0] != _add_round_key:
        newc1operation.append(i)

c1operation = newc1operation
mydes_backdoored2.operations = c1operation
newc1operation = []
prefix_operation_length = len(c1operation)
for i in range(0, len(c1operation) - 1):
    if i==0:
        if c1operation[i][0] == _xor_blocks:
            continue
        else:
            newc1operation.append(c1operation[i])

    else: 
        prefix_operation = c1operation[i-1]
        now_operation = c1operation[i]
        suffix_operation = c1operation[i+1]
        if prefix_operation in (_initial_permutate,_final_permutate,\
                                _exchange_blocks,_xor_blocks) and \
                                    now_operation == _xor_blocks:
            continue
        else:
            newc1operation.append(now_operation)
"""
def _inverse_extend_then_xor_block(block):
    # Extend block to 48 bits
    l, r = block[0:32], block[32:64] 
    rr = ''.join(r[i-1] for i in E)[:32]
    l = bin(int(l,2)^int(rr,2))[2:].zfill(32)
    return l + r

def _inverse_64bit_sbox_sbox_then_xor_block(block):
    l,r = block[:32],block[32:]
    x = "0" * 48
    output = ''
    for i in range(8):
        chunk = x[i*6:(i+1)*6]
        row = int(chunk[0] + chunk[5], 2)
        col = int(chunk[1:5], 2)
        output += bin(S_BOXES[i][row][col])[2:].zfill(4)
    x = output.zfill(48)
    output = ''
    for i in range(8):
        chunk = x[i*6:(i+1)*6]
        row = int(chunk[0] + chunk[5], 2)
        col = int(chunk[1:5], 2)
        output += bin(S_BOXES[i][row][col])[2:].zfill(4)
    return bin(int(l,2) ^ int(output,2))[2:].zfill(32) + r

def _inverse_64bit_sbox_then_xor_block(block):
    l,r = block[:32],block[32:]
    x = "0" * 48
    output = ''
    for i in range(8):
        chunk = x[i*6:(i+1)*6]
        row = int(chunk[0] + chunk[5], 2)
        col = int(chunk[1:5], 2)
        output += bin(S_BOXES[i][row][col])[2:].zfill(4)
    return bin(int(l,2) ^ int(output,2))[2:].zfill(32) + r

# extend;pbox;extend;pbox;xor
def _inverse_64bit_epepx(block):
    l,r = block[:32],block[32:] 
    er = ''.join(r[i-1] for i in E)
    per = "".join(er.zfill(32)[i-1] for i in P).zfill(32)
    l = bin(int(l,2) ^ int(per,2))[2:].zfill(32)
    return l + r

def _inverse_64bit_pbox_then_xor_block(block):
    l,r = block[:32],block[32:] 
    tmp = "0"*32
    per = "".join(tmp[i-1] for i in P).zfill(32)
    l = bin(int(l,2) ^ int(per,2))[2:].zfill(32)
    return l + r

def _inverse_extend_sbox_then_xor_block(block):
    l,r = block[:32],block[32:] 
    x = ''.join(r[i-1] for i in E).zfill(48)
    output = ''
    for i in range(8):
        chunk = x[i*6:(i+1)*6]
        row = int(chunk[0] + chunk[5], 2)
        col = int(chunk[1:5], 2)
        output += bin(S_BOXES[i][row][col])[2:].zfill(4)
    return bin(int(l,2) ^ int(output,2))[2:].zfill(32) + r

## test
"""
c1operation = newc1operation[1+3+1+1:-4-5-2-1 -4 -1] # exchange_blocks
c1operation = c1operation[ 9 :-17 ] # exchange_blocks
c1operation = c1operation[:-2 - 7-7 - 2 - 1 - 2 - 1] 
c1operation = c1operation[:-1 - 3] 
c1operation = c1operation[: - 5-6-7-4 - 1 - 4 - 1] 
c1operation = c1operation[: - 1 - 2 - 4 - 2-6 - 1-1 - 2] 
c1operation = c1operation[: -2-2-5-1 - 2 - 3 - 1 - 1 - 2 - 2 - 2 - 3]  
c1operation = c1operation[: -5 - 2 - 3 - 3 - 2 - 2 - 2 - 1-5-1 -11]  
c1operation = c1operation[: -1-2-1-2-1 - 2 - 1 - 4 - 1 - 2-8-7-1]  
c1operation = c1operation[: -12 - 1 - 3 - 1 - 4 - 2]
mydes_backdoored2.operations = c1operation
assert len(mydes_backdoored2.operations) == 0
"""
def inv_c0(c0:bytes): 
    c0 = bin(int.from_bytes(c0, "big"))[2:].zfill(64)
    c0 = _final_permutate(c0)
    c0 = _exchange_blocks(c0)
    c0 = _inverse_extend_then_xor_block(c0) 
    c0 = _initial_permutate(c0)
    c0 = _exchange_blocks(c0)
    c0 = _inverse_64bit_sbox_sbox_then_xor_block(c0)
    c0 = _inverse_64bit_epepx(c0) 
    c0 = _exchange_blocks(c0)
    c0 = _inverse_extend_then_xor_block(c0)
    c0 = _exchange_blocks(c0)
    c0 = _inverse_64bit_sbox_then_xor_block(c0)
    c0 = _inverse_extend_then_xor_block(c0)
    c0 = _inverse_64bit_pbox_then_xor_block(c0)
    c0 = _initial_permutate(c0)
    c0 = _inverse_extend_then_xor_block(c0)
    c0 = _inverse_extend_then_xor_block(c0)
    c0 = _exchange_blocks(c0)
    c0 = _inverse_extend_sbox_then_xor_block(c0)
    c0 = _inverse_extend_sbox_then_xor_block(c0)
    c0 = _inverse_extend_then_xor_block(c0)
    c0 = _inverse_64bit_sbox_then_xor_block(c0) 
    c0 = _exchange_blocks(c0)
    c0 = _inverse_extend_then_xor_block(c0)
    c0 = _inverse_extend_then_xor_block(c0) 
    return int(c0, 2).to_bytes(8, "big")

m00hex = inv_c0(c0).hex()



if test == True:
    print(m00hex == m0.hex())
else:
    print(m00hex)
    io.recvuntil("💬 ".encode())
    io.sendline(m00hex.encode())
    io.interactive()
