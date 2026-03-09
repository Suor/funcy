# `.pyih` → `.pyi` Stub Generation

Funcy uses `.pyih` (pyi higher) source files to generate `.pyi` type stubs. This avoids the cross-product explosion of overloads when typing the extended function protocol (7 variants) combined with collection type preservation.

## Quick Start

```bash
# Edit the .pyih source
vim funcy/seqs.pyih

# Regenerate all .pyi files
python translate_pyih.py

# Verify types
python type_tests/run.py mypy
python type_tests/run.py pyright
python type_tests/run.py ty
```

## Which modules use `.pyih`

| Module | `.pyih` source | Generated `.pyi` |
|--------|---------------|-----------------|
| seqs | `funcy/seqs.pyih` | `funcy/seqs.pyi` |
| colls | `funcy/colls.pyih` | `funcy/colls.pyi` |
| funcs | `funcy/funcs.pyih` | `funcy/funcs.pyi` |
| funcmakers | `funcy/funcmakers.pyih` | `funcy/funcmakers.pyi` |

Other modules (`flow`, `calc`, `debug`, etc.) have hand-written `.pyi` stubs.

## `.pyih` Syntax

`.pyih` files are valid Python 3.12+ syntax. They use three custom constructs that `translate_pyih.py` expands:

### `XFunc[[A], B]` — Extended mapper

Used for function parameters that accept the extended function protocol (Callable, None, Set, Regex, int, slice, Mapping) and transform values from type `A` to type `B`.

```python
def map(f: XFunc[[A], B], seq: Iterable[A]) -> Iterator[B]: ...
```

Expands to 7 overloads:

| Variant | `f` type | `A` becomes | `B` becomes |
|---------|----------|-------------|-------------|
| Callable | `Callable[[A], B]` | A | B |
| None | `None` | A | A (identity) |
| Set | `AbstractSet[A]` | A | `bool` |
| Regex | `str \| bytes \| re.Pattern[str]` | `Any` | `_ReResult \| None` |
| int | `int` | `Sequence[_T]` | `_T` (itemgetter) |
| slice | `slice` | `Sequence[_T]` | `Sequence[_T]` |
| Mapping | `Mapping[A, B]` | A | B (lookup) |

### `XPred[A]` — Extended predicate

Used for function parameters that accept the extended function protocol as a predicate. The element type `A` is preserved (predicates filter, not transform).

```python
def filter(pred: XPred[A], seq: Iterable[A]) -> Iterator[A]: ...
```

Expands to 7 overloads that constrain the input type:

| Variant | `pred` type | `A` constraint |
|---------|------------|----------------|
| Callable | `Callable[[A], Any]` | A |
| None | `None` | A (truthiness) |
| Set | `AbstractSet[A]` | A (membership) |
| Regex | `str \| bytes \| re.Pattern[str]` | `str` |
| int | `int` | `Sequence[Any]` |
| slice | `slice` | `Sequence[Any]` |
| Mapping | `Mapping[A, Any]` | A (key existence) |

### `[C: (list, set, ...)]` — Collection type expansion

PEP 695 type parameter syntax. Generates one overload per concrete type, substituting `C` throughout. Combines with XFunc/XPred for quadratic expansion.

```python
def walk[C: (list, set, frozenset)](f: XFunc[[A], B], coll: C[A]) -> C[B]: ...
```

Generates `3 * 7 = 21` overloads (3 collection types x 7 XFunc variants).

### `# xfunc_skip: Callable` — Skip variants

Placed before a function def. Skips named variant(s) during expansion. Useful when the Callable case needs a separate hand-written overload with more specific types.

```python
# xfunc_skip: Callable
def compose(f: XFunc[[_T], _V]) -> Callable[[_T], _V]: ...
# Callable case handled separately with typed multi-arg overloads:
def compose(__f: Callable[..., _R], *rest: _XFunc) -> Callable[..., _R]: ...
```

### Passthrough

Functions without `XFunc`, `XPred`, or collection type parameters pass through verbatim:

```python
def take(n: int, seq: Iterable[_T]) -> list[_T]: ...  # copied as-is
```

## Rules

1. **Never edit `.pyi` files directly** if a `.pyih` counterpart exists — a repo hook blocks this.
2. After editing a `.pyih`, always run `python translate_pyih.py` to regenerate.
3. Run all three type checkers: `python type_tests/run.py mypy && python type_tests/run.py ty && python type_tests/run.py pyright`
4. Run `python -m mypy.stubtest funcy.<module> --allowlist stubtest_allowlist.txt` to verify stubs match runtime.
