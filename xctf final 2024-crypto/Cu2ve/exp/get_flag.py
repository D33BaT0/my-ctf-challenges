from hashlib import shake_128
from itertools import product
from tqdm import tqdm
def encrypt(msg, key):
    y = shake_128("".join(map(str, key)).encode()).digest(len(msg))
    return bytes([msg[i] ^ y[i] for i in range(len(msg))])

real_hidden = [0, '?', 1, 1, 1, 1, 0, 1, '?', 1, '?', 1, 1, 1, 1, 1, 0, '?', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, '?', 1, 0, '?', 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, '?', 0, 1, '?', '?', 0, '?', '?', 1, 1, 1, 0, 1, 1, '?', 1, 0, '?', 0, '?', 1, 1, 0, 0, 0, 1, 0, 1, 1, '?', 0, 1, '?', 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1]
unknown_idx = [-1]
for _ in range(len(real_hidden)):
    if real_hidden[_] == '?':unknown_idx.append(_)
c = bytes.fromhex('dbc2eddcafdbd5d2dbc1b92cb32b4d6a604950c127a9d77007ee81bf')

length = len(unknown_idx) - 1
for itmp in tqdm(product([0,1],repeat=length)): 
    new_hidden = []
    for _ in range(length + 1):
        if _ == length:
            ti = real_hidden[unknown_idx[_]+1:]
        else:
            ti = real_hidden[unknown_idx[_]+1:unknown_idx[_+1]]
            ti.append(itmp[_])
        new_hidden.extend(ti)
    msg = encrypt(c, new_hidden)
    if b'flag' in msg:
        print(msg)

