# Spad3kapig

## Description

r3girl finds herself facing a familiar challenge in a shadowy part of the Crypto Block, one with a notorious history. A previous trial, thought conquered, has returned with a sharp twist, demanding even greater speed and precision. The digital gauntlet has been thrown down once more, but this time, the window of opportunity is razor-thin – a mere 10 seconds to decipher the hand and claim victory in this Spad3kapig rematch. Only a seasoned SpadesAce has a chance to succeed under such intense pressure.

Note: The solution provided here works for both this challenge and the original challenge.

This challenge is based on tenspades by the Nautilus Institute and is released under the MIT License. The full text of the license is included with the challenge files.

## Flag

`R3CTF{also_easy_to_solve_to_be_spades_ace_king_finally_not_only_a_brute_force_challenge_in_DEFCON.it_also_can_be_a_cryptgraphy_challenge}`

## Solution

### Overview

Of course, before starting cryptographic analysis, you need to analyze the logic in the binary file. You might want to find a reverse engineering expert to help you examine it. The following mainly describes how the cryptographic analysis part is conducted.

In each connection to the server, the `team_seed` changes, making brute force approaches infeasible. Additionally, you need to obtain the `team_seed` within 10 seconds.

In the challenge, you can get multiple results of `rng.next()` with `team_seed,random_device()`, allowing you to collect sufficient information related to `team_seed`. Below is a general description of how to attack this challenge using cryptanalysis methods.

Note: *This challenge had an unintended solution, which was very frustrating for me. It was solved by using brute-force with optimizations, without needing the intended method for solving a Hidden Number Problem (HNP) with a three-layer modulus.*

### First. recover the rng.next() from deck. 

Upon analyzing the deck's shuffle algorithm, we can recover `[rng.next() % (i+1) for i in range(52,0,-1)]`.

However, for this challenge, we only need information about the last card. Since the server output `seed` is related to the current state, we can determine the specific value of `rng.next()%52` for each state change by inputting incorrect cards and observing the correct card sequence.

### Second. recover the `team_seed` then get flag.
The relevant random number generation uses $a=team_{seed} \oplus 0x77777777, c=2025$, and the `next()` function outputs $new\_state = a\cdot old\_state + c \pmod{m}$.

In each round, the output $seed$ is the current $state$. We know the specific values where $(a \cdot seed_i + c \pmod{m}) \pmod{52} = r_i$, which can be expressed as:

$$
a\cdot seed_i + c \equiv r_i + k_i \cdot 52\pmod{m}
$$

However, since this operates under C++ language constraints, overflow occurs. This is equivalent to:

$$
a\cdot seed_i +c \pmod{2^{32}}\pmod{m}\pmod{52} = r_i\\
a\cdot seed_i + c \equiv r_i+k_i\cdot 52 + t_i\cdot m \pmod{2^{32}}
$$

Where $t_i \in \{0,1\}$ due to the modulo $2^{32}$ operation, and $k_i$ values are relatively small. Since $\gcd(52,2^{32}) = 4$, we need to consider $r_i\pmod{13}$. By using the Hidden Number Problem (HNP) approach, we can successfully recover the value of $a$, which allows us to determine the `team_seed` generated in the current environment. 

Once we've recovered the entire RNG state, we simply need to perform one more LCG deck operation to get the flag.

## Summary

Perhaps we spent 48 hours guessing during DEFCON CTF 2025 Quals, but in the end, we still found cryptographic analysis points that could be exploited. 

