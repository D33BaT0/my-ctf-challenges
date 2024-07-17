from collections import Counter
from tqdm import tqdm
from Crypto.Util.number import getRandomNBitInteger
from cypher import *

sbox =[[15, 2, 7, 10, 4, 3, 11, 0, 13, 8, 6, 12, 14, 5, 1, 9, 5, 8, 6, 14, 10, 12, 2, 13, 1, 4, 11, 7, 9, 15, 3, 0, 4, 7, 0, 10, 15, 3, 1, 13, 14, 8, 2, 9, 6, 11, 5, 12, 2, 12, 5, 3, 7, 10, 11, 0, 4, 14, 9, 6, 13, 1, 8, 15], [6, 8, 10, 15, 13, 14, 12, 9, 1, 3, 0, 2, 11, 5, 7, 4, 2, 15, 12, 9, 8, 6, 14, 7, 5, 13, 4, 11, 3, 0, 10, 1, 13, 15, 7, 10, 1, 6, 5, 14, 12, 11, 9, 0, 2, 4, 8, 3, 5, 12, 15, 0, 1, 3, 13, 7, 11, 4, 6, 10, 8, 9, 14, 2], [1, 10, 7, 13, 5, 2, 6, 3, 0, 11, 12, 4, 8, 14, 15, 9, 0, 4, 7, 12, 9, 3, 10, 14, 11, 1, 5, 8, 13, 2, 15, 6, 11, 1, 6, 12, 15, 9, 2, 8, 5, 0, 4, 14, 13, 10, 3, 7, 2, 11, 14, 10, 15, 8, 5, 13, 9, 7, 4, 1, 6, 0, 3, 12], [13, 1, 6, 2, 9, 14, 10, 0, 7, 3, 15, 8, 12, 5, 11, 4, 11, 0, 7, 9, 6, 14, 5, 10, 8, 12, 15, 13, 3, 1, 4, 2, 13, 2, 0, 11, 5, 4, 12, 6, 10, 3, 1, 9, 7, 15, 8, 14, 7, 1, 3, 5, 0, 9, 2, 11, 8, 13, 14, 15, 4, 12, 10, 6], [6, 9, 2, 8, 12, 1, 15, 7, 14, 10, 4, 5, 11, 13, 3, 0, 1, 2, 0, 6, 3, 10, 13, 12, 14, 9, 8, 11, 7, 15, 4, 5, 14, 7, 8, 9, 4, 6, 10, 11, 13, 3, 15, 0, 12, 1, 2, 5, 10, 15, 9, 14, 2, 11, 5, 12, 1, 8, 7, 6, 0, 13, 4, 3], [13, 12, 6, 7, 2, 1, 14, 4, 11, 0, 5, 8, 3, 10, 15, 9, 3, 2, 1, 12, 4, 5, 10, 13, 9, 8, 14, 6, 15, 11, 7, 0, 7, 11, 5, 9, 8, 14, 15, 4, 2, 0, 3, 6, 12, 1, 13, 10, 1, 6, 4, 0, 5, 14, 12, 3, 15, 11, 10, 7, 13, 9, 8, 2], [12, 9, 6, 14, 2, 13, 1, 11, 8, 7, 15, 0, 4, 5, 3, 10, 11, 7, 4, 5, 10, 13, 3, 1, 15, 12, 14, 6, 0, 2, 9, 8, 11, 3, 5, 6, 15, 8, 0, 2, 4, 14, 13, 7, 9, 1, 12, 10, 5, 1, 7, 12, 10, 0, 9, 15, 13, 14, 4, 3, 11, 8, 6, 2], [2, 0, 13, 7, 4, 1, 11, 12, 15, 9, 10, 6, 14, 8, 3, 5, 8, 7, 15, 1, 10, 14, 2, 12, 3, 6, 9, 4, 0, 13, 5, 11, 2, 4, 1, 11, 14, 13, 10, 5, 6, 3, 7, 12, 0, 15, 9, 8, 15, 0, 10, 11, 13, 3, 4, 8, 7, 9, 12, 2, 1, 5, 6, 14]]
pbox = [19, 14, 15, 3, 10, 25, 26, 20, 23, 24, 7, 2, 18, 6, 30,29, 1, 4, 9, 8, 27, 5, 13, 0, 21, 16, 17, 22, 12, 31, 11, 28]

def s(x ,index): 
    return sbox[index][(((x >> 4) & 3) << 4) + (x & 15)]

def p(x):
    bx = [int(_) for _ in bin(x)[2:].rjust(32, '0')]
    by = [bx[pbox[i]] for i in range(32)]
    return int(''.join([str(_) for _ in by]), 2)

def E(x):
    bx = bin(x)[2:].rjust(32, '0')
    by = ''
    index = -1
    for i in range(8):
        for j in range(index, index + 6):
            by += bx[j % 32]
        index += 4
    return int(by, 2)

def inv_p(x):
    x_bin = [int(_) for _ in bin(x)[2:].rjust(32, '0')]
    y_bin = [0]*32
    for i in range(32):
        y_bin[pbox[i]] = x_bin[i]
    y = int(''.join([str(_) for _ in y_bin]), 2)
    return y

def inverse_right(res, shift, bits=48):
    tmp = res
    for i in range(bits // shift):
        tmp = res ^ tmp >> shift
    return tmp

def inverse_left_mask(res, shift, mask, bits=48):
    tmp = res
    for i in range(bits // shift):
        tmp = res ^ tmp << shift & mask
    return tmp

def inv_key(key,rounds = 5):
    for _ in range(rounds):
        key = inverse_right(key,3)
        key = inverse_left_mask(key,13,0x33d0ea51c332)
        key = inverse_left_mask(key,21,0xb470deadbeef)
        key = inverse_right(key,14)
    return key

from pwn import *

while 1:
    io = remote("192.168.1.107",11420)# process(["python3","../src/oracle.py"]) 
    candidate_keys = [Counter() for _ in range(8)]
    pairs = [] 
    
    def get_enc(io,msg):
        io.recvuntil(":👾O👾:".encode())
        io.sendline(b"E")
        io.recvuntil("You will not kill my allies💕:".encode()).decode()
        io.sendline(msg.hex().encode())
        io.recvuntil("Open up the sky👽:".encode()).decode()
        cip = bytes.fromhex(io.recvline().strip().decode())
        return cip

    for _ in range(0x16):
        p1 = getRandomNBitInteger(64)
        p2 = p1 ^ 0x0000000100000006

        c1 = b2i(get_enc(io,i2b(p1,8)))# b2i(toycipher.enc(i2b(p1,8)))
        c2 = b2i(get_enc(io,i2b(p2,8)))# b2i(toycipher.enc(i2b(p2,8)))

        pairs.append([[p1,p2],[c1,c2]])

    for pair in pairs:
        c1, c2 = pair[1]
        l1, l2 = c1 >> 32, c2 >> 32
        r1, r2 = c1 & 0xffffffff, c2 & 0xffffffff 
        l1,r1 = r1,l1
        l2,r2 = r2,l2

        F_ = r1 ^ r2 ^ 1
        F_ = inv_p(F_) # xor of the two outputs of sbox, 32bit

        Ep1 = E(l1) # 48bit
        Ep2 = E(l2) # 48bit

        for i in range(8):
            inp1 = (Ep1 >> ((7-i)*6)) & 0b111111   # 6bit
            inp2 = (Ep2 >> ((7-i)*6)) & 0b111111   # 6bit
            out_xor = (F_ >> ((7-i)*4)) & 0b1111   # 4bit
            for keyi in range(2**6):
                if s(inp1^keyi, i) ^ s(inp2^keyi, i) == out_xor:
                    candidate_keys[i][keyi] += 1

    key8s = []
    for _ in range(8):
        keytmp = []
        candidate_i = candidate_keys[_].most_common(6)
        keytimesmax = candidate_i[0][1]
        keyvalssmax = candidate_i[0][0]
        for keyval,keytimes in candidate_i:
            if keytimesmax >= 6:
                if keytimesmax>int(1.5*keytimes):
                    keytmp.append(keyvalssmax)
                    break
            keytmp.append(keyval)
        key8s.append(keytmp)

    def get_RealKey(key8s):
        for key0 in key8s[0]:
            for key1 in key8s[1]:
                for key2 in key8s[2]:
                    for key3 in key8s[3]:
                        for key4 in key8s[4]:
                            for key5 in key8s[5]:
                                for key6 in key8s[6]:
                                    for key7 in key8s[7]:
                                        keyi = [key0,key1,key2,key3,key4,key5,key6,key7]
                                        key8 = int(''.join(bin(_)[2:].rjust(6,'0') for _ in keyi),2)
                                        realkey = inv_key(key8)
                                        [p0,p1],[c0,c1] = pairs[0]
                                        ty = ToyCypher(realkey)
                                        if b2i(ty.enc(i2b(p1,8))) == c1 and b2i(ty.enc(i2b(p0,8))) == c0 :
                                            RealKey = i2b(realkey,6)
                                            return RealKey

    realkey = get_RealKey(key8s)
    if realkey != None:
        print(realkey) 
        break
    io.close()

def get_random_cipher(io,key):
    toycipher = ToyCypher(b2i(key))
    io.recvuntil(":👾O👾:".encode())
    io.sendline(b"G")
    io.recvuntil("😈:".encode())
    cip = bytes.fromhex(io.recvline().strip().decode())
    print(len(cip))
    plain = toycipher.dec(cip)
    output = []
    for ind in range(len(plain)):
        plaini = plain[ind]
        tmpi = []
        for ci in range(4):
            tmpi.append(plaini&3)
            plaini >>= 2
        tmpi = tmpi[::-1]
        output.extend(tmpi)    
    return output

states = get_random_cipher(io,realkey)

from tqdm import tqdm

class MT19937:
	def __init__(self, seed):
		(MT19937.w, MT19937.n, MT19937.m, MT19937.r) = (32, 624, 397, 31)
		MT19937.a = 0x9908B0DF
		(MT19937.u, MT19937.d) = (11, 0xFFFFFFFF)
		(MT19937.s, MT19937.b) = (7, 0x9D2C5680)
		(MT19937.t, MT19937.c) = (15, 0xEFC60000)
		MT19937.l = 18
		self.states = [seed]
		MT19937.lowerMask = (1 << MT19937.r) - 1
		MT19937.mask = (1 << MT19937.w) - 1
		MT19937.upperMask = MT19937.mask ^ MT19937.lowerMask
		self.index = MT19937.n
		MT19937.f = 1812433253

		for i in range(1, self.n):
			self.states.append(self.mask & (i + self.f * (self.states[i-1] ^ (self.states[i-1] >> (self.w - 2)))))

	def temper(self,num):
		num = num ^ ((num >> MT19937.u) & MT19937.d)
		num = num ^ ((num << MT19937.s) & MT19937.b)
		num = num ^ ((num << MT19937.t) & MT19937.c)
		num = num ^ (num >> MT19937.l)
		return num
		
	def rand(self):
		if self.index >= MT19937.n:
			self.twist()
		y = self.states[self.index]
		self.index += 1
		return self.temper(y)

	def twist(self):
		for i in range(MT19937.n):
			x = (self.states[i] & MT19937.upperMask) ^ (self.states[(i + 1) % MT19937.n] & MT19937.lowerMask)
			xA = x >> 1
			if x & 1:
				xA = xA ^ self.a

			self.states[i] = self.states[(i + MT19937.m) % MT19937.n] ^ xA

		self.index = 0

class bitwiseMT19937:
    def __init__(self):
        self.states = [[1 << (i * 32 + j) for j in range(32)] for i in range(MT19937.n)]
        self.index = MT19937.n

    def temper(self, num):
        ret = num[:]
        for i in range(32):
            if (MT19937.d >> i) & 1:
                if i + MT19937.u < 32:
                    ret[i] ^= ret[i + MT19937.u]

        for i in range(31, -1, -1):
            if (MT19937.b >> i) & 1:
                if i - MT19937.s >= 0:
                    ret[i] ^= ret[i - MT19937.s]

        for i in range(31, -1, -1):
            if (MT19937.c >> i) & 1:
                if i - MT19937.t >= 0:
                    ret[i] ^= ret[i - MT19937.t]
                    
        for i in range(32):
            if i + MT19937.l < 32:
                ret[i] ^= ret[i + MT19937.l] 
        return ret
        
    def rand(self):
        if self.index >= MT19937.n:
            self.twist()
        y = self.states[self.index]
        self.index += 1
        return self.temper(y)

    def twist(self):
        for i in range(MT19937.n):
            x = self.states[(i + 1) % MT19937.n][:-1] + self.states[i][-1:]
            xA = x[1:] + [0]
            for t in range(32):
                if (MT19937.a >> t) & 1:
                    xA[t] ^= x[0] 

            for t in range(32):
                self.states[i][t] = self.states[(i + MT19937.m) % MT19937.n][t] ^ xA[t] 
        self.index = 0

def count(x):
    ret = 0
    for i in range(20000):
        ret ^= ((x >> i) & 1)
    return ret

TOTAL_BITS = 19968

linear_base = [(-1, -1) for _ in range(TOTAL_BITS)]
total = 0

def add(bits, output):
    global total
    while bits:
        idx = bits.bit_length() - 1
        if linear_base[idx] == (-1, -1):
            linear_base[idx] = (bits, output)
            total += 1
            return
        else:
            bits ^= linear_base[idx][0]
            output ^= linear_base[idx][1]

rngg = MT19937(9487)
bitRng = bitwiseMT19937()

for i in tqdm(range(10000)):
    bitrand = bitRng.rand() 
    output = states[i]
    add(bitrand[-2],    (output)&1)
    add(bitrand[-1], (output>>1)&1)

for i in range(TOTAL_BITS):
    if linear_base[i] == (-1, -1): continue
    assert (linear_base[i][0] & ((1 << 31) - 1)) == 0
    
for i in tqdm(range(TOTAL_BITS)):
    if linear_base[i] == (-1, -1):
        linear_base[i] = (1 << i, 0)
        continue

    mask = linear_base[i][0] ^ (1 << i)
    while mask:
        idx = mask.bit_length() - 1
        linear_base[i] = (linear_base[i][0] ^ linear_base[idx][0], linear_base[i][1] ^ linear_base[idx][1])
        mask ^= (1 << idx)

for i in range(TOTAL_BITS):
    assert linear_base[i][0] == (1 << i)

stateLong = sum((1 << i) * linear_base[i][1] for i in range(TOTAL_BITS))
states = []

for i in range(MT19937.n):
    states.append(stateLong & ((1 << 32) - 1))
    stateLong >>= 32

rngg.states = states[:]

for i in range(10016):
    rngg.rand()

plain = 0
for _ in range(32):
    plain <<= 2
    plain  += rngg.rand() >> 30

io.recvuntil(":👾O👾:".encode())
io.sendline(b"F")
io.recvuntil("Seek them out:".encode())
io.sendline(ToyCypher(b2i(realkey)).enc(i2b(plain,8)).hex().encode())
io.interactive()