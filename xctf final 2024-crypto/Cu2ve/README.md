# Cu2ve

## Category

Crypto

## Difficulty

Hard(intend solution)

## Solves

about 10

## Description

an easy curve problem...

## flag

`flag{u_kn0w_curv3.h@v3_fun!}`

## writeups

灵感来源于greycat ctf2024的curve，想法是出个不一样的paring based的题目。

本题相对于原来的curve相比是，curve是 $E(\mathbb{F}_p):y^2=x^3+b$ 的一个情况，同时曲线的阶 $n | p^{12}-1$ 且 $n$ 是一个素数；但本题中 $n$ 并非素数，而是一个合数，且曲线为 $y^2=x^3+Ax$ 生成方式是参照了*https://link.springer.com/content/pdf/10.1007/978-3-540-85538-5_9.pdf* 中 $k=8,D=1$ 的情况（KSS）。

这里就尝试去找 $n$ 与 $p^i-1$ 的关系，使用 $GCD$ 的方法去找到一个数，也就是论文中的 $r$ 的值，pairing friendly是当[r]-torison的时候满足。

```python
from Crypto.Util.number import *
p = 
n = 
for i in range(12):
    print(GCD(n,p**i-1))
```

题目中有一条原始的曲线 $E_0(\mathbb{F}_p):y^2=x^3+Ax$ 阶就是给出的 $n$ ，后又随机生成了 $E_{i}(\mathbb{F}_{p^2}):y^2=x^3+A_ix$ 接着我只需要去生成的 $P_i\in E_0,Q_i\in E_i$ 都lift到同一个曲线上，再paring一下即可（$j(E_0)=j(E_i)=1728$​）。

下面是test脚本

需要注意的时候是$E_i$的阶不是模n为0的情况，而是模$r$为0，模n不为0的时候才能tate_pairing上，否则tate出来的一直都是1，就所有都成立（这个在我出题的时候debug了好久）

```python
p = 
A = 1
F1 = GF(p) 
E1 = EllipticCurve(F1,[A,0]) 
n = E1.order()
r = gcd(n,p**8-1)
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
```



后面其实就是一个permutation的问题了，完全可以直接看作是已知明文的MTP去恢复出来key即可，test脚本如下：

```python
from utils import p,n,A,prp
from secrets import randbelow

twsit_state = [ 76, 5, 29, 61, 62, 54, 66, 69, 81, 48,
                            20, 64, 14, 77, 50, 79, 71, 40, 93, 58, 
                            59, 19, 31, 63,  2, 96, 35, 18, 85, 56,
                            21, 33,  7, 99, 17, 38, 97, 89, 74, 32, 
                            27, 42,  3, 82, 91, 41, 86,  9, 13, 30, 
                            11, 87,  1, 88, 26, 67, 25, 75, 94, 45, 
                            68, 39, 55, 16, 28, 57, 49, 37, 52, 22, 
                            70, 36,  0,  8, 65, 72, 43, 12, 23, 53,
                            51, 60,  4, 46, 83, 90, 84, 92, 24, 15,
                            80, 98, 34, 78, 95, 44, 73, 10,  6, 47]

m = 100
hidden = [randbelow(2) for _ in range(m)] 
rng = prp(hidden,m)

times = 615
ks = []
for _ in range(times):
    k = rng.next()
    if randbelow(5)!=1:
        ks.append("?")
        continue
    ks.append(k)

real_hidden = ["?" for _ in range(m)]

def recover_data(old_station,ktmp):
    global real_hidden
    new_station = [int(old_station[twsit_state[i]]) for i in range(m)]

    for _ in range(len(ktmp)):
        if ktmp[_] == "?": continue
        if real_hidden[new_station[_]] != "?" and real_hidden[new_station[_]] != ktmp[_]:
            print("bug?")
        real_hidden[new_station[_]] = ktmp[_]
    return new_station

old_station = [i for i in range(m)]
for _ in range(6):
    old_station = recover_data(old_station,ks[_*100:_*100+100])

print(real_hidden.count("?"))
```



不过这部分还可以直接进行一个permutation对应的位置去判断六组多一点 哪里为满足的去直接跑基本上近似100次即可（这样相对也比较快）。

如果还有部分位置信息未泄露的话，就需要带一点点爆破了。

整体恢复key的脚本如下，但是还有部分的信息其实是得不到的：

```python
from utils import *
from tqdm import tqdm

F.<x> = PolynomialRing(ZZ)
r = 2232123796482243553563388394642252242447624758532104909445052499370196473
e2o = 31278604127290247578271715456389580024504536762091689653084108630682523156753735534001088645984992476850153398971689257644109185492284665270104815648968278421418869650567421204328618291858399879149578979851216693594335362
assert e2o % r == 0
c = n//r 

F1 = GF(p) 
E1 = EllipticCurve(F1,[A,0]) 

F2.<u> = GF(p^2)

f = open("./output.txt",'r')
datas = eval(f.readlines()[1])
f.close() 

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

ksss = ['?', '?', '?', '?', '?', '?', '?', 1, 1, 0, '?', '?', 1, '?', '?', '?', '?', '?', '?', '?', 0, 0, 1, '?', 1, '?', 0, 0, 1, 1, '?', '?', '?', 1, '?', 0, '?', '?', 1, '?', 0, '?', 1, '?', '?', '?', '?', '?', '?', 0, '?', '?', '?', '?', '?', 1, '?', 1, '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', 0, 0, '?', '?', '?', '?', '?', 0, 0, 1, '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', 0, 1, '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', 0, 0, '?', 1, '?', 0, '?', '?', '?', 0, '?', '?', '?', '?', 1, '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', 1, 1, '?', 0, '?', '?', 1, 0, '?', '?', 1, '?', '?', '?', 0, 0, 0, 0, 0, '?', '?', 1, 0, '?', 1, 1, '?', 1, '?', '?', '?', '?', '?', 1, 1, '?', 0, '?', 1, '?', '?', '?', 1, '?', 0, '?', '?', '?', '?', '?', '?', '?', '?', 0, 0, '?', '?', '?', 1, 1, 0, '?', '?', '?', 1, '?', '?', '?', '?', 1, '?', '?', '?', '?', '?', '?', '?', '?', 0, 1, '?', '?', '?', 1, '?', '?', 0, 0, '?', '?', 1, 1, '?', 1, '?', 1, '?', '?', '?', '?', '?', '?', 1, '?', '?', 0, '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', 1, '?', '?', '?', '?', '?', '?', '?', '?', '?', 0, 0, '?', '?', 1, '?', '?', '?', 0, 1, '?', '?', '?', '?', '?', '?', 1, 0, '?', '?', 0, '?', 1, '?', 0, '?', '?', '?', '?', '?', 1, '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', 0, '?', '?', 1, '?', '?', '?', '?', '?', '?', 1, '?', '?', '?', '?', '?', 0, '?', 0, 1, '?', 0, '?', 1, '?', '?', 1, 0, '?', '?', '?', '?', '?', '?', '?', '?', '?', 0, '?', '?', '?', 0, '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', 1, '?', '?', 0, '?', '?', '?', '?', '?', 0, '?', '?', '?', '?', '?', 1, 0, '?', '?', '?', '?', '?', 1, '?', '?', '?', 1, '?', '?', '?', '?', 1, '?', 0, '?', 1, 1, 0, '?', '?', '?', 0, '?', '?', '?', '?', '?', 0, '?', '?', '?', '?', '?', '?', '?', '?', 0, '?', '?', '?', 1, '?', '?', 0, '?', '?', '?', '?', '?', 0, '?', '?', '?', '?', 1, '?', 1, '?', '?', 1, '?', '?', 1, '?', '?', '?', 0, 0, 1, '?', '?', 1, '?', '?', 1, 1, 0, '?', '?', '?', '?', '?', '?', 0, '?', '?', '?', 0, '?', '?', '?', '?', '?', '?', 0, '?', '?', '?', 1, '?', '?', '?', '?', '?', '?', '?', '?', 1, '?', '?', '?', '?', 0, '?', 0, '?', 1, 0, '?', '?', '?', 1, '?', 1, '?', '?', '?', 1, '?', 0, '?', '?', '?', '?', '?', '?', 1, '?', '?', 1, '?', '?', 0, '?', '?', '?', '?', 1, 0, '?', '?', '?', '?', 0, '?', '?', '?', '?', 1, '?', 0, 0, '?', '?', '?', '?', '?', 1, '?', '?', '?', '?', 0, 1, 1, '?', '?', '?', 0, '?', '?', 0, '?', '?', 0, '?', '?', '?', '?', '?', '?', 0]

for tmp in tqdm(datas[len(ksss):len(ksss)+50]):
    _,xP,_,zP,Q,yQ = tmp  
    tA = F2((Q[1]**2-Q[0]**3)/Q[0])
    E2 = EllipticCurve(F2,[tA,0]) 
    
    xP = E1(xP)
    zP = E1(zP)

    Q =  E2( Q)
    
    if Q * e2o != 0 :
        ksss.append("?")
        continue   

    axP = c * Ek(xP) 
    azP = c * Ek(zP)  

    yQ = E2(yQ)

    x1,y1 = E2_to_Ek( Q) 

    aa = (y1^2-x1^3)/x1
    Ek2 = EllipticCurve(K,[aa,0])
    phi = Ek2.isomorphism_to(Ek)

    x2,y2 = E2_to_Ek(yQ)
    
    hQ = phi(Ek2(x1,y1)) 
    yhQ= phi(Ek2(x2,y2)) 
    
    AAAAA = (axP).tate_pairing(yhQ, r, 8)
    BBBBB = (azP).tate_pairing( hQ, r, 8)

    if AAAAA == 1:
        print("BAD")
        ksss.append("?")
        continue

    if AAAAA == BBBBB:
        ksss.append(1)
    else: 
        ksss.append(0)

print(ksss)


m=100

twsit_state = [ 76, 5, 29, 61, 62, 54, 66, 69, 81, 48,
                            20, 64, 14, 77, 50, 79, 71, 40, 93, 58, 
                            59, 19, 31, 63,  2, 96, 35, 18, 85, 56,
                            21, 33,  7, 99, 17, 38, 97, 89, 74, 32, 
                            27, 42,  3, 82, 91, 41, 86,  9, 13, 30, 
                            11, 87,  1, 88, 26, 67, 25, 75, 94, 45, 
                            68, 39, 55, 16, 28, 57, 49, 37, 52, 22, 
                            70, 36,  0,  8, 65, 72, 43, 12, 23, 53,
                            51, 60,  4, 46, 83, 90, 84, 92, 24, 15,
                            80, 98, 34, 78, 95, 44, 73, 10,  6, 47]

real_hidden = ["?" for _ in range(m)]

def recover_data(old_station,ktmp):
    global real_hidden
    new_station = [int(old_station[twsit_state[i]]) for i in range(m)]

    for _ in range(len(ktmp)):
        if ktmp[_] == "?": continue
        if real_hidden[new_station[_]] != "?" and real_hidden[new_station[_]] != ktmp[_]:
            print("bug?")
        real_hidden[new_station[_]] = ktmp[_]
    return new_station

old_station = [i for i in range(m)]
for _ in range(6):
    old_station = recover_data(old_station,ksss[_*100:_*100+100])

print(real_hidden.count("?"))
print(real_hidden)
```

最后还是有16bit的未知信息，直接爆破即可

```python
from hashlib import shake_128
from itertools import product
from tqdm import tqdm
def encrypt(msg, key):
    y = shake_128("".join(map(str, key)).encode()).digest(len(msg))
    return bytes([msg[i] ^ y[i] for i in range(len(msg))])

real_hidden = [0, '?', 1, 1, 1, 1, 0, 1, '?', 1, '?', 1, 1, 1, 1, 1, 0, '?', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, '?', 1, 0, '?', 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, '?', 0, 1, '?', '?', 0, '?', '?', 1, 1, 1, 0, 1, 1, '?', 1, 0, '?', 0, '?', 1, 1, 0, 0, 0, 1, 0, 1, 1, '?', 0, 1, '?', 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1]

unknown_idx = [-1]
for _ in range(len(real_hidden)):
    if real_hidden[_] == '?':unknown_idx.append(_)

c = bytes.fromhex('dbc2eddcafdbd5d2dbc1b92cb32b4d6a604950c127a9d77007ee81bf')

length = len(unknown_idx) - 1
for itmp in tqdm(product([0,1],repeat=length)): 
    new_hidden = []
    for _ in range(length + 1):
        if _ == length:
            ti = real_hidden[unknown_idx[_]+1:]
        else:
            ti = real_hidden[unknown_idx[_]+1:unknown_idx[_+1]]
            ti.append(itmp[_])
        new_hidden.extend(ti)
    msg = encrypt(c, new_hidden)
    if b'flag' in msg:
        print(msg)
```

