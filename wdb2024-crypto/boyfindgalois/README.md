# boyfindgalois

## Category

Crypto

## Difficulty

Medium

## writeups

看附件server.py部分，得知交互只有2次机会：

1. 加密任意128长度的随机字符串并给出明密文；
2. 输入密文并且需要让服务端解密成功获得能过check的部分的消息

所以第一步我们实际上需要通过一组已知明密文攻击能伪造任意明文，通过审计pyfhe源码可知前述需要部分的一些初始化操作，使得可以使用Bfv这个加密解密，其中加密的话需要公钥才能加密，但是实际上没有公钥可以获得。

加密后得到的明文对应的密文对是：
$$
(\vec{v}\cdot\vec{p_0}+\vec{m_0},\vec{v}\cdot \vec{p_1})
$$
可以发现实际上对随机选取的向量v并不敏感，因此是可以通过已知明文的一组密文对构造出来这样的一组信息
$$
(\vec{v}\cdot\vec{p_0}+\vec{m_0}+(\vec{m_1}-\vec{m_0}),\vec{v}\cdot \vec{p_1})
$$
m1就是想要构造的明文，而m0是给出的一组明文，通过此我们可以并不需要去看解密如何实现就能直接构造出任意明文对应这组bfv的加解密实例的密文。

成功构造之后还需要通过check

```python
def check(msg):
    p,n = 3**40 + 118, 1337 
    for c in msg:
        if c == '+': n += n
        elif c == '*': n *= n
        n %= p
    return n == 31337
```

对其分析+是乘2 ，\*是平方，所以需要 2^a \* n^b = target；b 一定是2的幂次的，所以我可以爆破b，去求2的dlp算出这个a。然后我可以给个只有一种可能的规则，比如说给每个bit 1是\*+  然后0就给\*即可通过check

exp本地实现脚本如下：

```python
"""
得到一组消息能过check的

def check(msg):
    p,n = 3**40 + 118, 1337 
    for c in msg:
        if c == '+': n += n
        elif c == '*': n *= n
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
def pad(msg:bytes,length:int):
    return msg.rjust(length,b'\0')

codes = pad(b"**+**+****+*+*****+*+*+**+****+**+*****+*+***+*+*+****+*+*+*+*+*+*+**+***+*+**+*+*+*+***+*+*",128)
degree = 128 
plain_modulus = 257
ciph_modulus = 0x9000000000000
params = BFVParameters(poly_degree=degree,
                        plain_modulus=plain_modulus,
                        ciph_modulus=ciph_modulus)

scalar_multi = ciph_modulus // plain_modulus
encoder = BatchEncoder(params)


plaintext = bytes.fromhex("....")

cipher = """
c0: ....
 + c1: ..."""

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
print(c0.coeffs) 
print(c1.coeffs) 
```

