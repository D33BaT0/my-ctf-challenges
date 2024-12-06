# bl0ck

## Category

Crypto

## Difficulty

Easy

## Solves

27

## Description

1asy block  cipher.

## FLAG

`flag{K3y_c0l1i$ion5_0n@eS_1s_int3r3s7in9_in_ASIACrypt2024}`

## WriteUps

预期思路是根据backdoor产生9轮的AES-256, 是 AsiaCrypt2024 上 AES Collision 相关的内容（文中给出了一个样例，不需要选手去自己运行生成对应的数据，时间相对较久）。但是赛中我发现大量选手是以非预期直接 `decrypt(b'\0'*16)` 做的，大失败。

https://eprint.iacr.org/2024/1508.pdf#page=59.22