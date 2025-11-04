# Name Chaining

Assemble a promotional phrase by chaining all provided handles so that each word starts with the letter that ended the previous word.

## Objective

This project provides practice with:
- Recursive backtracking over constrained permutations
- String handling and bookkeeping in C

## Problem Description

Marketing for the handle generator needs a catchy slogan, and wordplay-loving residents of Gameland insist the phrase be "pretty." A phrase is pretty when every pair of adjacent words shares a boundary letter: the first word ends with the same character that begins the second. You are given a list of handles and must arrange them into a single pretty phrase that uses each handle exactly once. Any valid ordering is acceptable.

## Input Format
- The first line contains an integer `n` (1 ≤ n ≤ 12): the number of handles.
- The second line contains `n` space-separated handles.
- Each handle consists solely of lowercase Latin letters and has length between 1 and 20 characters.

## Output Format

Print one line containing a pretty phrase formed by the given handles, separated by single spaces. Every handle must appear exactly once. At least one valid ordering is guaranteed to exist.

## Example

### Sample 1 Input

```text
4
seek red karaoke dads
```

### Sample 1 Output

```text
red dads seek karaoke
```

### Sample 2 Input

```text
2
stressed desserts
```

### Sample 2 Output

```text
desserts stressed
```

## Explanation

- Sample 1: `red` ends with `d`, matching the start of `dads`. `dads` ends with `s`, matching `seek`, and `seek` ends with `k`, matching `karaoke`, so the chain is pretty.
- Sample 2: Either ordering works because each word starts and ends with complementary letters (`stressed` → `desserts` or vice versa).
