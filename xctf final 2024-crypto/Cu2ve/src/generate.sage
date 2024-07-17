# generate from https://link.springer.com/content/pdf/10.1007/978-3-540-85538-5_9.pdf
# pairing friendly part 参照了 maple 的 https://blog.maple3142.net/2024/04/21/grey-cat-the-flag-2024-quals-writeups/#curve 的coding
def qx(x):
    aa = x^6+2*x^5-3*x^4+8*x^3-15*x^2-82*x+125
    if aa % 180 != 0:
        return False
    else:
        return aa//180

def rx(u):
    return x^4-8*u^2+25

while 1:
    x = randint(0,2**64)
    if not(x%30==5 or x%30==25):
        continue
    p = qx(x)
    if (is_prime(p)):
        break

r = rx(x)//450
A = 1

F1 = GF(p) 
while 1:
    E1 = EllipticCurve(F1,[A,0]) 
    if E1.order()%r==0:  
        break
    A+=1
