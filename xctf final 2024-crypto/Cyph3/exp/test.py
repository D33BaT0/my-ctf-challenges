from collections import Counter
from tqdm import tqdm
from Crypto.Util.number import getRandomNBitInteger
from cypher import *
import os
key = os.urandom(6)
toycipher = ToyCypher(b2i(key))
plain = b'12345656'
print(toycipher.dec(toycipher.enc(plain)))