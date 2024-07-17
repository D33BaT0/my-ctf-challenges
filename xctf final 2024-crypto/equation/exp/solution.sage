
from pwn import *
from time import time
from itertools import product
while 1:
    io = remote(" ", )
    start = time()
    a,b,c,N = eval(io.recvline().strip().decode())

    ffactors = list(factor(N,limit = 2**28))
    if not is_prime(ffactors[-1][0]):
        io.close()
        continue
    print(len(ffactors))

    rots = []
    mods = []
    for fac,exp in ffactors:
        tmproot = []

        if exp>1 or fac==2:
            mod  = fac**exp
            for xx in range(mod):
                fff = Integer((a*xx**2+b*xx+c) % mod)
                if fff == 0:
                    tmproot.append(xx)
            rots.append(tmproot)
            mods.append(Integer(mod))

        else:
            mod = fac
            PR.<X> = PolynomialRing(GF(mod))
            ff = a*X**2+b*X+c
            if ff == 0:
                ti = [ii for ii in range(mod)]
                tmproot.extend(ti)
            for ro,ex in ff.roots():
                ti = [Integer(ro) for i in range(ex)]
                tmproot.extend(ti)
            rots.append(tmproot)
            mods.append(Integer(mod))
    lll = True
    tag = False
    for ress in product(*rots):
        T = Integer(crt(list(ress),mods)) # x = T * y +k *N
        if lll:
            L = Matrix(ZZ,[
                [N , 0],
                [T , 1]
            ]).LLL()
            for Li in L:
                xx,yy = abs(Li[0]),abs(Li[1])
                if a*xx**2+b*xx*yy+c*yy**2==N:
                    print(f"find x,y:{xx},{yy}")
                    io.sendline(str(xx)+","+str(yy))
                    io.interactive()
                    tag = True
                    break
        else:
            P = (a*T*T+b*T+c) // N
            Q = -(2*a*T+b)
            Ta = -Integer(Q)/Integer(2*P)
            cf = continued_fraction(Ta)

            for i in range(200):
                yy = cf.numerator(i)
                if len(bin(yy)) > 130:
                    break

                xx = int((T*yy)%N)
                if a*xx**2+b*xx*yy+c*yy**2==N:
                    print(f"find x,y:{xx},{yy}")
                    io.sendline(str(xx)+","+str(yy))
                    io.interactive()
                    tag = True

        if tag:
            break
    io.close()
    print(time() - start)
