import re
from typing import reveal_type
from funcy.funcmakers import make_func, make_pred

def to_str(x: object) -> str: return str(x)
def gt_zero(x: int) -> bool: return x > 0

nums: list[int] = [1, 2, 3]

# === make_func ===

# -- Callable: preserves return type --
reveal_type(make_func(to_str))     # R: (...) -> str
reveal_type(make_func(gt_zero))    # R: (...) -> bool
reveal_type(make_func(int))        # R: (...) -> int

# -- None: identity function --
reveal_type(make_func(None))       # R: (_T) -> _T

# -- int: itemgetter on Sequences --
f_int = make_func(0)
reveal_type(f_int)           # R: (Sequence[_T]) -> _T
reveal_type(f_int(nums))     # R: int
strs: tuple[str, str] = ("a", "b")
reveal_type(f_int(strs))          # R: str  # XFAIL[ty]: Literal inference

# -- slice: itemgetter on Sequences --
f_slice = make_func(slice(1, 3))
reveal_type(f_slice)         # R: (Sequence[_T]) -> Sequence[_T]
reveal_type(f_slice(nums))   # R: Sequence[int]

# -- str/bytes/Pattern: re_finder --
reveal_type(make_func(r"\d+"))              # R: (str) -> str | tuple[str, ...] | dict[str, str] | None
reveal_type(make_func(b"\\d+"))             # R: (str) -> str | tuple[str, ...] | dict[str, str] | None
reveal_type(make_func(re.compile(r"\d+")))  # R: (str) -> str | tuple[str, ...] | dict[str, str] | None

# -- Mapping: lookup function with typed key/value --
d: dict[str, int] = {"a": 1, "b": 2}
reveal_type(make_func(d))  # R: (str) -> int

# -- Set: membership test --
s: frozenset[int] = frozenset({1, 2, 3})
reveal_type(make_func(s))  # R: (int) -> bool

# === make_pred ===

# -- Callable: preserves return type --
reveal_type(make_pred(gt_zero))        # R: (...) -> bool
reveal_type(make_pred(str.startswith)) # R: (...) -> bool

# -- None: becomes bool --
reveal_type(make_pred(None))  # R: (Any) -> bool

# -- int: itemgetter (used as predicate) --
f_pred_int = make_pred(0)
reveal_type(f_pred_int)        # R: (Sequence[_T]) -> _T
reveal_type(f_pred_int(nums))  # R: int

# -- slice: itemgetter (used as predicate) --
f_pred_slice = make_pred(slice(0, 2))
reveal_type(f_pred_slice)        # R: (Sequence[_T]) -> Sequence[_T]
reveal_type(f_pred_slice(nums))  # R: Sequence[int]

# -- str/bytes/Pattern: re_tester (returns bool) --
reveal_type(make_pred(r"\d+"))              # R: (str) -> bool
reveal_type(make_pred(b"\\d+"))             # R: (str) -> bool
reveal_type(make_pred(re.compile(r"\d+")))  # R: (str) -> bool

# -- Mapping: lookup (used as predicate) --
reveal_type(make_pred({"a": 1}))  # R: (str) -> int  # XFAIL[ty]: can't infer Mapping TypeVars

# -- Set: membership test --
int_set: set[int] = {1, 2, 3}
reveal_type(make_pred(int_set))  # R: (int) -> bool

# === Errors: invalid types ===
make_func(3.14)   # E: wrong argument type
make_func([1, 2]) # E: wrong argument type
make_pred(3.14)   # E: wrong argument type
make_pred([1, 2]) # E: wrong argument type
