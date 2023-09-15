from gmpy2 import iroot
for x1 in range(2000,2100):
    if x1 % 2 != 0 :
        continue
    for x2 in range(x1,2100):
        y2_t = - x1 ** 3 // 4 + x2 * (x2**2 - 3 * x1**2//4)
        if iroot(y2_t,2)[1]:
                print(x1,x2)