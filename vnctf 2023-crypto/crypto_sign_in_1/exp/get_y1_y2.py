from gmpy2 import iroot
x1 = 2022
x2 = 2023
tmp = (3 * x1**2 * (x1 - x2)) // 4 + x2**3 - x1 **3
print(tmp)
# y2^2 - y1^2 = tmp
# print(factor(tmp))
# 5 * 47 * 47 * 67 * 67 * 73
# y1 - y2 = 
# y1 + y2 = 

y1 = 0
y2 = iroot(tmp,2)[0]
print(f"{y1},{y2}")

print(y2**2-y1**2 == tmp)
print(-(x1**2/4*3) == ((y1**2-x1**3)-(y2**2-x2**3)) / (x1 - x2))