from random import randint
from hashlib import md5, sha256
from Crypto.Cipher import AES

def pad(msg):
    return msg + bytes([i for i in range(16 - int(len(msg) % 16))])

def i2b(i,l):
    return int.to_bytes(i,length=l,byteorder='big')

def b2i(b):
    return int.from_bytes(b,byteorder='big')

def p2b(P):
    return i2b(P[0],32) + i2b(P[1],32)

def b2p(m):
    return (b2i(m[:32]),b2i(m[32:]))

def enc(msg,key):
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(pad(msg))

class RandomNG:
    def __init__(self, mod, seed):
        self.coeffs = [randint(1,mod) for _ in range(121)]
        self.mod = mod
        self.state = seed 

    def next(self):
        old_state = int(self.state)
        self.state = sum(coeff * self.state**i for i,coeff in enumerate(self.coeffs)) % self.mod
        return old_state

class Curve: 
    def __init__(self):
        # Nist p-256
        self.p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
        self.a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
        self.b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
        self.G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 
                  0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
        self.n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

    def add(self,P, Q):
        if (P == (0, 0)):
            return Q
        elif (Q == (0, 0)):
            return P
        else: 
            x1, y1 = P
            x2, y2 = Q
            if ((x1 == x2) & (y1 == -y2)):
                return ((0, 0))
            else:
                if (P != Q):
                    l = (y2 - y1) * pow(x2 - x1, -1, self.p)
                else:
                    l = (3 * (x1**2) + self.a) * pow(2 * y1, -1, self.p)
            x3 = ((l**2) - x1 - x2) % self.p
            y3 = (l * (x1 - x3) - y1) % self.p
            return x3, y3

    def mul(self, n , P):
        Q = P
        R = (0, 0)
        while (n > 0):
            if (n % 2 == 1):
                R = self.add(R, Q)
            Q = self.add(Q, Q)
            n = n // 2
        return R

class ECDH:
    def __init__(self, privkey=None):
        self.curve = Curve()
        if privkey is not None:
            self.private_key = int(sha256(str(privkey).encode()).hexdigest(), 16) % self.curve.n
        else:
            self.private_key = randint(1,self.curve.n)
        self.public_key  = self.curve.mul(self.private_key, self.curve.G)

    def exchange_key(self,others_publickey):
        return md5(str(self.curve.mul(self.private_key,others_publickey)).encode()).digest()

def transfer_A2B(USER,A,B,msg,enc=False):
    if enc == False:
        return b'[' + A + b"] to [" + B + b"]:" + msg+b'\n'
    else:
        return b'[' + A + b"] to [" + B + b"]: " + USER.send_enc_msg_from_A2B(A,B,msg).hex().encode()+b'\n'
