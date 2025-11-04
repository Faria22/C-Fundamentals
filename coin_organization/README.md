# Coin Organization
Sort incoming customer payments by their total value once two in-game currencies are reconciled to a shared rate.

## Objective
Organize mixed-denomination payments from multiple customers using the latest exchange rate between tokens and bills.
- Practice parsing structured input with per-record metadata.
- Reinforce integer arithmetic when converting values across denominations.
- Implement custom sorting logic based on derived totals.

## Problem Description
You manage a surge of orders in Gameland and must list customers from highest to lowest spender. Each person pays using a combination of tokens and bills, and the relative value between the two currencies shifts frequently. After receiving every customer's contribution, the current exchange rule—stated as “a tokens is worth b bills”—arrives. Use that rule to translate each payment into a comparable total and output the names in descending order of paid value.

## Input Format
- First line: integer `n` (1 ≤ n ≤ 100000) for the number of customers.
- Next `n` lines: a customer name (1–20 characters, no whitespace) followed by two integers `ti` and `bi` (0 ≤ ti, bi ≤ 100000) giving tokens and bills contributed.
- Final line: two integers `a` and `b` (1 ≤ a, b ≤ 100000) declaring that `a` tokens are equivalent to `b` bills.

## Output Format
- Output `n` lines listing customer names.
- Order names from the highest total payment to the lowest based on the provided exchange rate.

## Example
### Input
```text
5
John 3 10
Jacob 7 7
Rob 5 8
Nancy 4 5
Phil 11 4
10 13
```

### Output
```text
Phil
Jacob
Rob
John
Nancy
```

The ordering reflects each payment’s total once all tokens and bills are converted using the `10` tokens = `13` bills exchange rule.
