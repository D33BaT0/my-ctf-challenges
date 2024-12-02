# crypto\_sign\_in\_1

## Category

Crypto

## Difficulty

Medium

## Solves

7

## Description

Happy New Year 2023! Welcome to VNCTF 2023!

This time, I will give you a chance to fxxk my cryptosystem...

Well,128 bits is safe, isn't it?

Come on! Let's sign in!

## flag

Dynamic

## writeups

这道题预期中等难度（但是因为某出题人懒的更换环境.jpg，懒得加条件限制导致变成签到题）以及其实是想套点nb的思路的(bushi)。

#### 非预期1. 光滑阶，PH

大部分师傅是直接这么做了，就爆破等阶是光滑的时候就可以了。

#### 非预期2. #E(p)=p+1, MOV attack

这个做法就一个解，来自成电的师傅 @Lvsun。

这个其实在验题的时候想到过，一开始的时候觉得有问题，然后因为思路那时候太乱了就又觉得没问题了。

针对于曲线E:﻿﻿﻿ $y^2=x%3+Ax+B\pmod{q}$ ，在如下情况下，会使得他是一条super singular曲线(即#E(p)=p+1):
$$
1.q\pmod{3}=2,A=0\\
2.q\pmod{4}=3,B=0
$$
﻿﻿﻿A=0或者B=0的情况，并且随机选取的q参数，我们可以保证他存在如上的某种情况，可以使得他是一个supersingular曲线了。

不过这里可能就和构造(2022,y1)和(2023,y2)的两个点好像是满足其中第一个点再曲线上，第二个点会不在曲线上...

MOV Attack其实和PH思路我个人认为还是蛮像的，师傅们有啥不一样的想法欢迎来对线

#### 预期. singular attack

这个做法也有一个师傅做出来了，是来自杭电的师傅 @yolbby。（本来想着卡卡界再出一道，既然已经有预期了就不出了）

首先我们观察题目，让我们给出y1和y2，接着通过y1,y2去生成参数AA和BB﻿﻿﻿
$$
AA=\frac{(y1^2-y2^2-2022^3+2023^3)}{-1}\pmod{q}\\
BB=y1^2-2022^3-2022AA\pmod{q}
$$
﻿﻿﻿其实在这里我们就可以发现，AA中分母为2022-2023，分子可以化为﻿﻿﻿ $(y1^2-2022^3+BB)-(y2^2-2023^3+BB)$ ，那么这里就是给出的两个点即为(2022,y1)，(2023,y2)构造的曲线E。

同时根据G的选取也会发现就是这条曲线y\^2=x\^3+AA x+BB，预期是AA和BB都不能为0的，这里忘了卡一下...

就一般来说只能想到去让他成为一条singular的曲线，
$$
y1^2=x1^3+AA\cdot x1+BB\pmod{q}\tag{1}
$$

$$
y2^2=x2^3+AA\cdot{x2}+BB\pmod{q}\tag{2}
$$

曲线方程减方程(1)或(2)，令 $\text{new\_y}^2=y^2-y_1^2=(x-a)^2(x-b)=(x+x1/2)^2(x-x1)$ ﻿﻿﻿，但同时需要满足AA的情况，也即另外一个点在曲线上，将其构造可以满足singular的情况。

而在此处这里如果y1不给0的话会产生他的曲线有一定的形变，但是这个形变很神奇，在平面几何里面我倒是没想到啥比较好的替换方法，但是如果y1给0，那么就很容易可以解决了，于是找到了y2=3034时，是可以使得曲线成为Singular曲线，那接着就是很常见的singular attack了，咋搞就不特别描述了。