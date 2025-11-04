# Repository Guidelines

## Project Structure & Module Organization
Assignments live in top-level directories (e.g., `cats_game`, `chessland`) with `main.c`, `cases/` fixtures, optional `test_config.json`, and a git-ignored `build/`; `test_projects.py` drives compilation and checks.

## Agent Workflow
Scope is documentation only—never write or modify C sources. Read the project PDF, mirror the established README structure, focus on problem exposition (no solver hints or scoring notes), and update command snippets or links so they match the brief.

## README Structure & Formatting
Create `README.md` inside each project directory using this layout:
- `# <Project Title>` mirroring the PDF headline.
- One-sentence overview of the challenge.
- `## Objective` with a brief setup plus bullet list of practiced skills.
- `## Problem Description` covering story and mechanics; use numbered steps if describing sequences.
- `## Input Format` and `## Output Format` as bullet lists highlighting constraints.
- `## Example` with `### Input`/`### Output` code fences and optional explanation.
Match heading capitalization, stay in plain ASCII, and quote terminology directly from the PDF; omit hints, scoring tables, or solver-facing advice—even if the PDF mentions them—so the README stays focused on explaining the problem setup.

## Build, Test, and Development Commands
- `python3 test_projects.py <project>` builds with GCC (`-std=c11 -Wall -Wextra -O2`) and runs that project’s suite.
- `python3 test_projects.py --all` sweeps every project; rerun after touching shared tooling.
- `gcc -std=c11 -Wall -Wextra -O2 project/main.c -o project/build/project` is available for quick manual checks.

## Coding Style & Naming Conventions
Stick to C11 with two-space indents, same-line braces, lower_snake_case for symbols, and PascalCase for struct types; keep headers minimal and comment only when control flow or ownership is subtle.

## Testing Guidelines
Outputs must match `.out` fixtures byte-for-byte. Add cases as numbered pairs (`cases/sample05.in`/`.out`), note interactive quirks in `test_config.json`, and rerun `python3 test_projects.py <project>` (or `--all` after shared changes) before submitting.

## Commit & Pull Request Guidelines
Follow the repository’s concise, sentence-style commit summaries (e.g., “Solution to cats_game with small fix”), keep related work together, and add body notes when behavior shifts. Pull requests must list verification commands, link relevant briefs, and flag new tests or README updates for reviewers.

## Environment & Tooling Tips
Use Python 3.9+ and keep a GCC-compatible toolchain on your `PATH`; the tester writes artifacts under each `build/`, so leave those directories writable and run binaries from the project root to keep relative paths valid.
