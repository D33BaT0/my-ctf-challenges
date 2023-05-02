### d3sys writeup - EN

Server implements a class `D3_ENC`,which encrypts message by `CTR-SM4` and implements Authentication mechanism by `CRT-RSA`.

#### 1st part(interaction time within 60s) :

1st menu:

```python
 ====------------------------------------------------------------------------------------------------------
 |    |              +---------------------------------------------------------------------+              | 
 |    |              |            [R]egister     [L]ogin     [T]ime     [E]xit             |              | 
 |    |              +---------------------------------------------------------------------+              | 
 ====------------------------------------------------------------------------------------------------------
```

##### Authentication Mechanism:(get_tag) 

 $block_i=msg[16*i:16*i+16],i\in[0,\text{len}(msg)//16]$  


$$
authdata_0 = init\\
authdata_{i+1} =\text{sha256}(rsa(authdata_{i}))[:32]\oplus block_i\\
tag = \text{sha256}(rsa(authdata_{-1}))[:32]
$$

##### Registration Mechanism:

Input `username`, it should satisfy length < 20. Randomly generate an 8-byte nonce. 

Get token like this: $token = \{'id':Username,\ 'admin':0,'nonce':nonce.hex(),'time':time.time()\}$ 

Server encrypts the token by `CTR-SM4` ,records the `Username` and `tag` in the dictionary and sends `username,encrypted token and nonce` to client.

##### Login Mechanism

Input `username，encrypted token`.

Server decrypts the `encrypted token`, and judges if the token satisfies followings:

- `tag`=`dict[username].tag`
- `username` in `dict.keys`
- `username = token["username"]`
- `|time-token['time']|<1`
- `admin=1`

If the token satisfies these all, you can login in as `Admin` and do more you want to do.

**Note:** Here I forgot to write `unpad`, resulting in ID lengths only a few can be taken.

##### How to Attack

We can find that $authdata_{i+1} =\text{sha256}(rsa(authdata_{i}))[:32]\oplus block_i$ .Because its encrypting model is `CTR`, which can be regarded as `stream cipher`. 

Then you can change the block of plaintext by `xor`. But the `tag` can't be changed, so you can construct `username` to get an insensitive block.

1. choose len(`username`)=15, it makes nonce occupy a block(which is insensitive block).
2. xor `admin` from 0 to 1
3. xor nonce block makes the `authdata` after the nonce invariant.
4. `json.loads(plain)` => `plain` needs to be in `UTF-8` characters, so should brute for some times(about 10 times).

scripts:

```python
from Crypto.Util.number import bytes_to_long,long_to_bytes
from hashlib import sha256
from pwn import *

def xor(a,b):
    return bytes([i^j for i,j in zip(a,b)])

class Forgery:
    def __init__(self , ID , nonce , cipher,n,e  ,authdate , the_time):
        plain = b'{"id": "' + ID + b'", "admin": 0, "nonce": "' + nonce + b'", "time": ' + str(the_time).encode() + b'}\n\n\n\n\n\n\n\n\n\n'
        self.authdate = authdate
        self.pub = n,e
        self.plain_state = [(plain[i*16:(i+1)*16]) for i in range(len(plain)//16)]
        self.cipher_state = [(cipher[i*16:(i+1)*16]) for i in range(len(cipher)//16)]
    
    def do_forgery(self):
        new_plain_state , new_cipher_state = self.xor_admin_to_true()
        new_cipher_state = self.xor_nonce_for_mac(new_plain_state,new_cipher_state)
        new_cipher = new_cipher_state[0] + new_cipher_state[1] + new_cipher_state[2] + new_cipher_state[3] + new_cipher_state[4] + new_cipher_state[5]
        return new_cipher

    def crtencrypt(self,m):
        n,e = self.pub
        return pow(m,e,n)

    def _mac(self,msg):
        auth_date = self.authdate
        msg_state = [bytes_to_long(msg[i*16:(i+1)*16]) for i in range(len(msg)//16)]
        auth_date = bytes_to_long(sha256(str(self.crtencrypt(auth_date)).encode()).digest()[:16])
        for plain_state in msg_state:
            auth_date ^= plain_state
            auth_date = bytes_to_long(sha256(str(self.crtencrypt(auth_date)).encode()).digest()[:16])
        return auth_date

    def xor_admin_to_true(self):# 0 => 1
        new_cipher_state = []
        new_plain_state = []
        for i in range(2):
            new_plain_state.append(self.plain_state[i])
            new_cipher_state.append(self.cipher_state[i])
        new_plain_state.append(xor(self.plain_state[2],b'\x00' * 3 + b'\x01' + b'\x00' *12 ))
        new_cipher_state.append(xor(self.cipher_state[2],b'\x00' * 3 + b'\x01' + b'\x00' *12 ))
        for i in range(3):
            new_plain_state.append(self.plain_state[i+3])
            new_cipher_state.append(self.cipher_state[i+3])
        return new_plain_state , new_cipher_state

    def xor_nonce_for_mac(self,new_plain_state,new_cipher_state):
        old_plain_part_msg = self.plain_state[0] + self.plain_state[1] + self.plain_state[2]
        new_plain_part_msg = new_plain_state[0] + new_plain_state[1] + new_plain_state[2]
        oppm_mac = self._mac(old_plain_part_msg)
        nppm_mac = self._mac(new_plain_part_msg)

        new_cipher_nonce_part = new_cipher_state[3]

        the_new_plain_state_nonce = (long_to_bytes(oppm_mac ^ bytes_to_long(new_plain_state[3]) ^ nppm_mac))

        new_cipher_state[3] = xor(xor(new_cipher_nonce_part,self.plain_state[3]),the_new_plain_state_nonce)
        return (new_cipher_state)

def get_time(io):
    io.recvuntil(b'option >')
    io.sendline(b'T')
    io.recvuntil(b'[D^3] D^3\' clock shows ')
    the_time = int(io.recvline().strip())
    return the_time

def register_get_encrypt_token(io,ID):
    io.recvuntil(b'option >')
    io.sendline(b'R')
    io.recvuntil(b"[D^3] USERNAME:")
    io.sendline(ID)
    io.recvuntil(b'token is ')
    encrypted_token = io.recvuntil(b'& nonce is ')[:-11]
    nonce = io.recvline().strip()
    return encrypted_token,nonce

def login(io,ID,c):
    io.recvuntil(b'option >')
    io.sendline(b'L')
    io.recvuntil(b'[D^3] USERNAME:')
    io.sendline(ID)
    io.recvuntil(b'[D^3] Token:')
    io.sendline(c.encode())

timees = 0
while 1:
    io = remote("", )
    io.recvuntil(b'[D^3] My initial Authdate is ')
    auth_date = io.recvline().strip().decode()
    io.recvuntil(b'[D^3] My Auth pubkey is ')

    n,e = eval(io.recvline().strip())

    ID = b'd33b470zuishuai' 
    the_time = get_time(io)
    cipher,nonce = register_get_encrypt_token(io,ID)

    auth_date = bytes.fromhex(auth_date)
    cipher,nonce = bytes.fromhex(cipher.decode()),bytes.fromhex(nonce.decode())
    counter = cipher[:16]
    cipher = cipher[16:]

    forgery = Forgery(ID,nonce.hex().encode(),cipher,n,e,bytes_to_long(auth_date),the_time)
    c = forgery.do_forgery()
    c = (counter+c).hex()

    login(io,ID,c)
    msg = io.recvline()
    print(msg.strip().decode())
    if msg!= b'[D^3] Sorry,try again plz..\n' and msg != b'b"[D^3] Something Wrong...quiting...."\n'\
        and msg != b'[D^3] Ouch! HACKER? Get Out!\n' and msg != b'[D^3] Change name?\n' and \
            msg != b'[D^3] oh...no...out....\n': # msg!= b'Time Error!\n':
        break
    time.sleep(0.5)
    io.close()
    timees += 1
print(timees+1)
```

#### 2nd part(login in as admin):

menu:

```python
 ====------------------------------------------------------------------------------------------------------=
 |    |              +---------------------------------------------------------------------+              | 
 |    |              |            [G]et_dp_dq     [F]lag     [T]ime     [E]xit             |              | 
 |    |              +---------------------------------------------------------------------+              | 
 ====------------------------------------------------------------------------------------------------------=
```

The decryption exponents of CRT-RSA is additionally blinded, and only the lsb of $d_p, d_q$ and the encrypted flag can be obtained.

The content involved here can be implemented by reading the paper of AC22 [1] or EC22 [2], but here I tested the `tk `script [3] on Github. Using the parameters given in the paper, but I don't know if the method I used is wrong, I can only go to 170bits, so I wrote one with General's strategy.

In the players' write-ups, I saw that most of the solved methods were directly changed to the script.

I also limited the bound of coppersmith script from defund[4], but there were still players who ran out by high parameters.

**scripts**:

```python
import itertools

def poly_to_matrix(G,e,bounds,m):
    monomials = []
    for polynomial in G:
        for monomial in polynomial.monomials():
            if monomial not in monomials:
                monomials.append(monomial)

    print(monomials)
    mm = len(G)
    nn = len(monomials)
    B = Matrix(ZZ, mm,nn)
    
    for ii in range(mm):
        for jj in range(0, nn):
            if monomials[jj] in G[ii].monomials():
                B[ii, jj] = G[ii].monomial_coefficient(monomials[jj]) * monomials[jj](*bounds)
    B = B.dense_matrix()
    B = B.LLL()
    print("LLL done")
    return B,vector(monomials)

def find_roots2(BB,monomials,bounds):
    PR = PolynomialRing(ZZ,"x",len(bounds))
    a_varis = PR.gens() 
    all_pol = []
    mm,nn = BB.dimensions()
    for pol1_idx in range(mm):
        pol1 = 0
        for jj in range(nn):
            pol1 += monomials[jj](*a_varis) * BB[pol1_idx, jj] / monomials[jj](*bounds)
        if pol1 == 0:
            continue
        all_pol.append(pol1)
    print(len(all_pol))
    choose_pol = all_pol[:len(all_pol)//4 - 5]
    I = ideal(choose_pol)
    print(I.dimension())
    GB = I.groebner_basis()
    print(f"Final_GB({len(GB)}):")
    print(GB)
    print('------' * 32)

    b_varis = var(",".join(f"x{i}" for i in range(len(bounds))))
    print('roots:')
    res = solve([h_i(*b_varis) for h_i in GB], *b_varis , solution_dict=True)
    roots = []
    for _ in res:
        tmp = list(_.values())
        if 0 in tmp:
            continue
        roots.append(tmp)
    
    return roots

def small_roots(f, bounds, m, d):
    R = f.base_ring()
    N = R.cardinality()
    f = f.change_ring(ZZ)

    G = Sequence([], f.parent())
    for i in range(m+1):
        base = N^(m-i) * f^i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)
    B, monomials = poly_to_matrix(G,N,bounds,m)
    return B,monomials,bounds

nbit = 1024
blind_bit = 128
unknownbit = 193

n = 
e = 
dP_ = 
dQ_ = 
c = 

i2 = 2**(nbit // 2 + blind_bit - unknownbit)
A = (-e**2*dP_*dQ_+dP_*e+dQ_*e-1)

PR.<x,y> = PolynomialRing(Zmod(i2 * e))

X,Y = [int(2 ^ blind_bit) * e for i in range(2)]
f = (n-1) * x * y -(e*dQ_-1) * x-(e*dP_-1) * y + A

aaa = gcd(n-1,i2)
bbb = gcd(e*dQ_-1,i2)
ccc = gcd(e*dP_-1,i2)

if aaa == max([aaa,bbb,ccc]):
    f_ = f * int(pow((n-1)//gcd(n-1,i2),-1,i2*e))
elif bbb == max([aaa,bbb,ccc]):
    f_ = f * int(pow((e*dQ_-1)//gcd(e*dQ_-1,i2),-1,i2*e))
else:
    f_ = f * int(pow((e*dP_-1)//gcd(e*dP_-1,i2),-1,i2*e))

print("start first copper")
B,monomials,bounds = small_roots(f_,[X,Y],m=8,d=10)
roots = find_roots2(B,monomials,bounds)

k,l = roots[0]
k,l = int(k),int(l)
print(f'get k,l:{[k,l]}')
try:
    PR.<xx> = PolynomialRing(Zmod(n*k))
    ap = (e*dP_+k-1) * pow((e*i2),-1,k*n)

    f = xx + Integer(ap)
    X = 2 ^ unknownbit

    print("start second copper")
    xxx = f.small_roots(X,beta=0.4,epsilon=0.02)[0]
    print("second copper down")

    p = gcd(int(f(xxx)),n)
    q = n // p

    d = int(inverse_mod(e,(p-1)*(q-1)))
    m = bytes.fromhex(hex(int(pow(c,d,n)))[2:])
    print(m)
except:
    PR.<xx> = PolynomialRing(Zmod(n*l))
    aq = (e*dQ_+l-1) * pow((e*i2),-1,l*n)

    f = xx + Integer(aq)
    X = 2 ^ unknownbit

    print("start second copper")
    xxx = f.small_roots(X,beta=0.4,epsilon=0.02)[0]
    print("second copper down")

    p = gcd(int(f(xxx)),n)
    q = n // p

    d = int(inverse_mod(e,(p-1)*(q-1)))
    m = bytes.fromhex(hex(int(pow(c,d,n)))[2:])
    print(m)
```

#### References

[1]: Zhou Y, van de Pol J, Yu Y, et al. A Third is All You Need: Extended Partial Key Exposure Attack on CRT-RSA with Additive Exponent Blinding[C]//Advances in Cryptology–ASIACRYPT 2022: 28th International Conference on the Theory and Application of Cryptology and Information Security, Taipei, Taiwan, December 5–9, 2022, Proceedings, Part IV. Cham: Springer Nature Switzerland, 2023: 508-536.

[2]: May A, Nowakowski J, Sarkar S. Approximate divisor multiples–factoring with only a third of the secret CRT-exponents[C]//Advances in Cryptology–EUROCRYPT 2022: 41st Annual International Conference on the Theory and Applications of Cryptographic Techniques, Trondheim, Norway, May 30–June 3, 2022, Proceedings, Part III. Cham: Springer International Publishing, 2022: 147-167.

[3]: [juliannowakowski/crtrsa-small-e-pke: Implementation of "Approximate Divisor Multiples - Factoring with Only a Third of the Secret CRT-Exponents" (github.com)](https://github.com/juliannowakowski/crtrsa-small-e-pke)

[4]: [coppersmith/coppersmith.sage at master · defund/coppersmith (github.com)](https://github.com/defund/coppersmith)