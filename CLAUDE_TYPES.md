# Type Stubs

**Goal**: Catch type errors and provide useful types on exits, but don't break or annoy users. Types should be precise where possible but never reject valid code.

Type annotations live in `.pyi` stub files, not inline, to keep runtime code clean. The `py.typed` marker (PEP 561) is present.

**Key patterns in stubs**:
- Be as specific as possible with types: use `Callable[[_T], Any]` not `Callable[..., Any]` when a function takes one element arg; use `Callable[[_T, _T], _T]` for reducers, etc.
- Use `TypeVar _T` for type preservation (`empty(coll: _T) -> _T`) instead of redundant overloads
- Use `Callable[[_K], _K2]` for functions that transform types (e.g. `walk_keys`)
- EMPTY sentinel: functions like `all(pred, seq=EMPTY)` that shift args use `@overload`, listed in `stubtest_allowlist.txt`
- Regex return types: `_ReResult = str | tuple[str, ...] | dict[str, str]` — can't narrow by pattern without a mypy plugin (pyright and ty have no plugin systems)

## `.pyih` -> `.pyi` Code Generation

Four modules use `.pyih` source files that are translated to `.pyi` stubs: `seqs`, `colls`, `funcmakers`, `funcs`. The translator is `translate_pyih.py`. **Never directly edit a `.pyi` that has a `.pyih` counterpart** — a repo hook blocks this.

**Workflow**: edit the `.pyih` file, then run `python translate_pyih.py` to regenerate all `.pyi` files.

For full `.pyih` syntax documentation (XFunc, XPred, collection expansion, xfunc_skip, etc.), see [PYIH.md](PYIH.md).

## Type Tests

Type tests live in `type_tests/` at repo root. The runner (`type_tests/run.py`) validates against three checkers (mypy, pyright, ty).

Test file markers:
- No marker: line must type-check cleanly on all checkers
- `# E: <reason>`: line must produce a type error (all checkers must error)
- `# XFAIL: <reason>`: line currently errors but shouldn't ideally (aspirational, all checkers)
- `# XFAIL[ty]: <reason>`: known failure for a specific checker (ty has many TypeVar inference bugs)
- `# E: reason  # XFAIL[ty]: reason`: expected error, but ty doesn't catch it (mypy/pyright must error, ty is excused)
- `# R: type  # XFAIL[ty]: reason`: expected reveal type, but ty gets it wrong (skips reveal check for ty)

**Testing philosophy**: We care about our stubs working correctly, not about what checkers can infer. When testing with abstract types (Mapping, Sequence, Iterable), use real implementations — custom subclasses — not concrete types cast to abstract (e.g. `m: Mapping = d` where `d` is a dict). Checkers see through such casts and resolve to the concrete type, making the test misleading. A real `class MyMapping(Mapping[K, V])` forces the checker to use the abstract overload.

`stubtest` verifies stubs match runtime signatures. Functions with EMPTY sentinel patterns go in `stubtest_allowlist.txt`.
