# Handle Generator

Generate short “handles” from names by keeping only the first and last letter of each word and removing all spaces.

⸻

## Objective

This project provides practice with:
- Reading and writing to standard input/output in C
- Using loops and conditionals

⸻

## Problem Description

Given a list of names (one per line), each name consists only of upper/lowercase Latin letters and spaces.
For every name:
1. Keep only the first and last letter of each word.
2. Remove all spaces.
3. Output the resulting handle on its own line.

Example:

John Smith -> JnSh

⸻

## Input Format
- The first line contains an integer n (1 <= n <= 100,000): the number of names to process.
- The following n lines each contain one name (<= 100,000 characters, at least one non-space character).

⸻

## Output Format

Output n lines, each containing the generated handle.

⸻

## Example

### Input

```
3
John Smith
Felipe Faria
John Jacob Jingleheimer Schmidt
```

### Output

```
JnSh
FeFa
JnJbJrSt
```
