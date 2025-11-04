"""Compile and test configured C projects against their cases."""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CASE_DIR_NAME = 'cases'
CONFIG_FILE_NAME = 'test_config.json'
DEFAULT_BUILD_DIR_NAME = 'build'
DEFAULT_SOURCE_NAME = 'main.c'


def list_projects() -> list[str]:
    """Return repository directories that contain the expected source file.

    Returns
    -------
    list[str]
        Sorted project directory names.
    """
    projects = [
        entry.name
        for entry in ROOT.iterdir()
        if entry.is_dir() and not entry.name.startswith('.') and (entry / DEFAULT_SOURCE_NAME).is_file()
    ]
    return sorted(projects)


def find_case_dir(project_dir: Path) -> Path | None:
    """Locate the cases directory for the provided project.

    Parameters
    ----------
    project_dir : Path
        Directory containing the project sources.

    Returns
    -------
    Path | None
        The discovered cases directory, if present.
    """
    candidate = project_dir / CASE_DIR_NAME
    if candidate.is_dir():
        return candidate
    return None


def load_project_config(project_dir: Path) -> dict[str, Any] | None:
    """Load optional project-specific configuration file.

    Parameters
    ----------
    project_dir : Path
        Directory containing the project sources.

    Returns
    -------
    dict[str, Any] | None
        Parsed configuration dictionary when present.
    """
    config_path = project_dir / CONFIG_FILE_NAME
    if not config_path.is_file():
        return None
    with config_path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def compile_source(project_dir: Path, source_name: str, output_name: str) -> Path:
    """Compile the provided source file and return the emitted binary path.

    Parameters
    ----------
    project_dir : Path
        Directory containing the project sources.
    source_name : str
        Relative source filename to compile.
    output_name : str
        Desired output binary name.

    Returns
    -------
    Path
        Filesystem path to the compiled binary.
    """
    build_dir = project_dir / DEFAULT_BUILD_DIR_NAME
    build_dir.mkdir(exist_ok=True)
    binary_path = build_dir / output_name

    compile_cmd = [
        'gcc',
        '-std=c11',
        '-Wall',
        '-Wextra',
        '-O2',
        str(project_dir / source_name),
        '-o',
        str(binary_path),
    ]
    result = subprocess.run(compile_cmd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Compilation failed for project '{project_dir.name}' "
            f"(source '{source_name}')\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
    return binary_path


def compile_project(project_dir: Path) -> Path:
    """Compile the project's source file and return the binary path.

    Parameters
    ----------
    project_dir : Path
        Directory containing the project sources.

    Returns
    -------
    Path
        Filesystem path to the compiled binary.
    """
    return compile_source(project_dir, DEFAULT_SOURCE_NAME, project_dir.name)


def load_case_pairs(case_dir: Path) -> list[tuple[Path, Path]]:
    """Return ordered (input, expected) case pairs from the cases directory.

    Parameters
    ----------
    case_dir : Path
        Directory holding `.in` and `.out` files.

    Returns
    -------
    list[tuple[Path, Path]]
        Pairs of input and expected output files.
    """
    pairs: list[tuple[Path, Path]] = []
    for input_case in sorted(case_dir.glob('*.in')):
        expected = input_case.with_suffix('.out')
        if not expected.is_file():
            raise FileNotFoundError(
                f"Missing expected output file for test '{input_case.stem}' in {case_dir}",
            )
        pairs.append((input_case, expected))
    if not pairs:
        raise FileNotFoundError(f'No test cases found in {case_dir}')
    return pairs


def run_single_case(binary: Path, input_path: Path, expected_path: Path) -> tuple[bool, str]:
    """Execute the binary with the given input and compare output to expectation.

    Parameters
    ----------
    binary : Path
        Compiled program to execute.
    input_path : Path
        Test-case input file.
    expected_path : Path
        Test-case expected output file.

    Returns
    -------
    tuple[bool, str]
        Success flag and textual output (transcript or error details).
    """
    with input_path.open('rb') as input_file:
        execution = subprocess.run(
            [str(binary)],
            check=False,
            stdin=input_file,
            capture_output=True,
            text=True,
        )
    if execution.returncode != 0:
        failure = (
            f"Runtime error (exit code {execution.returncode}) for '{input_path.name}'\n"
            f'stdout:\n{execution.stdout}\n'
            f'stderr:\n{execution.stderr}'
        )
        return False, failure

    actual_text = execution.stdout
    expected_text = expected_path.read_text()
    if actual_text == expected_text:
        return True, ''

    def format_output(text: str) -> str:
        if not text:
            return '(empty output)\n'
        return text if text.endswith('\n') else f'{text}\n'

    failure = (
        f"Output mismatch for '{input_path.name}'\n"
        '=== Expected Output ===\n'
        f'{format_output(expected_text)}'
        '=== Actual Output ===\n'
        f'{format_output(actual_text)}'
    )
    return False, failure


def load_interactive_cases(cases_file: Path) -> list[dict[str, Any]]:
    """Load interactive case definitions in declaration order.

    Parameters
    ----------
    cases_file : Path
        JSON file outlining each interactive case.

    Returns
    -------
    list[dict[str, Any]]
        Parsed case entries.
    """
    with cases_file.open('r', encoding='utf-8') as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise TypeError(f"Interactive cases file '{cases_file}' must contain a list.")
    return data


def run_interactive_case(
    runner_path: Path,
    cases_file: Path,
    case_name: str,
    judge_binary: Path,
    solution_binary: Path,
    *,
    timeout: float | None = None,
) -> tuple[bool, str]:
    """Execute a single interactive case via the project runner script.

    Parameters
    ----------
    runner_path : Path
        Path to the runner Python script.
    cases_file : Path
        JSON definition listing available cases.
    case_name : str
        Identifier for the case to execute.
    judge_binary : Path
        Compiled judge binary path.
    solution_binary : Path
        Compiled solution binary path.
    timeout : float | None, optional
        Per-round timeout in seconds forwarded to the runner.

    Returns
    -------
    tuple[bool, str]
        Success flag and failure explanation (if any).
    """
    command = [
        sys.executable,
        str(runner_path),
        '--judge',
        str(judge_binary),
        '--solution',
        str(solution_binary),
        '--cases-file',
        str(cases_file),
        '--case',
        case_name,
    ]
    if timeout is not None:
        command.extend(['--timeout', f'{timeout:.6f}'])
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode == 0:
        return True, result.stdout

    failure = (
        f"Interactive case '{case_name}' failed.\n"
        f'stdout:\n{result.stdout}\n'
        f'stderr:\n{result.stderr}'
    )
    return False, failure


def test_interactive_project(
    project_dir: Path,
    config: dict[str, Any],
    *,
    case_name: str | None = None,
) -> tuple[bool, list[str]]:
    """Run interactive tests defined by the project configuration.

    Parameters
    ----------
    project_dir : Path
        Directory containing the interactive project.
    config : dict[str, Any]
        Parsed configuration dictionary for the project.

    Returns
    -------
    tuple[bool, list[str]]
        Success flag and any collected error messages.
    """
    missing = [
        key
        for key in ('runner', 'cases_file', 'judge_source')
        if not config.get(key)
    ]
    if missing:
        return False, [
            f"Interactive config for '{project_dir.name}' missing keys: {', '.join(missing)}.",
        ]

    runner_path = project_dir / config['runner']
    if not runner_path.is_file():
        return False, [
            f"Runner script '{config['runner']}' not found for project '{project_dir.name}'.",
        ]

    cases_path = project_dir / config['cases_file']
    if not cases_path.is_file():
        return False, [
            f"Cases file '{config['cases_file']}' not found for project '{project_dir.name}'.",
        ]

    judge_source = config['judge_source']
    judge_source_path = project_dir / judge_source
    if not judge_source_path.is_file():
        return False, [
            f"Judge source '{judge_source}' not found for project '{project_dir.name}'.",
        ]

    try:
        solution_binary = compile_project(project_dir)
    except RuntimeError as error:
        return False, [str(error)]

    try:
        judge_binary = compile_source(project_dir, judge_source, f'{project_dir.name}_judge')
    except RuntimeError as error:
        return False, [str(error)]

    try:
        cases = load_interactive_cases(cases_path)
    except (OSError, ValueError) as error:
        return False, [f'Failed to load interactive cases: {error}']

    if not cases:
        return False, [f"No interactive cases defined in '{cases_path}'."]

    timeout_value = None
    if 'timeout_seconds' in config:
        try:
            timeout_value = float(config['timeout_seconds'])
        except (TypeError, ValueError):
            return False, [
                f"Invalid 'timeout_seconds' value in config for '{project_dir.name}'.",
            ]

    filtered_cases = cases
    if case_name is not None:
        filtered_cases = [entry for entry in cases if entry.get('name') == case_name]
        if not filtered_cases:
            return False, [
                f"Interactive case '{case_name}' not found for project '{project_dir.name}'.",
            ]

    for entry in filtered_cases:
        entry_name = entry.get('name')
        if not entry_name:
            return False, ['Encountered interactive case entry without a name.']
        success, message = run_interactive_case(
            runner_path,
            cases_path,
            entry_name,
            judge_binary,
            solution_binary,
            timeout=timeout_value,
        )
        if success:
            print(f'{project_dir.name}: {entry_name} passed.')
            continue
        return False, [message]

    return True, []


def test_project(project_name: str, *, case_name: str | None = None) -> tuple[bool, list[str]]:
    """Compile the project and run all cases, collecting any failures.

    Parameters
    ----------
    project_name : str
        Name of the project directory to test.

    Returns
    -------
    tuple[bool, list[str]]
        Success flag and error messages for failing cases.
    """
    project_dir = ROOT / project_name
    if not project_dir.is_dir():
        return False, [f"Project '{project_name}' not found."]

    config = load_project_config(project_dir)
    if config and config.get('type') == 'interactive':
        return test_interactive_project(project_dir, config, case_name=case_name)

    case_dir = find_case_dir(project_dir)
    if case_dir is None:
        return False, [
            f"No '{CASE_DIR_NAME}' directory found for project '{project_name}'.",
        ]

    try:
        binary = compile_project(project_dir)
    except RuntimeError as error:
        return False, [str(error)]

    try:
        case_pairs = load_case_pairs(case_dir)
    except FileNotFoundError as error:
        return False, [str(error)]

    if case_name is not None:
        case_pairs = [
            pair for pair in case_pairs if pair[0].stem == case_name or pair[0].name == case_name
        ]
        if not case_pairs:
            return False, [
                f"Case '{case_name}' not found for project '{project_name}'.",
            ]

    for input_path, expected_path in case_pairs:
        success, message = run_single_case(binary, input_path, expected_path)
        if success:
            print(f'{project_name}: {input_path.name} passed.')
            continue
        return False, [message]

    return True, []


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser.

    Returns
    -------
    argparse.ArgumentParser
        Configured argument parser instance.
    """
    parser = argparse.ArgumentParser(
        description=f"Compile and run C projects against their test cases in '{CASE_DIR_NAME}'.",
    )
    parser.add_argument(
        'projects',
        nargs='*',
        help='One or more project directories located at the repository root.',
    )
    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        help='Run the test suite for every available project.',
    )
    parser.add_argument(
        '--case',
        help='Run only the specified case for the selected project.',
    )
    return parser


def main(argv: list[str]) -> int:
    """Parse arguments, run requested project suites, and return exit status.

    Parameters
    ----------
    argv : list[str]
        Command-line arguments excluding the program name.

    Returns
    -------
    int
        Shell-style success (0) or failure exit code.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    available = list_projects()

    selected: list[str] = []
    if args.all:
        if not available:
            print('No projects found in the repository.', file=sys.stderr)
            return 1
        selected.extend(available)
    selected.extend(args.projects)

    if not selected:
        if not available:
            print('No projects found in the repository.', file=sys.stderr)
            return 1
        print('Please specify at least one project to test or use --all.')
        print('Available projects:')
        for name in available:
            print(f' - {name}')
        return 1

    ordered: list[str] = []
    seen: set[str] = set()
    for project in selected:
        if project not in seen:
            seen.add(project)
            ordered.append(project)

    if args.case:
        if args.all:
            print('Cannot combine --all with --case.', file=sys.stderr)
            return 1
        if len(ordered) != 1:
            print('Specify exactly one project when using --case.', file=sys.stderr)
            return 1

    overall_success = True
    for project in ordered:
        print(f'== Testing project: {project} ==')
        success, messages = test_project(project, case_name=args.case)
        if success:
            print('All test cases passed.')
        else:
            overall_success = False
            for message in messages:
                print(message)
        print()

    if overall_success:
        print('All requested projects passed their test suites.')
        return 0

    print('At least one project failed.')
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
