from Crypto.Util.number import *

def attack(p, a2, a4, a6, Gx, Gy, Px, Py):
    x = GF(p)["x"].gen()
    f = x ** 3 + a2 * x ** 2 + a4 * x + a6
    roots = f.roots()

    # Singular point is a cusp.
    if len(roots) == 1:
        alpha = roots[0][0]
        u = (Gx - alpha) / Gy
        v = (Px - alpha) / Py
        return int(v / u)

    # Singular point is a node.
    if len(roots) == 2:
        if roots[0][1] == 2:
            alpha = roots[0][0]
            beta = roots[1][0]
        elif roots[1][1] == 2:
            alpha = roots[1][0]
            beta = roots[0][0]
        else:
            raise ValueError("Expected root with multiplicity 2.")
        print(alpha,beta)
        t = find_sqrt(alpha - beta,q)
        u = (Gy + t * (Gx - alpha)) / (Gy - t * (Gx - alpha))
        v = (Py + t * (Px - alpha)) / (Py - t * (Px - alpha))
        print(u,v)
        return int(log(v, u)) , GF(q)(u).multiplicative_order()

    raise ValueError(f"Unexpected number of roots {len(roots)}.")

q = 140112061836406475171682656801376702217
G = (4861829789811226219812387621040649046,16520450475620085245999415627834196206)
P = (54800164299339890550933073859723074272,26075157783659399204697496295286669863)
cipher = bytes.fromhex("20e60eafba374becdb67f142fd86661c7bd22c9fbfdea1ef08a0f7489b01527499448dba73fa133262dea2e91d5b8766")
Gx,Gy = G
Px,Py = P
y1,y2 = 0,3034
A = (y1**2 - y2**2 - 2022**3 + 2023**3) * inverse(-1, q) % q
B = (y1**2 - 2022**3 - A * 2022) % q

def find_sqrt(a,q):
    PR.<x> = PolynomialRing(GF(q))
    f = x**2-a
    print(f.roots())
    return Integer(f.roots()[0][0])

a,mo = attack(q,0,A,B,Gx, Gy, Px, Py)
from Crypto.Cipher import AES
for _ in range(5,1000):
    aes = AES.new((int(a) + _ * int(mo)).to_bytes(16, 'big'), AES.MODE_CBC, bytes(16))
    print(aes.decrypt(cipher))