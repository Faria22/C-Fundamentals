#!/usr/bin/env python3
"""Interactive runner for Cat's Game test cases."""

from __future__ import annotations

import argparse
import json
import selectors
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


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
    parser.add_argument('--cases-file', type=Path, required=True, help='JSON file describing the available cases.')
    parser.add_argument('--case', required=True, help='Name of the case entry to execute.')
    parser.add_argument('--timeout', type=float, default=10.0, help='Per-case timeout in seconds (default: 10).')
    return parser.parse_args()


def load_cases(cases_path: Path) -> dict[str, dict[str, Any]]:
    """Load case definitions indexed by case name.

    Parameters
    ----------
    cases_path : Path
        Location of the JSON file with case descriptions.

    Returns
    -------
    dict[str, dict[str, Any]]
        Mapping from case name to configuration objects.
    """
    with cases_path.open('r', encoding='utf-8') as handle:
        raw_cases = json.load(handle)
    return {entry['name']: entry for entry in raw_cases}


def _register_stream(selector: selectors.BaseSelector, fileobj: Any, token: tuple[str, str]) -> None:
    if fileobj is None:
        return
    selector.register(fileobj, selectors.EVENT_READ, data=token)


def _read_line(fileobj: Any) -> str | None:
    line = fileobj.readline()
    if not line:
        return None
    return line


def execute_case(judge_cmd: list[str], solution_cmd: list[str], timeout: float) -> dict[str, Any]:
    """Execute a single judge / solution interaction and capture transcripts.

    Parameters
    ----------
    judge_cmd : list[str]
        Command used to spawn the judge process.
    solution_cmd : list[str]
        Command used to spawn the contestant solution.
    timeout : float
        Maximum wall-clock seconds allowed for the round.

    Returns
    -------
    dict[str, Any]
        Aggregated exit codes, timeout flag, and collected streams.
    """
    solver = subprocess.Popen(
        solution_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    judge = subprocess.Popen(
        judge_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    selector = selectors.DefaultSelector()
    _register_stream(selector, solver.stdout, ('solver', 'stdout'))
    _register_stream(selector, solver.stderr, ('solver', 'stderr'))
    _register_stream(selector, judge.stdout, ('judge', 'stdout'))
    _register_stream(selector, judge.stderr, ('judge', 'stderr'))

    transcripts = {
        'solver_stdout': '',
        'solver_stderr': '',
        'judge_stdout': '',
        'judge_stderr': '',
    }

    solver_closed = {'stdout': False, 'stderr': False}
    judge_closed = {'stdout': False, 'stderr': False}
    start_time = time.perf_counter()
    timed_out = False

    try:
        while True:
            remaining = timeout - (time.perf_counter() - start_time)
            if remaining <= 0:
                timed_out = True
                break

            events = selector.select(timeout=min(0.1, remaining))
            if not events:
                if solver.poll() is not None and judge.poll() is not None:
                    break
                continue

            for key, _ in events:
                origin, stream = key.data
                line = _read_line(key.fileobj)
                if line is None:
                    selector.unregister(key.fileobj)
                    if origin == 'solver':
                        solver_closed[stream] = True
                    else:
                        judge_closed[stream] = True
                        if stream == 'stdout' and solver.stdin:
                            solver.stdin.close()
                    continue

                transcripts[f'{origin}_{stream}'] += line

                if origin == 'judge' and stream == 'stdout' and solver.stdin:
                    solver.stdin.write(line)
                    solver.stdin.flush()
                elif origin == 'solver' and stream == 'stdout' and judge.stdin:
                    judge.stdin.write(line)
                    judge.stdin.flush()

            if solver.poll() is not None and judge.poll() is not None:
                break

    finally:
        selector.close()

    if solver.stdin:
        solver.stdin.close()
        solver.stdin = None
    if judge.stdin:
        judge.stdin.close()
        judge.stdin = None

    if timed_out:
        solver.kill()
        judge.kill()

    try:
        stdout, stderr = solver.communicate(timeout=0.1)
        transcripts['solver_stdout'] += stdout or ''
        transcripts['solver_stderr'] += stderr or ''
    except subprocess.TimeoutExpired:
        solver.kill()
        stdout, stderr = solver.communicate()
        transcripts['solver_stdout'] += stdout or ''
        transcripts['solver_stderr'] += stderr or ''

    try:
        stdout, stderr = judge.communicate(timeout=0.1)
        transcripts['judge_stdout'] += stdout or ''
        transcripts['judge_stderr'] += stderr or ''
    except subprocess.TimeoutExpired:
        judge.kill()
        stdout, stderr = judge.communicate()
        transcripts['judge_stdout'] += stdout or ''
        transcripts['judge_stderr'] += stderr or ''

    return {
        'solver_code': solver.returncode or 0,
        'judge_code': judge.returncode or 0,
        'timed_out': timed_out,
        'timeout_seconds': timeout,
        **transcripts,
    }


def format_block(label: str, payload: str) -> str:
    """Return a labelled block when the payload contains text.

    Returns
    -------
    str
        Formatted block or an empty string when no content exists.
    """
    text = payload.strip()
    if not text:
        return ''
    return f'{label}:\n{text}'


def print_transcript(case_name: str, target: int, result: dict[str, Any]) -> None:
    """Emit the solver and judge transcripts for a completed case."""
    sections = [
        format_block('Solver stdout', result['solver_stdout']),
        format_block('Solver stderr', result['solver_stderr']),
        format_block('Judge stdout', result['judge_stdout']),
        format_block('Judge stderr', result['judge_stderr']),
    ]
    body = '\n'.join(filter(None, sections))
    if body:
        print(f'--- {case_name} / target {target} ---')
        print(body)
        print()


def evaluate_round(result: dict[str, Any]) -> tuple[bool, str]:
    """Summarise the outcome of an interactive round.

    Returns
    -------
    tuple[bool, str]
        Success flag and accompanying message.
    """
    if result.get('timed_out'):
        timeout = result.get('timeout_seconds', 0)
        return False, f'Round exceeded {timeout:.1f} seconds.'
    if result['solver_code'] != 0:
        return False, f"Solution exited with code {result['solver_code']}."
    if result['judge_code'] != 0:
        return False, f"Judge exited with code {result['judge_code']}."
    combined = f"{result['judge_stdout']}\n{result['judge_stderr']}"
    if 'Game Over.' in combined:
        return False, "'Game Over.' detected in judge output."
    if 'Yes!!!' not in combined:
        return False, 'Judge never confirmed success.'
    return True, ''


def main() -> int:
    """Entry point for the Cat's Game interactive runner CLI.

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
    targets = [int(value) for value in case.get('answers', [])]
    if not targets:
        targets = [max_value]

    for target in targets:
        judge_cmd = [args.judge, str(max_value), str(target)]
        solver_cmd = [args.solution]
        result = execute_case(judge_cmd, solver_cmd, timeout=args.timeout)
        print_transcript(args.case, target, result)
        success, message = evaluate_round(result)
        if not success:
            print(message, file=sys.stderr)
            return 1

    print(f'{args.case}: passed ({len(targets)} target(s) tested).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
