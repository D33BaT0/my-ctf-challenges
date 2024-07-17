from utils import * 
from tqdm import trange
from secret import FLAG

m = 100
F1 = GF(p)
F2.<u> = GF(p^2)

E1 = EllipticCurve(F1,[A,0]) 
hidden = [randint(0,1) for _ in range(m)] 
output = []
rng = prp(hidden,m)

for _ in trange(615):
    E2 = EllipticCurve(F2,[F2.random_element(),0]) 
    P,Q = E1.random_point(),E2.random_point()

    if rng.next():
        x,y = [randint(0,n) for _ in range(2)]
        z = x*y
    else: 
        x,y,z = [randint(0,n) for _ in range(3)]

    output.append([P,x*P,y*P,z*P,Q,y*Q])

output = [[(point[0], point[1]) for point in row] for row in output]

f = open("output.txt", "w")
f.write(f"c='{encrypt(FLAG, hidden).hex()}'\n") 
f.write(f"{output}\n")
