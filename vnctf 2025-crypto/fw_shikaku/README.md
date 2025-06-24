# fw_shikaku

## Category

Crypto

## Difficulty

Medium

## Solves

3

## Solution

197 维度的 LWE 不是很好使用 Lattice Reduction 归约出来，漏洞点就在 error 仅有 2 个，线性化即可。
M4 pro 12 线程，构建矩阵 list 是 10s 左右构建完，但是赋值矩阵花时间。其中 solve_right 相比先求 inverse 更快，大概 180s。单线程的话 大致 330s 就能成功求解，而且 solve_right 一类还可以优化，使用 C 估计 20s 内多线程就能成功求解。给了 450s 的限制。
