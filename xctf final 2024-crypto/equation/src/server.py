from Crypto.Util.number import getPrime
from secret import flag
from random import randrange 
import signal

def _handle_timeout(signum, frame):
    raise TimeoutError('function timeout')

timeout = 10
signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(timeout) 

p         = getPrime(128)
a,b,c,x,y = [randrange(0,p) for _ in range(5)]
N         = a*x**2+b*x*y+c*y**2

print(f"{a},{b},{c},{N}")

xx,yy = [int(i) for i in input().split(",")]
ss = set([xx,yy,x,y])

assert len(ss) == 2

print(f"you got it! flag is:{flag}")
