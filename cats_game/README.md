# Cat's Game

Play an interactive hot-or-cold guessing game against Patty Kerry to recover your stolen coins using optimal search strategies in C.

## Objective

This project provides practice with:
- Writing interactive programs that coordinate stdin/stdout with an automated judge
- Implementing binary search (and related heuristics) to minimise the number of guesses
- Managing state across iterative guesses (previous guess, delta comparisons, remaining attempts)

## Problem Description

Patty chooses a secret integer between 1 and `n`. Your program must discover the value using as few guesses as possible. After each incorrect guess, Patty tells you whether the new guess is **Warmer**, **Colder**, or **No change** compared to the last attempt. If you exceed the allowed number of guesses or step outside the permitted range, the game ends immediately.

Your program must:
1. Read a single integer `n` that indicates the maximum possible value.
2. Repeatedly print guesses (integers between -1,000,000,000 and 1,000,000,000).
3. Read responses from Patty after every guess to update your search strategy.
4. Stop after printing the correct value (Patty replies with `Yes!!!`) or when the judge ends the game.

The optimal strategy fits within `1 + 2 * ceil(log2(n))` guesses.

## Input / Output Interaction

Because the judge is interactive, inputs and outputs alternate:

1. Judge prints `n` on a single line.
2. Your program prints a guess.
3. Judge returns one of:
   - `Yes!!!` when the guess is correct (terminate).
   - `No.` optionally followed by `Warmer.`, `Colder.`, or `No change.` when the guess is wrong.
   - `Game Over.` if you violate the rules or run out of guesses.
4. Steps 2–3 repeat until termination.

## Sample Interaction

```
Judge -> 20
You   -> 5
Judge -> No.
You   -> 15
Judge -> No. Warmer.
You   -> 20
Judge -> No. Colder.
You   -> 13
Judge -> Yes!!!
```
