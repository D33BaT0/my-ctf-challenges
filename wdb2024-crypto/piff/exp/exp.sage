from Crypto.Util.number import *
from Crypto.Cipher import AES

q = 41
n = 128
F = GF(q)
R = PolynomialRing(F,'x')
x = R.gen() 

F1 = x^128 + 10*x^127 + 20*x^126 + 11*x^125 + 36*x^124 + 38*x^123 + 36*x^122 + 34*x^121 + 21*x^120 + 32*x^119 + 21*x^118 + 29*x^117 + 33*x^116 + 9*x^115 + 4*x^114 + 20*x^113 + 4*x^112 + 35*x^111 + 30*x^110 + 15*x^109 + 28*x^108 + 22*x^106 + 40*x^105 + 7*x^104 + 27*x^103 + 5*x^102 + 10*x^101 + 33*x^100 + 12*x^99 + 12*x^98 + 39*x^97 + 22*x^96 + 11*x^95 + 6*x^94 + 35*x^93 + 23*x^92 + 5*x^91 + 15*x^90 + 13*x^89 + 32*x^88 + 40*x^87 + 15*x^86 + 4*x^85 + 16*x^84 + 32*x^83 + x^82 + x^81 + 25*x^80 + 20*x^79 + 7*x^78 + 3*x^77 + 10*x^76 + 26*x^75 + 39*x^74 + 24*x^73 + 20*x^72 + 19*x^71 + 7*x^70 + 7*x^69 + 23*x^68 + 36*x^67 + 30*x^66 + 37*x^65 + 35*x^64 + 24*x^63 + 32*x^62 + 13*x^61 + 26*x^60 + 12*x^59 + 19*x^58 + 25*x^57 + 19*x^56 + 38*x^55 + 8*x^54 + 6*x^53 + 3*x^52 + 19*x^51 + 17*x^50 + 32*x^49 + 40*x^48 + 11*x^47 + 6*x^46 + 6*x^45 + 28*x^44 + 35*x^43 + 38*x^42 + 21*x^41 + 21*x^40 + 20*x^39 + 10*x^38 + 25*x^37 + 3*x^36 + 2*x^35 + 15*x^34 + x^33 + 2*x^32 + 4*x^31 + 31*x^30 + 29*x^29 + 31*x^27 + 19*x^26 + 2*x^25 + 17*x^24 + 40*x^23 + 13*x^22 + 8*x^21 + 3*x^20 + 30*x^19 + 16*x^18 + 15*x^17 + 20*x^16 + 22*x^15 + 2*x^14 + 36*x^13 + 24*x^12 + 10*x^11 + 20*x^10 + 35*x^9 + 32*x^8 + 8*x^7 + 35*x^6 + 14*x^5 + 29*x^4 + 40*x^3 + 38*x^2 + x + 25
φ1 = 10*x^126 + 39*x^124 + 27*x^123 + 16*x^122 + 20*x^121 + 2*x^120 + 27*x^119 + 24*x^117 + 36*x^116 + 16*x^114 + x^112 + x^111 + 8*x^110 + 40*x^109 + 15*x^108 + 18*x^107 + 25*x^106 + 6*x^105 + 22*x^104 + 8*x^102 + 20*x^101 + 15*x^100 + 33*x^99 + 9*x^98 + 6*x^97 + 21*x^96 + 4*x^95 + 2*x^94 + 18*x^93 + 37*x^92 + 6*x^91 + 16*x^90 + 38*x^89 + 27*x^88 + 9*x^87 + 7*x^86 + 13*x^85 + 27*x^84 + 22*x^83 + 19*x^82 + 22*x^81 + 31*x^80 + 25*x^79 + 2*x^78 + 14*x^77 + 23*x^76 + 15*x^75 + 37*x^74 + 25*x^73 + 14*x^72 + 10*x^71 + 18*x^70 + 38*x^69 + 33*x^68 + 2*x^67 + 37*x^66 + 29*x^65 + 15*x^64 + 10*x^63 + 28*x^62 + 10*x^61 + 34*x^60 + 21*x^59 + 39*x^58 + 8*x^56 + 28*x^55 + 33*x^54 + 10*x^53 + 21*x^52 + 35*x^51 + 15*x^50 + 11*x^49 + 21*x^48 + 19*x^47 + 22*x^46 + 14*x^45 + 22*x^44 + 30*x^42 + 5*x^41 + 29*x^40 + 6*x^39 + 3*x^38 + 11*x^37 + 37*x^36 + 7*x^35 + 33*x^34 + 4*x^33 + 33*x^32 + 39*x^31 + 37*x^30 + 17*x^29 + 30*x^28 + 35*x^27 + 33*x^26 + 3*x^25 + 30*x^24 + 31*x^23 + 18*x^22 + 34*x^21 + 16*x^20 + 6*x^19 + 30*x^18 + 35*x^17 + 3*x^16 + 37*x^15 + 3*x^14 + 24*x^13 + 14*x^12 + 8*x^11 + 23*x^10 + 40*x^9 + 32*x^8 + 5*x^7 + 15*x^6 + 37*x^5 + 32*x^4 + 17*x^3 + 11*x^2 + 26*x
F2 = x^128 + 18*x^127 + 34*x^126 + 40*x^125 + 18*x^124 + 30*x^123 + 2*x^122 + 11*x^121 + 21*x^120 + 30*x^119 + 20*x^118 + 34*x^117 + x^116 + 40*x^115 + 39*x^113 + 5*x^112 + 7*x^111 + 20*x^110 + 25*x^109 + 30*x^108 + 8*x^107 + 29*x^106 + x^105 + 25*x^104 + 35*x^103 + 37*x^102 + 4*x^101 + 35*x^100 + 33*x^98 + 22*x^97 + 26*x^96 + 12*x^95 + 20*x^94 + 27*x^93 + 39*x^92 + 32*x^91 + 9*x^90 + 12*x^89 + 13*x^88 + 29*x^87 + 33*x^86 + 26*x^85 + 14*x^84 + 21*x^83 + 19*x^82 + 7*x^81 + 11*x^80 + 3*x^79 + 2*x^78 + 8*x^77 + 3*x^76 + 35*x^74 + 40*x^73 + 23*x^72 + 2*x^71 + 16*x^70 + 17*x^69 + 16*x^68 + 29*x^67 + 30*x^66 + 29*x^65 + 36*x^64 + 2*x^63 + 39*x^62 + 17*x^61 + 6*x^60 + 29*x^59 + 21*x^58 + 21*x^57 + 23*x^56 + 32*x^55 + 28*x^54 + 38*x^53 + 22*x^52 + 35*x^51 + 23*x^50 + 13*x^49 + 10*x^48 + 20*x^47 + 30*x^46 + 22*x^45 + 36*x^44 + 3*x^43 + 19*x^42 + 40*x^41 + 20*x^40 + 7*x^39 + 36*x^38 + 27*x^37 + 36*x^36 + 33*x^35 + 32*x^34 + 15*x^33 + 18*x^32 + 38*x^31 + 40*x^30 + 9*x^29 + 8*x^28 + 34*x^27 + 5*x^26 + x^25 + 17*x^24 + 36*x^23 + 30*x^22 + 18*x^21 + 7*x^20 + 26*x^19 + 4*x^18 + 39*x^17 + 16*x^16 + 18*x^15 + 23*x^14 + 5*x^13 + 17*x^12 + 23*x^11 + 13*x^10 + 34*x^9 + 21*x^8 + 24*x^7 + 5*x^6 + 13*x^5 + 16*x^4 + 40*x^3 + 18*x^2 + 11*x + 10
φ2 = 16*x^126 + 24*x^125 + 8*x^124 + 6*x^123 + 37*x^122 + 28*x^120 + 4*x^119 + 35*x^118 + 26*x^117 + 30*x^116 + 29*x^115 + 36*x^114 + 30*x^113 + 22*x^112 + 16*x^111 + 34*x^110 + 35*x^109 + 23*x^108 + 27*x^107 + 35*x^106 + 13*x^104 + 5*x^103 + 38*x^102 + 28*x^101 + 21*x^100 + 11*x^99 + 31*x^98 + 7*x^97 + 4*x^95 + 17*x^94 + 40*x^92 + 30*x^91 + 5*x^90 + 9*x^89 + 5*x^88 + 26*x^87 + 23*x^86 + 9*x^85 + 17*x^84 + 37*x^83 + 22*x^82 + 12*x^81 + 40*x^80 + 24*x^79 + 29*x^78 + 22*x^77 + 12*x^75 + 37*x^74 + 22*x^73 + 11*x^72 + 14*x^71 + 19*x^70 + 16*x^68 + 28*x^67 + 39*x^66 + 21*x^65 + 28*x^64 + 36*x^63 + 21*x^62 + 37*x^61 + 27*x^60 + 36*x^59 + 12*x^58 + 19*x^57 + 16*x^56 + 17*x^55 + 13*x^54 + 2*x^53 + 12*x^52 + 38*x^50 + 10*x^49 + 3*x^48 + 20*x^47 + 7*x^46 + 7*x^45 + 11*x^44 + x^43 + 23*x^42 + 17*x^41 + 18*x^40 + 19*x^39 + 15*x^38 + 3*x^37 + 2*x^36 + 19*x^35 + 35*x^34 + 29*x^33 + 6*x^32 + 16*x^31 + 36*x^30 + 30*x^29 + 15*x^28 + 30*x^27 + 13*x^26 + 34*x^25 + 29*x^24 + 7*x^23 + 37*x^22 + 40*x^21 + 14*x^20 + 20*x^19 + 5*x^18 + 7*x^17 + 21*x^16 + 21*x^15 + 32*x^14 + 36*x^13 + 25*x^12 + x^11 + 30*x^10 + 5*x^9 + 29*x^8 + 21*x^7 + 19*x^6 + 16*x^5 + 23*x^4 + 16*x^3 + 40*x^2 + 26*x + 31
C=33*x^127 + 35*x^126 + 2*x^125 + 4*x^124 + 39*x^123 + 24*x^122 + 4*x^121 + 18*x^120 + 22*x^119 + 8*x^118 + 15*x^117 + 38*x^116 + 11*x^115 + 14*x^114 + 11*x^113 + 38*x^112 + 35*x^111 + 15*x^110 + 21*x^109 + 31*x^108 + 28*x^107 + 16*x^106 + 30*x^105 + x^104 + 11*x^103 + 31*x^102 + 30*x^101 + 38*x^100 + 23*x^99 + 28*x^98 + 29*x^97 + 22*x^96 + 24*x^95 + 28*x^94 + 14*x^93 + x^92 + 23*x^91 + 25*x^90 + 10*x^89 + 15*x^88 + 18*x^87 + 18*x^86 + 21*x^85 + 38*x^84 + 7*x^83 + 19*x^82 + 29*x^81 + 33*x^80 + 15*x^79 + 30*x^78 + 27*x^77 + 29*x^76 + 15*x^75 + 32*x^74 + 3*x^73 + 29*x^72 + 19*x^71 + 21*x^70 + 28*x^69 + 16*x^68 + 5*x^67 + 30*x^66 + 21*x^65 + 26*x^64 + 18*x^63 + 12*x^61 + 7*x^60 + 19*x^59 + 5*x^58 + 32*x^57 + 40*x^56 + 29*x^55 + 28*x^54 + 19*x^53 + 40*x^52 + 15*x^51 + 31*x^50 + 5*x^49 + 8*x^48 + 23*x^47 + 11*x^46 + 40*x^45 + 4*x^43 + 23*x^42 + x^41 + 5*x^40 + 16*x^39 + 38*x^38 + 39*x^37 + 15*x^36 + 26*x^35 + 30*x^34 + 29*x^33 + 7*x^32 + x^31 + 16*x^30 + x^29 + 5*x^28 + 2*x^27 + 36*x^26 + 3*x^25 + 32*x^24 + 32*x^23 + 23*x^22 + 35*x^21 + 26*x^20 + 13*x^19 + 16*x^18 + 40*x^17 + 21*x^16 + 16*x^15 + 21*x^14 + 25*x^13 + 25*x^12 + 17*x^11 + 20*x^10 + 4*x^9 + 2*x^8 + 8*x^7 + 20*x^6 + 24*x^5 + 28*x^4 + 21*x^3 + 28*x^2 + 7*x + 16
cipher=b'\xcc\xfcZ\x07d\x149\xf8\x06\n\x8cp$\x16d\x1d\xa9\x807\xf2\xc13Y\xe3\xd5=\x189\x1a_c,'

def get_psi(R, x, q, n, phi, F):
    polys = []
    for i in range(n):
        polys.append(pow(phi(x),i,F(x)))
    monomials = [x**i for i in range(n)]
    B = Matrix(GF(q), n)
    for ii in range(1,n):
        for jj in range(n):
            if monomials[jj] in polys[ii].monomials():
                B[ii, jj] = polys[ii].monomial_coefficient(monomials[jj])
    t = Matrix(GF(q), 1,n)
    t[0,1] = 1;B[0,0] = 1
    psi = t*B**(-1)
    psi = tuple(list(psi)[0])
    psi = R(psi)
    return psi

psi1 = get_psi(R, x, q, n, φ1, F1)
psi2 = get_psi(R, x, q, n, φ2, F2)
ff   = F1(psi1(x)).gcd(F2(psi2(x)))

ki = ''.join(str(i) for i in  (C(psi1(x)) % ff(x)).change_ring(GF(2)).coefficients(sparse=False))
if len(ki) != 128:
    ki += '0'*(128-len(ki))

aes = AES.new(long_to_bytes(int(ki , 2)), mode=AES.MODE_ECB)
print(aes.decrypt(cipher))
