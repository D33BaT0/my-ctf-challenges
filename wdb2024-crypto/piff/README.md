# piff

## Category

Crypto

## Difficulty

Medium

## writeups

加密 $C(x)=( p\cdot \phi_1(x)\cdot r(\phi_1(x)) + m(\phi_1(x)) ) \pmod{F_1(x)}$, 其中$m(x),r(x)$系数为0或1。

但是我们首先需要去求得 $\psi_1$，这里主要使用线代的方法直接构造多项式矩阵即可求得，当然应该也存在直接求逆映射的函数吧。求得 $\psi_1$ 后，若想要解密还需要有 $f(x)$。根据逆映射，我们有
$$
F_i(\psi_i(x))=0\pmod{f(x)},i\in\{0,1\}
$$
那么我们可以通过已知信息得到两条$f(x)$ 的倍数，接着使用GCD即可求的 $f(x)$ 。求得$\phi_1$逆映射使得
$$
\psi_1(\phi_1(y))\equiv y\pmod{F_1(y)}
$$
即$\phi_1(\psi_1(x))\equiv x\ (mod\ f(x))$，可得$C(\psi_1(x))=p\cdot x\cdot r(x)+m(x) \pmod{f(x)}$。根据加密函数中 $p$ 为2，那么直接求直接模2可得$m(x)$。

最终可以得到flag。