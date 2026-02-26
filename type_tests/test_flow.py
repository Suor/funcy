from typing import Any, NoReturn, assert_type
from collections.abc import Callable
from funcy import (
    raiser, ignore, silent, retry, fallback,
    limit_error_rate, ErrorRateExceeded, throttle,
    collecting, joining,
    once, once_per, once_per_args, wrap_with,
)

# -- raiser returns a function that raises --
assert_type(raiser(ValueError), Callable[..., NoReturn])
assert_type(raiser("error message"), Callable[..., NoReturn])

# -- ignore / silent preserve function signature --
@ignore(ValueError)
def may_fail(x: int) -> int: return x
reveal_type(may_fail)  # R: (x: int) -> int

@silent
def always_safe(x: int) -> int: return x
reveal_type(always_safe)  # R: (x: int) -> int

# -- retry preserves function signature --
@retry(3, errors=ValueError)
def retried() -> str: return "ok"
reveal_type(retried)  # R: () -> str

# -- throttle preserves function signature --
@throttle(1.0)
def throttled() -> int: return 1
reveal_type(throttled)  # R: () -> int

# -- collecting --
@collecting
def gen() -> Any:
    yield 1
reveal_type(gen)  # R: () ->

# -- once / once_per --
@once
def init() -> None: pass
reveal_type(init)  # R: () -> None

@once_per("x")
def init_per(x: int) -> None: pass
reveal_type(init_per)  # R: (x: int) -> None

@once_per_args
def init_all(x: int) -> None: pass
reveal_type(init_all)  # R: (x: int) -> None

# -- ErrorRateExceeded --
assert_type(ErrorRateExceeded(), ErrorRateExceeded)

# -- fallback --
assert_type(fallback(lambda: 1, lambda: 2), Any)

# -- Should be errors --
raiser(42)  # E: wrong arg type
