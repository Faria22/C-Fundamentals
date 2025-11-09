# Table Activation
Activate each tournament table in an order that respects the given tree while always picking the match that creates the least excitement.

## Objective
Rebuild the provided bracket by turning on tables in a valid sequence that preserves the original tree structure.

- Practice manipulating tree topologies in C.
- Use heaps/min queues to repeatedly select the next table by excitement.

## Problem Description
The tournament supplies two aligned arrays: the tree topology that tells where each table's winner advances, and the ordered skills of the players currently waiting at the leaf spots. Your program must stage matches so that the same tree structure emerges in real time. At every step, consider only tables whose child tables (if any) have already finished, compute each table’s excitement as the absolute skill difference of its two players, and activate the table with the smallest excitement; ties break by the lowest player skill involved. Continue activating tables until the championship table (the one whose parent is `-1`) completes.

## Input Format
- Line 1: integer `n` (`1 ≤ n ≤ 500000`) for the number of players.
- Line 2: `n - 1` integers `p1 … pn` (each `pi = -1` or `1 ≤ pi ≤ n - 1`) where `pi` denotes the table that the victor of table `i` advances to, and `-1` marks the championship table.
- Line 3: `n` distinct integers `s1 … sn` (`0 ≤ si ≤ 1000000000`) giving the skill for each player in initial order.

## Output Format
- Print `n - 1` lines; each line is the ID of the next table to activate so that every activation uses the least possible excitement available at that moment (breaking ties on lower player skill).

## Example
The sample below shows two independent tournament configurations.

### Input
```text
5
2 -1 4 2
5 1 4 2 3

6
-1 1 5 3 2
3 19 10 20 13 6
```

### Output
```text
3 4 1 2

4 3 5 2 1
```
