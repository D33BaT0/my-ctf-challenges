def padding(msg):
    plen = (8 - len(msg) % 8) % 8
    return msg + bytes([plen]*plen)

def b2i(m):
    return int.from_bytes(m,'big')

def i2b(m,length):
    return int.to_bytes(m,length,'big')

def genplain(rng):
    plain = 0
    for _ in range(32):
        plain <<= 2
        plain  += rng.getrandbits(2)
    return i2b(plain,8)

class RoundsKeyGenerator:
    def __init__(self,master_key,rounds):
        self.MK = master_key
        self.rounds = rounds
        self.rounds_keys = []
        self.GenRoundsKeys()

    def RotMastKey(self):
        y = self.MK 
        y = y ^ y >> 14
        y = y ^ y << 21 & 0xb470deadbeef
        y = y ^ y << 13 & 0x33d0ea51c332
        y = y ^ y >> 3 
        self.MK = y

    def GenRoundsKeys(self):
        for _ in range(self.rounds):
            self.RotMastKey()
            self.rounds_keys.append(self.MK)

class ToyCypher:
    s_box =  [
              [15, 2, 7, 10, 4, 3, 11, 0, 13, 8, 6, 12, 14, 5, 1, 9, 
               5, 8, 6, 14, 10, 12, 2, 13, 1, 4, 11, 7, 9, 15, 3, 0, 
               4, 7, 0, 10, 15, 3, 1, 13, 14, 8, 2, 9, 6, 11, 5, 12,
               2, 12, 5, 3, 7, 10, 11, 0, 4, 14, 9, 6, 13, 1, 8, 15], 
              
              [6, 8, 10, 15, 13, 14, 12, 9, 1, 3, 0, 2, 11, 5, 7, 4, 
               2, 15, 12, 9, 8, 6, 14, 7, 5, 13, 4, 11, 3, 0, 10, 1, 
               13, 15, 7, 10, 1, 6, 5, 14, 12, 11, 9, 0, 2, 4, 8, 3, 
               5, 12, 15, 0, 1, 3, 13, 7, 11, 4, 6, 10, 8, 9, 14, 2],
               
              [1, 10, 7, 13, 5, 2, 6, 3, 0, 11, 12, 4, 8, 14, 15, 9, 
               0, 4, 7, 12, 9, 3, 10, 14, 11, 1, 5, 8, 13, 2, 15, 6, 
               11, 1, 6, 12, 15, 9, 2, 8, 5, 0, 4, 14, 13, 10, 3, 7,
               2, 11, 14, 10, 15, 8, 5, 13, 9, 7, 4, 1, 6, 0, 3, 12], 
              
              [13, 1, 6, 2, 9, 14, 10, 0, 7, 3, 15, 8, 12, 5, 11, 4, 
               11, 0, 7, 9, 6, 14, 5, 10, 8, 12, 15, 13, 3, 1, 4, 2, 
               13, 2, 0, 11, 5, 4, 12, 6, 10, 3, 1, 9, 7, 15, 8, 14,
               7, 1, 3, 5, 0, 9, 2, 11, 8, 13, 14, 15, 4, 12, 10, 6], 
              
              [6, 9, 2, 8, 12, 1, 15, 7, 14, 10, 4, 5, 11, 13, 3, 0,
               1, 2, 0, 6, 3, 10, 13, 12, 14, 9, 8, 11, 7, 15, 4, 5, 
               14, 7, 8, 9, 4, 6, 10, 11, 13, 3, 15, 0, 12, 1, 2, 5,
               10, 15, 9, 14, 2, 11, 5, 12, 1, 8, 7, 6, 0, 13, 4, 3], 
              
              [13, 12, 6, 7, 2, 1, 14, 4, 11, 0, 5, 8, 3, 10, 15, 9,
               3, 2, 1, 12, 4, 5, 10, 13, 9, 8, 14, 6, 15, 11, 7, 0, 
               7, 11, 5, 9, 8, 14, 15, 4, 2, 0, 3, 6, 12, 1, 13, 10, 
               1, 6, 4, 0, 5, 14, 12, 3, 15, 11, 10, 7, 13, 9, 8, 2], 
              
              [12, 9, 6, 14, 2, 13, 1, 11, 8, 7, 15, 0, 4, 5, 3, 10, 
               11, 7, 4, 5, 10, 13, 3, 1, 15, 12, 14, 6, 0, 2, 9, 8, 
               11, 3, 5, 6, 15, 8, 0, 2, 4, 14, 13, 7, 9, 1, 12, 10,
               5, 1, 7, 12, 10, 0, 9, 15, 13, 14, 4, 3, 11, 8, 6, 2], 
              
              [2, 0, 13, 7, 4, 1, 11, 12, 15, 9, 10, 6, 14, 8, 3, 5,
               8, 7, 15, 1, 10, 14, 2, 12, 3, 6, 9, 4, 0, 13, 5, 11, 
               2, 4, 1, 11, 14, 13, 10, 5, 6, 3, 7, 12, 0, 15, 9, 8, 
               15, 0, 10, 11, 13, 3, 4, 8, 7, 9, 12, 2, 1, 5, 6, 14]
            ]

    p_box = [19, 14, 15, 3, 10, 25, 26, 20, 23, 24, 7, 2, 18, 6, 30,29, 1, 4, 9, 8, 27, 5, 13, 0, 21, 16, 17, 22, 12, 31, 11, 28]

    def __init__(self,key=None,rounds=5):
        self.rounds = rounds
        self.key = key
        self.genKeys()

    def genKeys(self):
        RKG = RoundsKeyGenerator(self.key,self.rounds)
        self.rounds_keys = RKG.rounds_keys

    def s(self, x ,index):
        return ToyCypher.s_box[index][(((x >> 4) & 3) << 4) + (x & 15)]

    def p(self,x):
        bx = [int(_) for _ in bin(x)[2:].rjust(32, '0')]
        by = [bx[ToyCypher.p_box[i]] for i in range(32)]
        return int(''.join([str(_) for _ in by]), 2)

    def E(self,x):
        bx = bin(x)[2:].rjust(32, '0')
        by = ''
        index = -1
        for i in range(8):
            for j in range(index, index + 6):
                by += bx[j % 32]
            index += 4
        return int(by, 2)

    def F(self,x, rounds):
        x_in = bin(self.E(x) ^ self.rounds_keys[rounds])[2:].rjust(48, '0')
        y_out = ''
        for i in range(0, 48, 6):
            y_out += bin(self.s(int(x_in[i:i+6], 2), i // 6))[2:].rjust(4, '0')
        y_out = int(y_out, 2)
        y = self.p(y_out)
        return y

    def blockEnc(self , x):
        bx = bin(x)[2:].rjust(64, '0')
        l, r = int(bx[:32], 2), int(bx[32:], 2)
        for i in range(self.rounds): 
            l, r = r, l ^ self.F(r, i)
        return (l + (r << 32)) & ((1 << 64) - 1)
    
    def blockDec(self , x):
        bx = bin(x)[2:].rjust(64, '0')
        l, r = int(bx[32:], 2), int(bx[:32], 2)
        for i in range(self.rounds-1, -1 ,-1): 
            l, r = r^self.F(l, i), l
            # l, r = r, l ^ self.F(r, i)
        return (r + (l << 32)) & ((1 << 64) - 1)

    def enc(self,pt):
        pt = padding(pt)
        return b"".join([i2b(self.blockEnc(b2i(pt[i:i+8])),8) for i in range(0,len(pt),8)])

    def dec(self,ct): 
        return b"".join([i2b(self.blockDec(b2i(ct[i:i+8])),8) for i in range(0,len(ct),8)])
