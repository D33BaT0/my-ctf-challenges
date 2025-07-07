from utils import *
import os

MOD  = 0x10000000000000000000000000000000000000000000000000000000000000129
SEED = b2i(os.urandom(32))

class Users:
    def __init__(self):
        self.usernames = set()
        self.passwords = {}
        self.tokens = {}

        self.ecdhs = {}
        self.exchange_keys = {}

        self.RNG = RandomNG(MOD,SEED)
        self.x = randint(1,MOD)

    def generate_token(self,username):
        s = self.RNG.next()
        u = b2i(sha256(username).digest())
        return i2b(int((self.x * pow(s + u, -1, MOD)) % MOD),32)

    def register(self, username, password, limit = 123):
        if username in self.usernames:
            return False, b"Username already exists!"
        
        if len(self.usernames) > limit + 1: 
            return False, b"Too many accounts!"

        self.usernames.add(username)
        self.passwords[username] = password

        token = self.generate_token(username)
        self.tokens[username] = token
        if username == b'AliceIsSomeBody':
            ecdh = ECDH(self.x)
        else:
            ecdh = ECDH()

        self.ecdhs[username] = ecdh 
        
        return True, token

    def login_by_password(self,username,password):
        if username not in self.usernames:
            return False, b"Username does not exist!"

        check_password = self.passwords[username]
        if check_password == password:
            return True, b"Login successfully!"
        else:
            return False, b"Password incorrect!"

    def login_by_token(self,username,token):
        if username not in self.usernames:
            return False, b"Username does not exist!"

        check_token = self.tokens[username]
        if check_token == token:
            return True, b"Login successfully!"
        else:
            return False, b"Token incorrect!"

    def reset_password(self,username, new_password):
        if username not in self.usernames:
            return False, b"Username does not exist!"
        self.passwords[username] = new_password
        return True, b"Reset password successfully!" 

    def view_private_key(self,username):
        return i2b(self.ecdhs[username].private_key,32)

    def getsb_public_key(self,username):
        return p2b(self.ecdhs[username].public_key)

    def send_enc_msg_from_A2B(self,A,B,msg):
        if A < B:
            if A+B not in self.exchange_keys:
                ABkey = self.ecdhs[A].exchange_key(self.ecdhs[B].public_key)
                self.exchange_keys[A+B] = ABkey
            else:
                ABkey = self.exchange_keys[A+B]
        else:
            if B+A not in self.exchange_keys:
                ABkey = self.ecdhs[A].exchange_key(self.ecdhs[B].public_key)
                self.exchange_keys[B+A] = ABkey
            else:
                ABkey = self.exchange_keys[B+A]

        return enc(msg,ABkey)
