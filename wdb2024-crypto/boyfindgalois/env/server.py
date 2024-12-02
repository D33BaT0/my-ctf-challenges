from bfv.batch_encoder import BatchEncoder
from bfv.bfv_encryptor import BFVEncryptor
from bfv.bfv_decryptor import BFVDecryptor
from bfv.bfv_key_generator import BFVKeyGenerator
from bfv.bfv_parameters import BFVParameters 
from util.polynomial import Polynomial
from util.ciphertext import Ciphertext
from secret import flag
import os

degree = 128 
plain_modulus = 257
ciph_modulus = 0x9000000000000

def unpad(msg):
    for i in range(len(msg)):
        if msg[i] != 0: 
            return bytes(msg[i:])

def init(degree,plain_modulus,ciph_modulus):
    params = BFVParameters(poly_degree=degree,
                            plain_modulus=plain_modulus,
                            ciph_modulus=ciph_modulus)
    encoder = BatchEncoder(params)
    key_generator = BFVKeyGenerator(params)

    public_key = key_generator.public_key
    secret_key = key_generator.secret_key
    
    encryptor = BFVEncryptor(params, public_key)
    decryptor = BFVDecryptor(params,secret_key)
    return encryptor,decryptor,encoder

def check(msg):
    p,n = 3**40 + 118, 1337 
    for c in msg:
        if c == '+': n += n
        elif c == '*': n *= n
        n %= p
    return n == 31337

def main():
    encryptor,decryptor,encoder = init(degree,plain_modulus,ciph_modulus)
    for _ in range(2):
        option = input("Option: ")[:1].upper()
        if option == "E":
            msg = os.urandom(degree)
            encoded_msg = encoder.encode(list(msg))
            cipher = encryptor.encrypt(encoded_msg)
            print(f"plain = {msg.hex()}\ncipher = {cipher}")

        elif option == "D":
            c0 = Polynomial(degree,list(map(int,input("c0: ")
                                            .strip().split(", "))))

            c1 = Polynomial(degree,list(map(int,input("c1: ")
                                            .strip().split(", "))))

            cipher = Ciphertext(c0, c1)
            encoded_msg = decryptor.decrypt(cipher) 
            msg = unpad(encoder.decode(encoded_msg)).decode()
            if check(msg):
                print(f"flag is :{flag}") 

        else:
            exit(0)

main()


