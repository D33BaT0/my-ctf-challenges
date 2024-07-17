# generate from https://link.springer.com/content/pdf/10.1007/978-3-540-85538-5_9.pdf
# 这是D =1 的情况，主要内容在《Constructing Tower Extensions of Finite Fields for Implementation of Pairing-Based Cryptography》 6.1
# pairing friendly 的部分参照了 maple 的 https://blog.maple3142.net/2024/04/21/grey-cat-the-flag-2024-quals-writeups/#curve 的 coding

def qx(x):
    aa = x^6+2*x^5-3*x^4+8*x^3-15*x^2-82*x+125
    if aa % 180 != 0:
        return False
    else:
        return aa//180

def rx(u):
    return u^4-8*u^2+25

while 1:
    x = randint(0,2**64)
    if not(x%30==5 or x%30==25):
        continue
    p = qx(x)
    if (is_prime(p)):
        r = rx(x)//450
        
        if is_prime(r):
            break

A=1
F1 = GF(p) 
while 1:
    E1 = EllipticCurve(F1,[A,0]) 
    if E1.order()%r==0:  
        break
    A+=1

n = E1.order()
c = n//r
F2.<u> = GF(p^2)

while 1:
    tA = F2.random_element()
    E2 = EllipticCurve(F2,[tA,0])
    if E2.order()%r==0 and E2.order()%n!=0: # 需要满足这个 而不是模n，因此它tate不会导致一直是1
        break

P =  E1.random_point()
Q =  E2.random_point()
 
k = 8
K.<a> = GF(p^k)
PR.<tt> = PolynomialRing(K)
uk = K(str(F2.modulus().change_ring(ZZ)(tt).roots(multiplicities=False)[0]))
Ek = EllipticCurve(K,[A,0])

def E2_to_Ek(P):
    x,y = P.xy()
    x = x.polynomial().change_ring(ZZ)(uk)
    y = y.polynomial().change_ring(ZZ)(uk)
    return x,y

x1,y1 = E2_to_Ek(Q)
aa = (y1^2-x1^3)/x1
Ek2 = EllipticCurve(K,[aa,0])
phi = Ek2.isomorphism_to(Ek)

tag = 0

from tqdm import trange
for _ in trange(30):
    xxx,yyy = randint(0,n),randint(0,n)
    zzz1,zzz2=randint(0,n), xxx*yyy

    xP,yP = xxx*P,yyy*P
    z1P,z2P = zzz1*P,zzz2*P
    yQ = yyy*Q

    axP  = c * Ek( xP)
    # print(axP.parent())
    ayP  = c * Ek( yP)
    az1P = c * Ek(z1P)
    az2P = c * Ek(z2P) 
 
    x1,y1 = E2_to_Ek( Q)
    x2,y2 = E2_to_Ek(yQ)
    
    hQ  = phi(Ek2(x1,y1))
    yhQ = phi(Ek2(x2,y2))

    AAAA = ( axP).tate_pairing(yhQ, r, 8 ) 
    BBBB = (az1P).tate_pairing( hQ, r, 8 )
    if AAAA == 1:
        print("Bad")
        break

    if AAAA == (az2P).tate_pairing(hQ, r, 8 ):
        print("True 1")
        tag = tag 

    if AAAA == BBBB:
        print("True 2")
        tag +=1 

print(tag)
print(n)
print(p)
print(A)
print(r)