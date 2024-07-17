首先是已经知道需要输入DES的key并且满足 DES的random次加密msg还等于msg

同时根据check

```python

def check(enc): 
    for _ in range(100):
        msg = os.urandom(8)   
        if enc(enc(msg)) == msg: 
            return False
    return True

if not check(enc):
    print("bad key")
    exit()
```

知道该key并不能是弱密钥，需要找个DES的不动点，去寻找相关paper找到 https://ieeexplore.ieee.org/document/9832875 可以得知一组固定的点，同时满足它不是弱密钥。

之后交互即可

```
from Crypto.Util.number import *
from Crypto.Cipher import DES
# https://ieeexplore.ieee.org/document/9832875
from pwn import * 
io = remote("192.168.1.107",11420)
io.recv()
io.sendline(b"B0B351C802C83DE0")
io.recv()
io.sendline(b"4739a2f04b7eab28")
io.interactive()

# 验证如下
key = long_to_bytes(0xB0B351C802C83DE0)
plain = long_to_bytes(0x4739a2f04b7eab28)
des = DES.new(key,DES.MODE_ECB)

def tmp_enc(des,msg):
    for _ in range(114514):
        msg = des.encrypt(msg)
    return msg

assert tmp_enc(des,plain) == plain

P2 =  long_to_bytes(0x9FE10D2E8C496143)
K2 =  long_to_bytes(0x5D460701328F2962)
des = DES.new(K2,DES.MODE_ECB)
assert des.encrypt(P2) == P2

```

