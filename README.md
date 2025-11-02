# C Fundamentals

This repository contains my complete reimplementation of my CS1 assignments in C, redone from scratch to strengthen my programming fundamentals and demonstrate mastery of core C concepts.

## Topics Covered
- Basic I/O and control flow
- Functions and recursion
- Arrays and strings
- Pointers and dynamic memory
- Structs and complex data types
- Basic algorithms (sorting, searching)

## Prerequisites
- Python 3.9 or newer for the `test_projects.py` runner
- A C toolchain such as GCC or Clang available on your `PATH`

## Repository Layout
- `test_projects.py` — Python tester that builds projects and verifies cases
- `<project>/main.c` — entry point for each assignment reimplementation
- `<project>/cases/` — paired `.in`/`.out` files that drive automated checks
- `<project>/build/` — generated binaries created when running the tester (ignored by git)
- `<project>/test_config.json` — optional overrides for projects with specialized tests (e.g., interactive cases)

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
