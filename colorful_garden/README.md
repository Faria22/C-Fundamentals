# Colorful Garden
Reconstruct the garden’s red and black flowers from compact row and column group descriptions.

## Objective
Arrange a rectangular grid that honors every provided grouping clue while navigating intersecting constraints.
- Interpret run-length descriptions that count consecutive black-flower groups.
- Validate partial rows and columns as you explore configurations.
- Use recursive backtracking to search for a consistent layout.

## Problem Description
A tournament backdrop must mirror the “optimal” garden determined by a research firm. The firm lost the actual layout but shared compressed instructions that list, for every row and column, the sizes of consecutive black-flower groups encountered from the top or left. Red flowers fill the remaining cells, and the order of the groups matters.
1. Read the row clues, each giving the number of black groups followed by their sizes in left-to-right order.
2. Read the column clues, organized similarly from top to bottom.
3. Produce any grid of `r × c` plants using `B` for black and `r` for red so that every row and column matches its clue sequence exactly.

## Input Format
- First line: two integers `r c` (`1 ≤ r, c ≤ 15`) indicating the grid dimensions.
- Next `r` lines: each starts with an integer `gb` (number of black groups in that row) followed by `gb` positive integers for the group sizes, listed from left to right.
- Next `c` lines: each starts with an integer `gb` for that column’s groups followed by `gb` positive integers ordered from top to bottom.
- At least one valid arrangement is guaranteed.

## Output Format
- Print `r` lines, each containing `c` characters.
- Use `B` for a black-flowered plant and `r` for a red-flowered plant.
- The `i`‑th character on the `j`‑th line represents the plant in row `j`, column `i`.

## Example
### Input
```text
5 5
1 5
2 2 1
2 1 1
2 3 1
1 5
2 1 2
1 5
2 2 2
3 1 1 1
2 2 2
```

### Output
```text
BBBBB
rBBrB
rBrBr
BBBrB
BBBBB
```

This layout matches every row and column clue: each listed group of black flowers appears in the stated order, and all remaining cells are filled with red flowers.
