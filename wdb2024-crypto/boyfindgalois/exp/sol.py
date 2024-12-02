from pwn import *

def pad(msg:bytes,length:int):
    return msg.rjust(length,b'\0')
"""
get a code

def check(code):
    p = 3**40 + 118
    n = 1337
    # assert len(code)<100
    for c in code:
        if c == '+':
            n += n
        elif c == '*':
            n *= n
        n %= p
    return int(n)

p = 3**40 + 118
F = GF(p)

n = F(1337)
target = F(31337)

def get_code(bins):
    codes = ""
    for i in range(len(bins)):
        if bins[i] == "1":
            codes += "+*"
        elif bins[i] == "0" :
            codes += "*"
    return codes

from tqdm import trange
for mul_times in trange(1337):
    A = target/(n**int(pow(2,mul_times,p-1)))
    try:
        ord_2 = bin(A.log(F(2)))[2:]
        if mul_times < len(ord_2):
            continue
        ord_2 = (mul_times + 1 - len(ord_2))*"0"+ord_2 
        assert n**int(pow(2,mul_times,p-1)) * pow(2,int(ord_2,2),p) == target  
        ret = get_code(ord_2)[:-1] 
        if check(ret) == 31337:
            print(len(ret),ret)  
            break
    except:
        continue"""

from bfv.batch_encoder import BatchEncoder
from bfv.bfv_encryptor import BFVEncryptor
from bfv.bfv_decryptor import BFVDecryptor
from bfv.bfv_key_generator import BFVKeyGenerator
from bfv.bfv_parameters import BFVParameters 
from util.polynomial import Polynomial
from util.ciphertext import Ciphertext

codes = pad(b"**+**+****+*+*****+*+*+**+****+**+*****+*+***+*+*+****+*+*+*+*+*+*+**+***+*+**+*+*+*+***+*+*",128)
degree = 128 
plain_modulus = 257
ciph_modulus = 0x9000000000000
params = BFVParameters(poly_degree=degree,
                        plain_modulus=plain_modulus,
                        ciph_modulus=ciph_modulus)

scalar_multi = ciph_modulus // plain_modulus
encoder = BatchEncoder(params)
io = remote("192.168.0.144",11422)

io.recvuntil(b"Option: ")
io.sendline(b"E")
io.recvuntil(b"plain = ")
plaintext = bytes.fromhex(io.recvline().strip().decode())
io.recvuntil(b"cipher = ")
cipher = (io.recvline() + io.recvline()).decode()

def parse_cipher(cipher):
    c0,c1 = cipher.split("c0: ")[1].split(" + c1: ")
    c0_l,c1_l = [],[]
    for i in range(127,1,-1):
        c0i,c0 = c0.split(f"x^{i} + ")
        c1i,c1 = c1.split(f"x^{i} + ")
        c0_l.append(int(c0i))
        c1_l.append(int(c1i))
    c0i,c0 = c0.split(f"x + ")
    c1i,c1 = c1.split(f"x + ")
    c0_l.append(int(c0i))
    c0_l.append(int(c0))
    c1_l.append(int(c1i))
    c1_l.append(int(c1))
    return c0_l[::-1],c1_l[::-1]

c0,c1 = parse_cipher(cipher) 
c0,c1 = Polynomial(degree,c0),Polynomial(degree,c1)
knownp = encoder.encode(list(plaintext))
knownp_scaled_message = knownp.poly.scalar_multiply(scalar_multi, ciph_modulus)

target = encoder.encode(list(codes))
target_scaled_message = target.poly.scalar_multiply(scalar_multi, ciph_modulus)
need_add = knownp_scaled_message.scalar_multiply(-1,ciph_modulus).add(target_scaled_message,ciph_modulus)
c0 = c0.add(need_add) 
c0 = str(list(c0.coeffs))[1:-1] 
c1 = str(list(c1.coeffs))[1:-1]
io.recvuntil(b"Option: ")
io.sendline(b"D")
io.recvuntil(b"c0: ")
io.sendline(c0.encode())
io.recvuntil(b"c1: ")
io.sendline(c1.encode())
io.interactive()