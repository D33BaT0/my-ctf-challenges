# r3system / r3system-revenge

## Description

There were whispers of lesser systems in the past iterations of the r3kapig's cyber-metropolis. Now, r3girl stands before the monolithic r3system, a digital fortress said to dwarf all that came before. The path to understanding its true nature is heavily guarded. First, you must demonstrate unparalleled computational prowess to become the **King of PoW**. Only by obtaining the system's core schematics can you possibly decipher its final mystery and seize the prize that lies within this heavily fortified sector.

Note: You should pass 1 PoW then get the source code! 

## Flag

`r3ctf{finding_reduced_round_keccak_collisions_is_awsome-related_nonce_attack_can_be_more_efficient}`

## Solution

### First part. pass the part of PoW(Keccak 224-4 round collisions)


#### **Overview**

The objective is to find 22 collision pairs for a reduced-round version of Keccak-224. The methodology for this attack is based on the paper **"New attacks on Keccak-224 and Keccak-256"**.

The primary difficulty lies in implementing the **Target Difference Algorithm (TDA)** described in the paper. Furthermore, a key to quickly obtaining the source code for the second step is to study the examples provided in the paper and to gain a deep understanding of Keccak's *padding* scheme. It's important to note that the main distinction between Keccak, SHA-3, and SHAKE lies in their respective padding methods.

#### **Core Concept: Target Difference Algorithm (TDA)**

The central idea is to construct a message pair that follows a specific differential path, in order to leverage the **"internal differential"** technique. This involves introducing specific differences that cancel each other out within the internal state of the hash function after a few rounds, ultimately leading to a collision at the output.

The Keccak round function $R$ is a composition of several operations: $R = \iota \circ \chi \circ \pi \circ \rho \circ \theta$.
* $\theta, \rho, \pi$: These are linear operations. Their composition is denoted as $L = \pi \circ \rho \circ \theta$.
* $\chi$: This is the only **non-linear** operation, acting as the S-box.
* $\iota$: This involves adding a round-specific constant.

The Target Difference Algorithm (TDA) cleverly exploits the quadratic algebraic properties of the $\chi$ S-box and the degrees of freedom available in the message input. The algorithm consists of two main phases:

1.  **Difference Phase**: The goal is to find a candidate initial state difference (the "target difference"), $\Delta_i = M^1 \oplus M^2$. This difference must satisfy two conditions:
    * The difference in the parts of the state corresponding to padding and capacity must be zero.
    * The input difference to the first-round S-boxes, $L(\Delta_i)$, must be compatible with the output difference, $\Delta_T$, as dictated by the S-box's difference distribution table.
    The output of this phase is an affine subspace describing all possible candidate values for $L(\Delta_i)$.

2.  **Value Phase**: Once a suitable $\Delta_i$ is determined, this phase aims to find a specific initial state, $M^1$, that can produce this target difference. It must satisfy:
    * The parts corresponding to padding and capacity must conform to the Keccak specification.
    * For every S-box in the first round, the input pair $(v, v \oplus L(\Delta_i))$, where $v$ is a part of $L(M^1)$, must produce the required output difference $\Delta_T$.
    The output of this phase is an affine subspace describing candidate values for $L(M^1)$, which in turn uniquely determines $\Delta_T$.

By solving these systems of linear equations, TDA provides a specific 1600-bit initial difference $\Delta_i$ and an affine subspace that contains candidate messages ($M^1$) for the subsequent collision search.

#### **Collision Search and Verification**

The main steps to find a collision are as follows:

1.  **Extract TDA Output**: A successful TDA run yields a fixed 1600-bit initial differential state $\Delta_i$ (with a high probability that the output will follow the differential characteristic) and a projection space for all possible values of $L(M^1)$. Applying the inverse linear layer, $L^{-1}$, to this space gives the projection space for the message $M^1$ itself.

2.  **Search the Solution Space**: The projection space for $M^1$ is spanned by a base vector $M^1_0$ and a set of basis vectors $\{u_1, \dots, u_k\}$. Any candidate message in this space can be expressed as $M^1 = M^1_0 \oplus \bigoplus_{j=1}^k c_j u_j$, where each coefficient $c_j$ is either 0 or 1. The code iterates through all combinations of these coefficients to generate candidate messages $M^1$ and their corresponding pairs $M^2 = M^1 \oplus \Delta_i$.

3.  **Verify the Collision**: For each generated message pair $(M^1, M^2)$:
    * By TDA, the pair already satisfies the differential $\Delta_t$ after the first Keccak round.
    * Next, verify that this $\Delta_t$ propagates correctly through the second and third rounds according to the pre-selected differential characteristic.
    * Finally, check if the hash outputs after four rounds are identical. If they are, a collision has been found.

#### **Additional Constraint**

Furthermore, an additional constraint must be applied: the candidate message **$M^1$ must start with the character 'r'**.

### Second part. related nonce attack with more efficient method.

#### Overview


This was for a "revenge" edition of the `r0/r1/r2system` challenge in `R3CTF 2024`. In this version, the nonce-generating polynomial has a degree of 121. According to the paper **"A Novel Related Nonce Attack for ECDSA"**, the recursive `dpoly` method has a prohibitively high complexity for this problem, making it impossible to find a solution within the 600-second time limit.

However, during the competition, an unintended and simpler vulnerability was discovered by `Sceleri(Friendly Maltese Citizens)`: the `randint` function was implemented in a way that made the nonces easily predictable, thus trivializing the recovery of the private key `x`.

Below, I will briefly describe the intended solution of `r3system-revenge`.

#### A Vandermonde-like Matrix Approach

Consider a recurrence relation of order $m$: $k_{i+1} = \sum_{j=0}^{m} a_j k_i^j$. Assume we have $N = m+2$ consecutive nonces $k_1, \dots, k_{m+2}$, which are generated from the initial values $k_0, \dots, k_{m+1}$. The recurrence relation holds for $i=0, \dots, m+1$.

This allows us to write out the following $m+2$ relations:
$$
\begin{align*}
k_1 &= a_m k_0^m + a_{m-1} k_0^{m-1} + \dots + a_1 k_0 + a_0 \\
k_2 &= a_m k_1^m + a_{m-1} k_1^{m-1} + \dots + a_1 k_1 + a_0 \\
&\vdots \\
k_{m+2} &= a_m k_{m+1}^m + a_{m-1} k_{m+1}^{m-1} + \dots + a_1 k_{m+1} + a_0
\end{align*}
$$


We can view this as a linear system. Consider the following $(m+2) \times (m+2)$ matrix:
$$
\begin{equation*}  
M = 
\begin{pmatrix}
k_1 & k_0^m & k_0^{m-1} & \cdots & k_0^1 & 1 \\
k_2 & k_1^m & k_1^{m-1} & \cdots & k_1^1 & 1 \\
\vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
k_{m+2} & k_{m+1}^m & k_{m+1}^{m-1} & \cdots & k_{m+1}^1 & 1
\end{pmatrix}
\end{equation*}
$$

The recurrence relation essentially states that the first column of $M$ is a linear combination of the subsequent $m+1$ columns, with coefficients $(a_m, a_{m-1}, \dots, a_0)$. Specifically, if we consider the vector $\mathbf{c} = (-1, a_m, a_{m-1}, \dots, a_0)^T$, then we have $M \mathbf{c} = \mathbf{0}\pmod{p}$. Since a non-zero vector $\mathbf{c}$ exists in the null space of $M$, the matrix $M$ must be singular, meaning its determinant is zero.

The structure of matrix $M$ is similar to a Vandermonde matrix, particularly in the columns containing powers of $k_i$. The condition $\det(M)=0\pmod{p}$ provides a constraint derived from the recurrence relation. The key to this construction is identifying the linear dependency between the nonces and their powers, which is induced by the PRNG's recurrence. At this point, the determinant equation $\det(M)=0\pmod{p}$ becomes a polynomial expression involving only the nonce values $k_0, k_1, \dots, k_{m+2}$; the unknown coefficients $a_j$ have been successfully eliminated.


#### Computing the Vandermonde-like Determinant


By substituting the linear equations for each $k_i$ in terms of the private key $x$ into this determinant equation, we directly obtain a polynomial equation $P(x)=0\pmod{p}$. Finding the roots of this polynomial recovers the private key $x$.

The determinant of matrix $M$ can be expressed using cofactor expansion along the first column: $ \det(M) = \sum_{i=1}^{N} (-1)^{i+1} M_{i,1} \cdot \det(C_{i,1})\pmod{p}$, where $N = m+2$ is the dimension of the matrix, $M_{i,1} = k_i$ is the element in the $i$-th row and first column, and $C_{i,1}$ is the $(N-1) \times (N-1)$ submatrix (cofactor) obtained by removing the $i$-th row and first column of $M$.

When we remove the $i$-th row and 1st column from M, the resulting matrix $C_{i,1}$ has the form:
$$
C_{i,1} = \begin{pmatrix} k_0^m & k_0^{m-1} & \cdots & k_0^1 & 1 \\ \vdots & \vdots & \ddots & \vdots & \vdots \\ k_{i-2}^m & k_{i-2}^{m-1} & \cdots & k_{i-2}^1 & 1 \\ k_{i}^m & k_{i}^{m-1} & \cdots & k_{i}^1 & 1 \\ \vdots & \vdots & \ddots & \vdots & \vdots \\ k_{N-1}^m & k_{N-1}^{m-1} & \cdots & k_{N-1}^1 & 1 \end{pmatrix} \notag
$$

Observe that each row of this matrix consists of powers of a single base value $k_j$ (where $j \in \{0, 1, \dots, N-1\} \setminus \{i-1\}$), from power $m$ down to 0. Each submatrix $C_{i,1}$ is a standard $(N-1) \times (N-1)$ Vandermonde matrix whose base values are the set $\mathcal{K}_i = \{k_0, k_1, \dots, k_{N-1}\} \setminus \{k_{i-1}\}$.

The determinant of an $(N-1) \times (N-1)$ Vandermonde matrix with base values $\alpha_1, \dots, \alpha_{N-1}$ is known to be $\prod_{1 \le r < s \le N-1} (\alpha_s - \alpha_r)$. Therefore, for $\det(C_{i,1})$, we have: 
$$
\det(C_{i,1}) = \prod_{\substack{0 \le r < s \le N-1 \\ r, s \neq i-1}} (k_s - k_r) \notag
$$
Using the method described above, the complexity of the original `dpoly` calculation, roughly $O(N^4\log N)$, can be reduced to approximately $O(N^3 \log^2 N)$. This significant reduction in complexity makes the attack feasible.

#### Compute the roots and get $x$

Ultimately, you need to find the roots of $\det(M)$, which is the polynomial $P(x)\pmod{p}$. However, its degree is relatively high, so it cannot be solved directly using Sagemath's built-in `.roots()` function.

Since p is a prime number, we can use a common property of finite fields: all elements in $\mathbb{F}_p$ are roots of $x^p-x$. Therefore, we can reduce the degree of the polynomial $P(x)$ by computing the $\gcd(x^p - x, P(x))$, and then find the roots of the resulting, lower-degree polynomial.

This may yield multiple possible values for $x$. You simply need to validate them with Alice's public key to find the correct $x$, which will ultimately lead to the flag.

## Summary

This challenge was quite complex and was designed specifically for a 48-hour competition. 

***If anyone has ideas or wants to discuss this further deep research of techniques about RELATED NONCE ATTACK  described, please feel free to contact me.***