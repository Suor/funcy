from typing import Any, assert_type
from collections.abc import Callable, Iterator
from funcy import (
    identity, constantly, caller,
    rpartial, func_partial,
    curry, rcurry, autocurry,
    iffy, compose, rcompose, complement, juxt, ljuxt,
)

# -- identity preserves type --
assert_type(identity(42), int)  # XFAIL[ty]: Literal narrowing
assert_type(identity("hello"), str)  # XFAIL[ty]: Literal narrowing

# -- constantly returns a function that always returns x --
f = constantly(42)
assert_type(f, Callable[..., int])  # XFAIL[ty]: Literal narrowing
assert_type(f("anything"), int)  # XFAIL[ty]: Literal narrowing

# -- rpartial / func_partial preserve return type --
def add(a: int, b: int) -> int: return a + b
assert_type(rpartial(add, 1), Callable[..., int])
assert_type(func_partial(add, 1), Callable[..., int])

# -- autocurry preserves function signature --
reveal_type(autocurry(add))  # R: (a: int, b: int) -> int

# -- iffy --
assert_type(iffy(bool, str), Callable[..., Any])

# -- compose / rcompose --
assert_type(compose(str, abs), Callable[..., Any])
assert_type(rcompose(abs, str), Callable[..., Any])

# -- complement --
assert_type(complement(bool), Callable[..., bool])

# -- juxt / ljuxt --
assert_type(juxt(str, int), Callable[..., Iterator[Any]])
assert_type(ljuxt(str, int), Callable[..., list[Any]])
