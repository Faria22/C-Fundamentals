"""Compile and test configured C projects against their cases."""

import argparse
import difflib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASE_DIR_NAME = 'cases'
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
    build_dir = project_dir / DEFAULT_BUILD_DIR_NAME
    build_dir.mkdir(exist_ok=True)
    binary_path = build_dir / project_dir.name

    compile_cmd = [
        'gcc',
        '-std=c11',
        '-Wall',
        '-Wextra',
        '-O2',
        str(project_dir / DEFAULT_SOURCE_NAME),
        '-o',
        str(binary_path),
    ]
    result = subprocess.run(compile_cmd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Compilation failed for project '{project_dir.name}'\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
    return binary_path


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
        Success flag and failure explanation (if any).
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

    actual_output = execution.stdout.splitlines(keepends=True)
    expected_output = expected_path.read_text().splitlines(keepends=True)
    if actual_output == expected_output:
        return True, ''

    diff = ''.join(
        difflib.unified_diff(
            expected_output,
            actual_output,
            fromfile=f'expected/{expected_path.name}',
            tofile=f'actual/{input_path.stem}.out',
        ),
    )
    failure = f"Output mismatch for '{input_path.name}'\n{diff or '(no diff generated)'}"
    return False, failure


def test_project(project_name: str) -> tuple[bool, list[str]]:
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

    failures: list[str] = []
    for input_path, expected_path in case_pairs:
        success, message = run_single_case(binary, input_path, expected_path)
        if not success:
            failures.append(message)

    if failures:
        return False, failures
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

    overall_success = True
    for project in ordered:
        print(f'== Testing project: {project} ==')
        success, messages = test_project(project)
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
