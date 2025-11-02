# Chessland Attacks

Determine which rooks on a large 2D chessboard can attack each other using dynamic memory and array lists in C.

## Objective

This project provides practice with:
- Dynamic memory management (malloc, calloc, realloc, free)
- Array lists and struct-based data organization

## Problem Description

You are given the positions of several rooks on a chessboard.
Each rook can attack another if:
1. They share the same row or column, and
2. There are no other rooks between them.

Your task is to determine, for each rook, how many and which other rooks threaten it.

## Input Format
- The first line contains an integer n (1 ≤ n ≤ 100,000): the number of rooks.
- The next n lines each contain two integers r and c (1 ≤ r, c ≤ 1,000,000,000), representing the rook’s rank and file.
- The i-th rook has an ID = i.
- No two rooks occupy the same square.
- There are at most 10,000 unique ranks and 10,000 unique files.

## Output Format

Output n lines.
- The i-th line starts with an integer t, the number of rooks that can attack the i-th rook.
- Then list t integers — the IDs of the rooks that threaten it (order does not matter).
- All values on a line are separated by spaces.

## Example

### Input

```
3
1 1
5 5
6 1
```

### Output

```
1 3
0
1 1
```

Explanation:
Rooks 1 and 3 share the same column and can attack each other. Rook 2 is safe.
