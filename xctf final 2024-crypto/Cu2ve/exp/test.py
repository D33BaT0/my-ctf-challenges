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
    if randbelow(4)!=1:
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