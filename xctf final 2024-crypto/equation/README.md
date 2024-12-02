# equation

## Category

Crypto/livesolo 

## Difficulty

easy

## Description

ezezez equation

## flag

`flag{pell_is_ez_to_solve}`

## writeups

已知 $a\cdot x^2+b\cdot xy+c\cdot y^2=N$ ， 其中 $a,b,c,x,y$ 都是128 比特； $N$ 是 384 比特的。

如果 $N$ 可以被分解， $N=\prod_{i} p_i$ 中素因子都可以得到。原方程我们可以转换成模 $N$ 的为0的值，即
$$
a\cdot x^2+b\cdot xy+c\cdot y^2 = 0\pmod{N}\tag{1}
$$
令方程 (1) 左右同时除掉一个 $y^2$ ，并设 $z = x/y \pmod{N}$ ，那么可以得到
$$
a\cdot z^2 + b\cdot z + c = 0\pmod{N}\tag{2}
$$
接着 $z \pmod{p_i}$ 的值容易得到，之后对此进行中国剩余定理求得 $z\pmod{N}$ 的值。

已经得到了 $x/y\pmod{N} = z$ ，转换回整数上 $x = k\cdot N+z\cdot y$ ，其中 $k$ 和 $y$ 的比特长度差不多（这里直接LLL也可以直接求出x,y，不过下面描述一下连分数的方法）。回代原方程，
$$
a\cdot (N^2\cdot k^2+2Nz\cdot ky + z^2\cdot y^2) + b\cdot (N\cdot ky+z\cdot y^2)+c\cdot y^2 =N\\
(a\cdot N^2) \cdot k^2 + (2aNz+bN)\cdot(ky) + (az^2+bz+c)\cdot y^2 = N\\
X=(az^2+bz+c)/N\\
Y=2az+b\\
K=aN\\
X\cdot y^2+Y\cdot yk+K\cdot k^2 = 1
$$
$X,Y,Z$ 的值我们都可以取到，
$$
X\cdot y^2+Yk\cdot y+Kk^2-1=0\tag{3}
$$
方程 (3) 解为
$$
\frac{-Yk±\sqrt{\Delta}}{2X}=y ; \Delta = Y^2k^2-4X(Kk^2-1)
$$
其中， $\Delta$ 的分析发现很小，由此
$$
\frac{-Y}{2X}\approx \frac{y}{k}\tag{4}
$$
由于 $y,k$ 的比特数都相对 $Y,X$ 小很多，因此对 (4) 式左边进行连分数即可得到 $y,k$ 的值，那么回代即可计算 $x$ 的值了。

