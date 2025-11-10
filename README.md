# C Fundamentals

This repository contains my complete reimplementation of my CS1 assignments in C, redone from scratch to strengthen my programming fundamentals and demonstrate mastery of core C concepts.

## Topics Covered
- Interactive standard I/O
- Dynamic memory management
- Stacks
- Linked lists
- Custom sorting
- Constraint satisfaction via backtracking
- Binary search trees
- String normalization
- Permutation search

## Prerequisites
- Python 3.9 or newer for the `test_projects.py` runner
- A C toolchain such as GCC or Clang available on your `PATH`

## Repository Layout
- `test_projects.py` — Python tester that builds projects and verifies cases
- `<project>/main.c` — entry point for each assignment reimplementation
- `<project>/cases/` — paired `.in`/`.out` files that drive automated checks
- `<project>/build/` — generated binaries created when running the tester (ignored by git)
- `<project>/test_config.json` — optional overrides for projects with specialized tests (e.g., interactive cases)

## Projects
- `arcade_management` — Streams arcade arrivals/departures, maintaining a stack-like crowd to identify the current most valuable player on demand.
- `cats_game` — Plays a warmer/colder interactive guessing challenge that homes in on Patty’s secret number within strict guess limits.
- `chessland` — Groups rooks by rows and columns to list every attacker relationship across a massive chessboard.
- `coin_organization` — Converts mixed token/bill payments with a deferred exchange rate and sorts customers by their unified totals.
- `colorful_garden` — Reconstructs a red/black flower grid from row and column run-length clues via recursive backtracking.
- `exciting_tournament` — Simulates a single-elimination bracket driven by table activation order while summing total excitement.
- `handle_generator` — Reduces each provided name to a spaceless handle built from the boundary letters of every word.
- `name_chaining` — Orders precomputed handles so consecutive words share boundary letters, guaranteeing a “pretty” promotional phrase.

## How to Run
Use the bundled Python test runner to compile and validate one or more projects:

```bash
python3 test_projects.py chessland
```

Pass multiple project names to run their test suites sequentially:

```bash
python3 test_projects.py chessland handle_generator
```

Run every project's suite at once with the `--all` flag:

```bash
python3 test_projects.py --all
```

If you omit project names (and skip `--all`), the script lists the available options.
