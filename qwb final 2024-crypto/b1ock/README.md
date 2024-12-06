# b1ock

## Category

Crypto

## Difficulty

Medium Hard.

## Solves

11/32(so many??!)

## Description

2 1z block  cipher.

## FLAG

`flag{y0u_c4n_e4sy1ly_f1nd_th3_INv@r1aN7_S33d!}`

## WriteUps

### Unintend

赛中发现大量选手在尝试去固定一个choice的选取去恢复seed(貌似maple3142那有相关脚本)，但是由于 Python 3.12 4300digits 的限制使得该非预期无法通过远程但是本地可以通，差点锅了。

### Intend

由于此处选用的operations是random.choice的，且其为48轮DES操作（共291个操作）。

同时发现写的operation中具有大量的只取前64比特进行操作，或者是结果将原来的前64比特附在前面，后面跟着输出结果。

这如果使用random.choice令其操作顺序打乱，会导致很多问题

1. 部分行为并没有进行操作（比如说pbox,sbox,extend等操作）；
2. exchange可能使得前面部分操作不发生变换；
3. 大部分位置添加的信息是可以预测的，比如说pbox的后半段；extend的后半段；
4. 同时有时可以使得add round key直接没有在操作，那么可以直接删去key的行为（整体变为一个线性的）

我们首先是需要去找到一个种子使得ark操作完全消失的时候，那么直接进行爆破即可（不用一个个去写操作判断）

tmp2des是des.py的改了一点点

```python
import os 
from des import DES as DESS 
from tmp2des import _initial_permutate,_final_permutate,_exchange_blocks,E,\
        S_BOXES,P

def find_brute_seed():
    plaintext = os.urandom(8) 
    
    key1 = os.urandom(8)
    key2 = os.urandom(8)
    while 1:
        seed1 = int.from_bytes(os.urandom(8), "big") 
        mydes_backdoored1 = DESS(key1, rounds=48, backdoor = seed1)
        mydes_backdoored2 = DESS(key2, rounds=48, backdoor = seed1)
        c1 = mydes_backdoored1.encrypt_block(plaintext)
        if  c1 == mydes_backdoored2.encrypt_block(plaintext):
            print(seed1)
            for _ in range(100):
                assert c1 ==  DESS(os.urandom(8), rounds=48, backdoor = seed1).encrypt_block(plaintext)
            break
```

找到种子后即直接进行写逆函数分析即可，我这里使用的种子是5170914533036723911

整体分析过程如下，细节就不写了：

```python

seed = 5170914533036723911
key = os.urandom(8)

test = False
if test:
    m0 = os.urandom(8)
    mydes_backdoored  = DESS(key, rounds = 48, backdoor = seed)
    c0 = mydes_backdoored.encrypt_block(m0)
else:
    c0 = bytes.fromhex(input())

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

```

