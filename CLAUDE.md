# CLAUDE.md

## Project Overview

Funcy is a Python library of functional programming tools. It has zero runtime dependencies and supports Python 3.4+ and PyPy3.

## Commands

```bash
# Run all tests
pytest -W error

# Run a single test file
pytest tests/test_seqs.py

# Run a single test
pytest tests/test_seqs.py::test_take

# Lint
flake8 funcy
flake8 --select=F,E5,W tests

# Type checking tests (validates stubs against # E: markers)
python type_tests/run.py          # run all three checkers
python type_tests/run.py mypy     # run a single checker
python type_tests/run.py pyright
python type_tests/run.py ty
python type_tests/run.py coverage # verify all public names have type tests

# Verify stubs match runtime signatures
tox -e stubtest

# Build docs
cd docs && sphinx-build -b html -W . _build/html

# Tox (multi-version testing)
tox -e py313
tox -e lint
tox -e docs
tox -e typetest
tox -e stubtest
```

## Architecture

All public API is re-exported through `funcy/__init__.py` via wildcard imports. Each module defines `__all__`.

### Module Map

- **seqs.py** - Sequence/iterator operations (`take`, `drop`, `first`, `map`, `filter`, `partition`, `chunks`, `group_by`, `distinct`, etc.)
- **colls.py** - Collection manipulation (`merge`, `walk`, `select`, `get_in`, `set_in`, `split_keys`, etc.)
- **funcs.py** - Function composition (`identity`, `partial`, `curry`, `compose`, `complement`, `juxt`)
- **flow.py** - Control flow (`retry`, `throttle`, `ignore`, `silent`, `once`, `limit_error_rate`)
- **calc.py** - Caching/memoization (`memoize`, `cache`, `make_lookuper`)
- **decorators.py** - Decorator utilities (`@decorator`, `@wraps`, `ContextDecorator`)
- **debug.py** - Debugging helpers (`tap`, `log_calls`, `log_errors`, `print_durations`)
- **objects.py** - Object utilities (`cached_property`, `monkey`, `LazyObject`)
- **strings.py** - Regex wrappers (`re_find`, `re_all`, `re_test`)
- **types.py** - Type predicates (`isa`, `is_mapping`, `is_seq`)
- **tree.py** - Tree traversal (`tree_leaves`, `tree_nodes`)
- **funcolls.py** - Functional collection predicates (`all_fn`, `any_fn`, `none_fn`, `some_fn`)
- **funcmakers.py** - Extended function semantics (internal, not in `__all__` of `__init__`)
- **_inspect.py** - Function introspection helpers (internal)

### Key Design Patterns

- **Lazy by default**: Most sequence operations return iterators. Eager variants are prefixed with `l` (e.g., `lmap`, `lfilter`, `lcat`).
- **Extended function protocol** (`funcmakers.py`): Many functions accept not just callables but also regex strings, ints/slices (as `itemgetter`), dicts (as lookup), and sets (as membership test). This is handled by `make_func`/`make_pred`.
- **Type preservation**: Collection operations like `walk` preserve the input type (dict stays dict, set stays set).

### Type Stubs

For type stub details (patterns, `.pyih` code generation, type tests), see [CLAUDE_TYPES.md](CLAUDE_TYPES.md). For extended `.pyih` syntax reference, see [PYIH.md](PYIH.md).

## Shell Rules

- Never use `cat <<EOF` / heredoc in Bash. Use the Write tool to create files instead, even for temporary ones.

## Code Style

- Max line length: 100
- Flake8 with many relaxed rules (see `tox.ini` `[flake8]` section)
- Tests use the `whatever` library for concise lambda-like expressions (`_ + 1`)
