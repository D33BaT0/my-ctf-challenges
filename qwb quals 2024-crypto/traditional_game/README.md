# traditional_game

## Category

Crypto

## Difficulty

Medium

## Solves

about 17

## Description

Since you've made it here, let's now play a Traditional Game from 1997.

## flag

`flag{eeeeeeeeeeeeeeeeeeeeezzzz_game_will_be_over}`

## writeups

第一步需要过game，而这里初始化时间的时候是int(time.time())，可以使用反射攻击pass掉。

第二步需要d 的 Partial Key Exposure

这里只用一块信息的话是不能够恢复的，所以需要两部分信息，已知，设 $Blind$ 为 $B$
$$
d=d_m\cdot 2^{unkbit}\cdot B+B\cdot x+d_l
$$
用关系
$$
d\cdot e - 1 = k(n+1-(p+q))
$$
而这里由于 $e$ 小并且 $d$ 的高位可以知道，那么很容易求得 $k$ 

接着就是 
$$
d_m\cdot B\cdot 2^{unkbit}\cdot e +e\cdot B\cdot x+ e\cdot d_l - 1- k(n+1)+k(p+q)=0
$$
那么将已知常数部分用$A$代替，则得到
$$
A+e\cdot B\cdot x + k(p+q)=0
$$
接着模 $k$ 可以得到 $x$ 的低位，那么可以使用 $x$ 去表示 $d$ ，接着用 $d$ 去获取 $p$ 的MSB;

模 $eB$ 可以得到 $p+q$ 的低位，用此可以去获取 $p$ 的LSB，两边一起卡然后去coppersmith 可以分解 $N$

