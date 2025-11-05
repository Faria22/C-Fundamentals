# Arcade Management
Track the arcade's "most valuable player" as people enter and leave throughout the day.

## Objective
Implement the event log for a retro arcade to reinforce dynamic data handling.
- Practice with linked lists and stack-driven state tracking
- Manage ordered arrivals and departures under last-in-first-out constraints

## Problem Description
Visitors arrive at the arcade with a recorded number of tokens, and departures occur without revealing who left. Customers refuse to exit until everyone who arrived after them is gone, so the crowd behaves like a stack. Each event line indicates either someone entering with their token total, someone leaving, or a request to report the current "most valuable player." Whenever a report is requested, the system must emit the name of the person in the arcade who entered with the most tokens; ties favor the most recent entrant with that amount.

## Input Format
- Each line starts with an integer `t` where `0 ≤ t ≤ 3` specifying the event type.
- `t = 0`: the day ends and processing stops.
- `t = 1`: followed by an integer `M` (`1 ≤ M ≤ 10^9`) and a string `S` (`1 ≤ |S| ≤ 20`) for a player entering with `M` tokens and name `S`.
- `t = 2`: a player leaves the arcade (no additional data).
- `t = 3`: request to output the current most valuable player.

## Output Format
- For every line where `t = 3`, print exactly one line containing the name of the current most valuable player in the arcade.
- When multiple players entered with the same token count, report the most recent entrant among them.

## Example
### Input
```text
1 5 Eric
1 10 John
1 2 Kate
3
1 30 Ash
3
2
2
3
2
3
0
```
### Output
```text
John
Ash
John
Eric
```
The sample demonstrates how the most valuable player changes as entrants join and leave under the stack-like departure rule.
