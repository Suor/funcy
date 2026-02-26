from typing import Any, assert_type
from collections.abc import Callable
from funcy import memoize, cache, make_lookuper, silent_lookuper

# -- memoize as decorator (no args) --
@memoize
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)
reveal_type(fib)  # R: (n: int) -> int

# -- memoize with key_func --
@memoize(key_func=lambda x: x % 10)
def mod_cache(x: int) -> str:
    return str(x)
reveal_type(mod_cache)  # R: (x: int) -> str

# -- cache --
@cache(60)
def cached_fn(x: int) -> str:
    return str(x)
reveal_type(cached_fn)  # R: (x: int) -> str

# FIX: it's possible to detect type, i.e. dict[str, int] -> Callable[[str], int]
#      or int | None for silent_lookuper. Should check with reveal_type
# -- make_lookuper --
@make_lookuper
def my_lookup() -> dict[str, int]:
    return {"a": 1, "b": 2}
assert_type(my_lookup, Callable[..., Any])  # XFAIL[ty]: wrapper transforms signature

# -- silent_lookuper --
@silent_lookuper
def my_silent() -> dict[str, int]:
    return {"a": 1, "b": 2}
assert_type(my_silent, Callable[..., Any])  # XFAIL[ty]: wrapper transforms signature
