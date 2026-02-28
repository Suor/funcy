import re
from collections.abc import Iterator, Sequence
from typing import reveal_type
from funcy import (
    identity, constantly, caller,
    rpartial, func_partial,
    curry, rcurry, autocurry,
    iffy, compose, rcompose, complement, juxt, ljuxt,
)

# -- identity preserves type --
x: int = 42
s: str = "hello"
reveal_type(identity(x))  # R: int  # XFAIL[ty]: Literal narrowing
reveal_type(identity(s))  # R: str  # XFAIL[ty]: Literal narrowing

# -- constantly returns a function that always returns x --
f = constantly(x)
reveal_type(f)  # R: (...) -> int  # XFAIL[ty]: Literal narrowing
reveal_type(f("anything"))  # R: int  # XFAIL[ty]: Literal narrowing

# -- caller --
def add_int(a: int, b: int) -> int: return a + b
reveal_type(caller(1, 2)(add_int))  # R: int

# -- rpartial / func_partial preserve return type --
def add(a: int, b: int) -> int: return a + b
reveal_type(rpartial(add, 1))  # R: (...) -> int
reveal_type(func_partial(add, 1))  # R: (...) -> int

# -- curry / rcurry --
reveal_type(curry(add))  # R: (...) -> int
reveal_type(rcurry(add))  # R: (...) -> int

# -- autocurry preserves function signature --
reveal_type(autocurry(add))  # R: (a: int, b: int) -> int

# -- iffy: Callable action preserves return type --
def int_to_str(x: int) -> str: return str(x)
reveal_type(iffy(bool, int_to_str))  # R: (int) -> str
reveal_type(iffy(int_to_str))  # R: (...) -> str

# -- iffy: XFunc variants for one-arg form --
reveal_type(iffy(None))  # R: (_T) -> _T
lookup: dict[int, str] = {1: "a"}
reveal_type(iffy(lookup))  # R: (int) -> str
int_set: frozenset[int] = frozenset({1, 2, 3})
reveal_type(iffy(int_set))  # R: (int) -> bool

# -- iffy: XPred variants for two-arg form --
reveal_type(iffy(None, int_to_str))  # R: (int) -> str
reveal_type(iffy(int_set, int_to_str))  # R: (int) -> str

# -- compose / rcompose: Callable --
reveal_type(compose(int_to_str, abs))  # R: (...) -> str
reveal_type(rcompose(abs, int_to_str))  # R: (...) -> str

# -- compose: XFunc variants for single-arg form --
reveal_type(compose(None))  # R: (_T) -> _T
reveal_type(compose(lookup))  # R: (int) -> str
reveal_type(compose(int_set))  # R: (int) -> bool
reveal_type(compose(0))  # R: (Sequence[_T]) -> _T

# -- complement: Callable --
reveal_type(complement(bool))  # R: (...) -> bool

# -- complement: XPred variants --
reveal_type(complement(int_set))  # R: (int) -> bool
reveal_type(complement(lookup))   # R: (int) -> bool
reveal_type(complement(r"\d+"))   # R: (str) -> bool
reveal_type(complement(0))        # R: (Sequence[Any]) -> bool

# -- juxt / ljuxt --
def to_bytes(x: int) -> bytes: return str(x).encode()
reveal_type(juxt(int_to_str, to_bytes))  # R: (...) -> Iterator[str | bytes]
reveal_type(ljuxt(int_to_str, to_bytes))  # R: (...) -> list[str | bytes]

# -- juxt / ljuxt: _Func fallback --
reveal_type(juxt(int_to_str, None))  # R: (...) -> Iterator[Any]
reveal_type(ljuxt(int_to_str, None))  # R: (...) -> list[Any]

# -- Should be errors --
iffy(3.14)  # E: float is not a valid action
iffy(3.14, int_to_str)  # E: float is not a valid pred
compose(3.14)  # E: float is not a valid function
complement(3.14)  # E: float is not a valid pred
