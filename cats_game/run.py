#!/usr/bin/env python3
"""Interactive runner for Cat's Game test cases."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any


class SubprocessThread(threading.Thread):
    """Spawn a subprocess and record its exit code and streams."""

    def __init__(
        self,
        args: list[str],
        *,
        stdin_pipe: Any = subprocess.PIPE,
        stdout_pipe: Any = subprocess.PIPE,
        stderr_pipe: Any = subprocess.PIPE,
    ) -> None:
        super().__init__()
        self.p = subprocess.Popen(
            args,
            stdin=stdin_pipe,
            stdout=stdout_pipe,
            stderr=stderr_pipe,
            text=True,
        )
        self.return_code: int | None = None
        self.stdout: str | None = None
        self.stderr: str | None = None

    def run(self) -> None:
        """Wait for the subprocess to finish and capture its streams."""
        try:
            self.stdout, self.stderr = self.p.communicate()
        finally:
            self.return_code = self.p.returncode


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the interactive runner.

    Returns
    -------
    argparse.Namespace
        Parsed arguments describing the execution context.
    """
    parser = argparse.ArgumentParser(description="Run interactive Cat's Game cases.")
    parser.add_argument('--judge', required=True, help='Path to the compiled judge binary.')
    parser.add_argument('--solution', required=True, help='Path to the contestant solution binary.')
    parser.add_argument(
        '--cases-file',
        type=Path,
        required=True,
        help='JSON file describing the available cases.',
    )
    parser.add_argument(
        '--case',
        required=True,
        help='Name of the case entry to execute (see the JSON file).',
    )
    return parser.parse_args()


def load_cases(cases_path: Path) -> dict[str, dict[str, Any]]:
    """Load the JSON case definitions indexed by their names.

    Parameters
    ----------
    cases_path : Path
        JSON file with case descriptions.

    Returns
    -------
    dict[str, dict[str, Any]]
        Mapping of case names to definition dictionaries.
    """
    with cases_path.open('r', encoding='utf-8') as handle:
        raw_cases = json.load(handle)
    return {entry['name']: entry for entry in raw_cases}


def adaptive_targets(max_value: int) -> list[int]:
    """Generate representative targets for adaptive test scenarios.

    Parameters
    ----------
    max_value : int
        Upper bound provided by the judge for the case.

    Returns
    -------
    list[int]
        Deterministic set of target values to probe.
    """
    candidates = {
        1,
        max_value,
        max_value // 2,
        max_value // 3,
        max_value // 4,
        max_value - 1,
    }
    return sorted({target for target in candidates if 1 <= target <= max_value})


def run_single_round(
    judge_cmd: list[str],
    solution_cmd: list[str],
) -> dict[str, Any]:
    """Execute one judge/solution interaction and capture process results.

    Parameters
    ----------
    judge_cmd : list[str]
        Command used to launch the judge process.
    solution_cmd : list[str]
        Command used to launch the contestant solution.

    Returns
    -------
    dict[str, Any]
        Collected execution metadata and buffered streams.
    """
    solver_thread = SubprocessThread(solution_cmd)
    judge_thread = SubprocessThread(
        judge_cmd,
        stdin_pipe=solver_thread.p.stdout,
        stdout_pipe=solver_thread.p.stdin,
    )

    solver_thread.start()
    judge_thread.start()
    judge_thread.join()
    solver_thread.join()

    # Ensure process pipes are closed.
    if solver_thread.p.stdin:
        solver_thread.p.stdin.close()

    return {
        'solver_code': solver_thread.return_code or 0,
        'judge_code': judge_thread.return_code or 0,
        'solver_stdout': solver_thread.stdout or '',
        'solver_stderr': solver_thread.stderr or '',
        'judge_stdout': judge_thread.stdout or '',
        'judge_stderr': judge_thread.stderr or '',
    }


def evaluate_round_result(result: dict[str, Any]) -> tuple[bool, str]:
    """Interpret the recorded output from an interaction round.

    Parameters
    ----------
    result : dict[str, Any]
        Metadata captured during an interaction run.

    Returns
    -------
    tuple[bool, str]
        Success flag and failure explanation when applicable.
    """
    solver_code = result['solver_code']
    judge_code = result['judge_code']
    judge_stdout = result['judge_stdout']
    judge_stderr = result['judge_stderr']

    if solver_code != 0:
        return False, f'Solution exited with code {solver_code}.'

    if judge_code != 0:
        return False, f'Judge exited with code {judge_code}.'

    combined = f'{judge_stdout}\n{judge_stderr}'
    if 'Game Over.' in combined:
        return False, "'Game Over.' detected in judge output."

    if 'Yes!!!' not in combined:
        return False, 'Judge never confirmed success.'

    return True, ''


def main() -> int:
    """Entry point for the Cat's Game interactive runner.

    Returns
    -------
    int
        Shell-style exit status.
    """
    args = parse_args()
    cases = load_cases(args.cases_file)
    if args.case not in cases:
        print(f'Unknown case {args.case!r}.', file=sys.stderr)
        return 2

    case = cases[args.case]
    max_value = int(case['max'])
    targets = [int(value) for value in case['answers']] if case.get('answers') else adaptive_targets(max_value)

    failures: list[str] = []
    for target in targets:
        judge_cmd = [args.judge, str(max_value), str(target)]
        solution_cmd = [args.solution]

        result = run_single_round(judge_cmd, solution_cmd)
        success, message = evaluate_round_result(result)
        if not success:
            detail = (
                f'Target {target} failed.\n'
                f'Judge stdout:\n{result["judge_stdout"]}\n'
                f'Judge stderr:\n{result["judge_stderr"]}\n'
                f'Solver stdout:\n{result["solver_stdout"]}\n'
                f'Solver stderr:\n{result["solver_stderr"]}\n'
                f'Reason: {message}'
            )
            failures.append(detail)
            break

    if failures:
        print('\n'.join(failures), file=sys.stderr)
        return 1

    print(f'{args.case}: passed ({len(targets)} target(s) tested).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
