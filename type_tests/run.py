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
    for filepath in sorted(glob.glob(os.path.join(test_dir, "test_*.py"))):
        exp = set()
        skip = set()
        rev = {}
        with open(filepath) as f:
            for lineno, line in enumerate(f, 1):
                if "# E:" in line:
                    exp.add(lineno)
                elif "# XFAIL:" in line:
                    skip.add(lineno)
                else:
                    # Check for checker-specific XFAIL: # XFAIL[ty]:
                    m = re.search(r"# XFAIL\[([^\]]+)\]:", line)
                    if m and checker in m.group(1).split(","):
                        skip.add(lineno)
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
    return expected, skipped, reveals


def normalize_type(revealed, checker):
    """Normalize a revealed type string for comparison."""
    s = revealed
    if checker == "mypy":
        # mypy uses qualified names: builtins.int -> int, builtins.str -> str
        s = re.sub(r'builtins\.', '', s)
        # Remove module prefixes for common types
        s = re.sub(r'\b[a-z_][a-z_0-9]*\.([A-Z])', r'\1', s)
        # mypy omits -> None in revealed types, add it back for consistency
        if s.startswith("def ") and "->" not in s:
            s = s + " -> None"
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
    errors = {}  # {filepath: set of line numbers}
    reveals = {}  # {filepath: {lineno: revealed_type}}
    try:
        import json
        data = json.loads(result.stdout)
        for diag in data.get("generalDiagnostics", []):
            filepath = os.path.abspath(diag["file"])
            lineno = diag["range"]["start"]["line"] + 1  # pyright uses 0-based
            if diag.get("severity") == "error":
                errors.setdefault(filepath, set()).add(lineno)
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
    errors = {}  # {filepath: set of line numbers}
    reveals = {}  # {filepath: {lineno: revealed_type}}
    for line in result.stdout.splitlines():
        # mypy error format: file.py:lineno: error: message
        match = re.match(r"(.+?):(\d+):\s*error:", line)
        if match:
            filepath = os.path.abspath(match.group(1))
            lineno = int(match.group(2))
            errors.setdefault(filepath, set()).add(lineno)
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
    errors = {}  # {filepath: set of line numbers}
    reveals = {}  # {filepath: {lineno: revealed_type}}
    output = (result.stdout + result.stderr).splitlines()
    in_error = False
    in_reveal = False
    reveal_file = None
    reveal_line = 0
    for line in output:
        # ty format:
        #   error[rule-name]: Message text
        #     --> file.py:lineno:col
        #   info[revealed-type]: Revealed type
        #     --> file.py:lineno:col
        #        | ^^^ `type_here`
        if re.match(r"\s*error\[", line):
            in_error = True
            in_reveal = False
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
                errors.setdefault(filepath, set()).add(lineno)
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

# Names that are intentionally not tested (internal helpers, re-exports, etc.)
COVERAGE_SKIP = {"SkipMemory", "Call"}


def check_coverage(test_dir):
    """Check that all public names from stubs are imported in type tests."""
    import ast

    # Collect all public names from .pyi stubs
    stub_dir = os.path.join(os.path.dirname(test_dir), "funcy")
    stub_names = set()
    for filepath in sorted(glob.glob(os.path.join(stub_dir, "*.pyi"))):
        mod = os.path.basename(filepath).replace(".pyi", "")
        if mod == "__init__":
            continue
        with open(filepath) as f:
            tree = ast.parse(f.read())
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not node.name.startswith("_"):
                    stub_names.add(node.name)
            elif isinstance(node, ast.ClassDef):
                if not node.name.startswith("_"):
                    stub_names.add(node.name)
            elif isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and not t.id.startswith("_"):
                        stub_names.add(t.id)

    # Collect all names imported from funcy in test files
    tested = set()
    for filepath in sorted(glob.glob(os.path.join(test_dir, "test_*.py"))):
        with open(filepath) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and "funcy" in node.module:
                for alias in node.names:
                    tested.add(alias.name)

    missing = stub_names - tested - COVERAGE_SKIP
    if missing:
        print("FAIL - untested public stub names:")
        for name in sorted(missing):
            print(f"  {name}")
        sys.exit(1)
    else:
        print(f"OK - all {len(stub_names)} public stub names are covered "
              f"({len(COVERAGE_SKIP)} skipped)")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {*CHECKERS, "coverage"}:
        print(f"Usage: {sys.argv[0]} {{{','.join(CHECKERS)},coverage}}")
        sys.exit(2)

    if sys.argv[1] == "coverage":
        check_coverage(TEST_DIR)
        return

    checker = sys.argv[1]
    print(f"Running {checker} on {TEST_DIR}...")

    expected, skipped, expected_reveals = parse_markers(TEST_DIR, checker)
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

    ok = True
    for filepath in all_files:
        exp = expected.get(filepath, set())
        act = actual.get(filepath, set())
        skip = skipped.get(filepath, set())

        # Unexpected errors: actual errors on lines not marked # E: or # XFAIL:
        unexpected = act - exp - skip
        # Missing errors: lines marked # E: that didn't error
        missing = exp - act
        # Stale XFAILs: lines marked # XFAIL that no longer fail
        # An XFAIL is stale if it doesn't error AND doesn't have a mismatching reveal
        exp_rev = expected_reveals.get(filepath, {})
        act_rev = actual_reveals.get(filepath, {})
        reveal_mismatches = set()
        for lineno, pattern in exp_rev.items():
            if lineno not in act_rev:
                reveal_mismatches.add(lineno)
            else:
                actual_type = normalize_type(act_rev[lineno], checker)
                if pattern not in actual_type:
                    reveal_mismatches.add(lineno)
        stale = skip - act - reveal_mismatches

        relpath = os.path.relpath(filepath)
        if unexpected:
            ok = False
            for line in sorted(unexpected):
                print(f"  UNEXPECTED ERROR: {relpath}:{line}")
        if missing:
            ok = False
            for line in sorted(missing):
                print(f"  MISSING EXPECTED ERROR: {relpath}:{line}")
        if stale:
            ok = False
            for line in sorted(stale):
                print(f"  STALE XFAIL (no longer fails): {relpath}:{line}")

        # Check reveal_type matches
        for lineno, pattern in sorted(exp_rev.items()):
            if lineno in skip:
                continue
            if lineno not in act_rev:
                ok = False
                print(f"  MISSING REVEAL: {relpath}:{lineno} (expected: {pattern})")
            else:
                actual_type = normalize_type(act_rev[lineno], checker)
                if pattern not in actual_type:
                    ok = False
                    print(f"  REVEAL MISMATCH: {relpath}:{lineno}")
                    print(f"    expected: {pattern}")
                    print(f"    actual: {actual_type}")

    if ok:
        print(f"OK - {checker}: all type errors match expectations")
    else:
        print(f"FAIL - {checker}: type error mismatches found")
        sys.exit(1)


if __name__ == "__main__":
    main()
