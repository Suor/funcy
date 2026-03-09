#!/usr/bin/env python3
"""Runner for type-checking tests.

Runs a type checker (pyright, mypy, or ty) on type_tests/ and validates
that errors match the expected markers in test files.

Markers:
    # E: <reason>         — must produce a type error (real error we catch)
    # XFAIL: <reason>     — currently errors, but shouldn't ideally (all checkers)
    # XFAIL[ty]: <reason> — known failure for a specific checker
    # R: <type>           — reveal_type must match this type (substring match after normalization)

Usage:
    python type_tests/run.py pyright
    python type_tests/run.py mypy
    python type_tests/run.py ty
"""
import glob
import os
import re
import subprocess
import sys

TEST_DIR = os.path.dirname(__file__) or "."


def parse_markers(test_dir, checker):
    """Parse test files for # E:, # XFAIL:, and # R: markers.

    Returns (expected, skipped, reveals) where:
        expected: {filepath: set of line numbers} — lines that must error
        skipped: {filepath: set of line numbers} — lines to ignore
        reveals: {filepath: {lineno: pattern}} — expected reveal_type patterns
    """
    expected = {}
    skipped = {}
    reveals = {}
    has_error_marker = {}  # lines with # E: regardless of XFAIL
    for filepath in sorted(glob.glob(os.path.join(test_dir, "test_*.py"))):
        exp = set()
        skip = set()
        e_lines = set()
        rev = {}
        with open(filepath) as f:
            for lineno, line in enumerate(f, 1):
                # Check for checker-specific XFAIL first (can coexist with # E:)
                xfail_match = re.search(r"# XFAIL\[([^\]]+)\]:", line)
                is_xfail_for_checker = (
                    xfail_match and checker in xfail_match.group(1).split(",")
                )
                if "# XFAIL:" in line or is_xfail_for_checker:
                    skip.add(lineno)
                if "# E:" in line:
                    e_lines.add(lineno)
                    if not is_xfail_for_checker:
                        exp.add(lineno)
                # R: marker can coexist with XFAIL markers
                r = re.search(r"# R: (.+?)(?:\s*# (?:XFAIL|E:).*)?$", line)
                if r:
                    rev[lineno] = r.group(1).strip()
        abspath = os.path.abspath(filepath)
        if exp:
            expected[abspath] = exp
        if skip:
            skipped[abspath] = skip
        if rev:
            reveals[abspath] = rev
        if e_lines:
            has_error_marker[abspath] = e_lines
    return expected, skipped, reveals, has_error_marker


def normalize_type(revealed, checker):
    """Normalize a revealed type string to a canonical form for exact comparison.

    Handles differences between mypy, pyright, and ty:
    - mypy: "def (*Any, **Any) -> str", "def (str) -> int", "_T`6"
    - pyright: "_T@make_func", "(str | int)" parenthesized unions
    - ty: "(...) -> str", "(str, /) -> int", "_T'return"
    Canonical form: "(...) -> str", "(str) -> int", "_T"
    """
    s = revealed
    if checker == "mypy":
        # mypy uses qualified names: builtins.int -> int, builtins.str -> str
        s = re.sub(r'builtins\.', '', s)
        # Remove module prefixes for common types (handles multiple levels like funcy.objects.X)
        s = re.sub(r'\b(?:[a-z_][a-z_0-9]*\.)+([A-Z])', r'\1', s)
        # mypy omits -> None in revealed types, add it back for consistency
        if s.startswith("def ") and "->" not in s:
            s = s + " -> None"
        # Normalize Callable[..., X]: mypy "(*Any, **Any)" -> "..."
        s = re.sub(r'\(\*Any, \*\*Any\)', '(...)', s)
        # Normalize TypeVar suffixes: mypy uses _T`123
        s = re.sub(r'`\d+', '', s)
    if checker == "pyright":
        # Normalize TypeVar suffixes: pyright uses _T@func_name
        s = re.sub(r'@\w+', '', s)
        # Strip parentheses around union types in return position: "-> (A | B)" -> "-> A | B"
        s = re.sub(r'->\s*\(([^()]+)\)', r'-> \1', s)
    if checker == "ty":
        # Strip positional-only marker at end of params: ", /)" -> ")"
        s = re.sub(r', /\)', ')', s)
        # Normalize TypeVar suffixes: ty uses _T'word
        s = re.sub(r"'[a-z_]+", '', s)
        # ty uses Unknown for unresolved types
        s = re.sub(r'\bUnknown\b', 'Any', s)
    # Strip "def name" prefix: mypy uses "def (...)", ty uses "def name(...)"
    s = re.sub(r'^def \w*\s*', '', s)
    # Strip generic TypeVar prefix: [_T] or [_K, _V] at start
    s = re.sub(r'^\[[\w, ]+\]\s*', '', s)
    # Normalize bottom type: pyright uses NoReturn, mypy/ty use Never
    s = re.sub(r'\bNoReturn\b', 'Never', s)
    # Normalize whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def run_pyright(test_dir):
    """Run pyright and parse errors and reveal_type notes."""
    result = subprocess.run(
        ["pyright", "--outputjson", test_dir],
        capture_output=True, text=True,
    )
    errors = {}  # {filepath: {lineno: message}}
    reveals = {}  # {filepath: {lineno: revealed_type}}
    try:
        import json
        data = json.loads(result.stdout)
        for diag in data.get("generalDiagnostics", []):
            filepath = os.path.abspath(diag["file"])
            lineno = diag["range"]["start"]["line"] + 1  # pyright uses 0-based
            if diag.get("severity") == "error":
                errors.setdefault(filepath, {})[lineno] = diag.get("message", "")
            elif diag.get("severity") == "information":
                m = re.search(r'Type of ".+?" is "(.+)"', diag.get("message", ""))
                if m:
                    reveals.setdefault(filepath, {})[lineno] = m.group(1)
    except (json.JSONDecodeError, KeyError):
        print("Failed to parse pyright output", file=sys.stderr)
        print(result.stdout[:2000], file=sys.stderr)
        sys.exit(2)
    return errors, reveals


def run_mypy(test_dir):
    """Run mypy and parse errors and reveal_type notes."""
    result = subprocess.run(
        ["python", "-m", "mypy", test_dir, "--no-error-summary"],
        capture_output=True, text=True,
    )
    errors = {}  # {filepath: {lineno: message}}
    reveals = {}  # {filepath: {lineno: revealed_type}}
    for line in result.stdout.splitlines():
        # mypy error format: file.py:lineno: error: message [code]
        match = re.match(r"(.+?):(\d+):\s*error:\s*(.*)", line)
        if match:
            filepath = os.path.abspath(match.group(1))
            lineno = int(match.group(2))
            errors.setdefault(filepath, {})[lineno] = match.group(3).strip()
            continue
        # mypy reveal format: file.py:lineno: note: Revealed type is "..."
        match = re.match(r'(.+?):(\d+):\s*note:\s*Revealed type is "(.+)"', line)
        if match:
            filepath = os.path.abspath(match.group(1))
            lineno = int(match.group(2))
            reveals.setdefault(filepath, {})[lineno] = match.group(3)
    return errors, reveals


def run_ty(test_dir):
    """Run ty and parse errors and reveal_type notes."""
    result = subprocess.run(
        ["ty", "check", test_dir],
        capture_output=True, text=True,
    )
    errors = {}  # {filepath: {lineno: message}}
    reveals = {}  # {filepath: {lineno: revealed_type}}
    output = (result.stdout + result.stderr).splitlines()
    in_error = False
    in_reveal = False
    error_message = ""
    reveal_file = None
    reveal_line = 0
    for line in output:
        # ty format:
        #   error[rule-name]: Message text
        #     --> file.py:lineno:col
        #   info[revealed-type]: Revealed type
        #     --> file.py:lineno:col
        #        | ^^^ `type_here`
        m_err = re.match(r"\s*error\[.+?\]:\s*(.*)", line)
        if m_err:
            in_error = True
            in_reveal = False
            error_message = m_err.group(1).strip()
        elif re.match(r"\s*info\[revealed-type\]:", line):
            in_reveal = True
            in_error = False
        elif re.match(r"\s*(?:info|warning)", line):
            in_error = False
            in_reveal = False
        elif in_error:
            match = re.match(r"\s*-->\s*(.+?):(\d+):\d+", line)
            if match:
                filepath = os.path.abspath(match.group(1))
                lineno = int(match.group(2))
                errors.setdefault(filepath, {})[lineno] = error_message
                in_error = False
        elif in_reveal:
            # Try to get the type from the ^^^ `type` line
            m = re.search(r'`(.+?)`\s*$', line)
            if m and reveal_file is not None:
                reveals.setdefault(reveal_file, {})[reveal_line] = m.group(1)
                in_reveal = False
            else:
                match = re.match(r"\s*-->\s*(.+?):(\d+):\d+", line)
                if match:
                    reveal_file = os.path.abspath(match.group(1))
                    reveal_line = int(match.group(2))
    return errors, reveals


CHECKERS = {
    "pyright": run_pyright,
    "mypy": run_mypy,
    "ty": run_ty,
}

# Names intentionally not tested (stdlib re-exports, etc.)
COVERAGE_SKIP = {
    "accumulate", "chain", "contextmanager", "count", "cycle",
    "nullcontext", "partial", "reduce", "repeat", "suppress",
    "unwrap", "ContextDecorator",
}


def check_coverage(test_dir):
    """Check that all public funcy names are actually used in type tests."""
    import ast
    sys.path.insert(0, os.path.join(os.path.dirname(test_dir)))
    import funcy

    public_names = set(funcy.__all__)

    # Collect names actually used (not just imported) in test files.
    # ast.Name nodes only appear for real references, not inside import statements
    # (those use ast.alias), so any ast.Name matching a funcy name is a real usage.
    used = set()
    for filepath in sorted(glob.glob(os.path.join(test_dir, "test_*.py"))):
        with open(filepath) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in public_names:
                used.add(node.id)

    missing = public_names - used - COVERAGE_SKIP
    if missing:
        print("FAIL - public funcy names not tested:")
        for name in sorted(missing):
            print(f"  {name}")
        sys.exit(1)
    else:
        print(f"OK - all {len(public_names)} public funcy names are covered "
              f"({len(COVERAGE_SKIP)} skipped)")


def find_stale_xfails(skip, error_markers, actual_lines, expected_rev, actual_rev, checker):
    """Find XFAIL lines that no longer fail.

    Two cases:
    - # E: + # XFAIL[checker]: stale if checker now catches the error
    - Pure XFAIL: stale if no longer errors and no reveal mismatch
    """
    stale = set()
    for lineno in skip:
        if lineno in error_markers:
            if lineno in actual_lines:
                stale.add(lineno)
        else:
            has_error = lineno in actual_lines
            has_reveal_mismatch = (
                lineno in expected_rev
                and (lineno not in actual_rev
                     or expected_rev[lineno] != normalize_type(actual_rev[lineno], checker))
            )
            if not has_error and not has_reveal_mismatch:
                stale.add(lineno)
    return stale


def validate_file(filepath, expected, skipped, expected_reveals, error_markers,
                  actual, actual_reveals, checker):
    """Validate a single test file, return list of failure message strings."""
    exp = expected.get(filepath, set())
    act_dict = actual.get(filepath, {})
    act = set(act_dict.keys())
    skip = skipped.get(filepath, set())
    exp_rev = expected_reveals.get(filepath, {})
    act_rev = actual_reveals.get(filepath, {})
    e_markers = error_markers.get(filepath, set())

    relpath = os.path.relpath(filepath)
    failures = []

    # Unexpected errors: actual errors on lines not marked # E: or # XFAIL:
    for line in sorted(act - exp - skip):
        failures.append(f"  UNEXPECTED ERROR: {relpath}:{line}: {act_dict.get(line, '')}")

    # Missing errors: lines marked # E: that didn't error
    for line in sorted(exp - act):
        failures.append(f"  MISSING EXPECTED ERROR: {relpath}:{line}")

    # Stale XFAILs: lines marked # XFAIL that no longer fail
    for line in sorted(find_stale_xfails(skip, e_markers, act, exp_rev, act_rev, checker)):
        failures.append(f"  STALE XFAIL (no longer fails): {relpath}:{line}")

    # Reveal type mismatches
    for lineno, pattern in sorted(exp_rev.items()):
        if lineno in skip:
            continue
        if lineno not in act_rev:
            failures.append(f"  MISSING REVEAL: {relpath}:{lineno} (expected: {pattern})")
        else:
            actual_type = normalize_type(act_rev[lineno], checker)
            if pattern != actual_type:
                failures.append(f"  REVEAL MISMATCH: {relpath}:{lineno}")
                failures.append(f"    expected: {pattern}")
                failures.append(f"    actual: {actual_type}")

    return failures


def run_checker(checker):
    """Run a single type checker and validate results. Returns True on success."""
    print(f"Running {checker} on {TEST_DIR}...")

    expected, skipped, expected_reveals, error_markers = parse_markers(TEST_DIR, checker)
    actual, actual_reveals = CHECKERS[checker](TEST_DIR)

    # Only consider errors in test files (ignore errors in runner and library source)
    abs_test_dir = os.path.abspath(TEST_DIR)
    def is_test_file(f):
        return f.startswith(abs_test_dir) and os.path.basename(f).startswith("test_")
    actual = {f: lines for f, lines in actual.items() if is_test_file(f)}
    actual_reveals = {f: lines for f, lines in actual_reveals.items() if is_test_file(f)}

    # Collect all test files
    all_files = sorted(set(list(expected.keys()) + list(actual.keys())
                           + list(expected_reveals.keys())))

    failures = []
    for filepath in all_files:
        failures.extend(validate_file(
            filepath, expected, skipped, expected_reveals, error_markers,
            actual, actual_reveals, checker))

    if not failures:
        print(f"OK - {checker}: all type errors match expectations")
        return True
    else:
        for msg in failures:
            print(msg)
        print(f"FAIL - {checker}: type error mismatches found")
        return False


def main():
    valid = {*CHECKERS, "coverage", "all"}
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] not in valid):
        print(f"Usage: {sys.argv[0]} [{','.join(CHECKERS)},coverage,all]")
        sys.exit(2)

    command = sys.argv[1] if len(sys.argv) == 2 else "all"

    if command == "coverage":
        check_coverage(TEST_DIR)
        return

    checkers = list(CHECKERS) if command == "all" else [command]
    failed = [c for c in checkers if not run_checker(c)]
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
