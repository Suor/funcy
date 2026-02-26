from typing import Any
from funcy import (
    raiser, ignore, silent, reraise, retry, fallback,
    limit_error_rate, ErrorRateExceeded, throttle,
    post_processing, collecting, joining,
    once, once_per, once_per_args, wrap_with,
)

# -- raiser returns a function that raises --
reveal_type(raiser(ValueError))  # R: -> Never
reveal_type(raiser("error message"))  # R: -> Never

# -- ignore / silent preserve function signature --
@ignore(ValueError)
def may_fail(x: int) -> int: return x
reveal_type(may_fail)  # R: (x: int) -> int

@silent
def always_safe(x: int) -> int: return x
reveal_type(always_safe)  # R: (x: int) -> int

# -- reraise --
reveal_type(reraise(ValueError, RuntimeError))  # R: AbstractContextManager[None

# -- retry preserves function signature --
@retry(3, errors=ValueError)
def retried() -> str: return "ok"
reveal_type(retried)  # R: () -> str

# -- throttle preserves function signature --
@throttle(1.0)
def throttled() -> int: return 1
reveal_type(throttled)  # R: () -> int

# -- limit_error_rate preserves function signature --
@limit_error_rate(10, 60)
def rate_limited(x: int) -> str: return str(x)
reveal_type(rate_limited)  # R: (x: int) -> str

# -- post_processing preserves function signature --
@post_processing(list)
def gen_list() -> Any:
    yield 1
reveal_type(gen_list)  # R: () ->

# -- collecting --
@collecting
def gen() -> Any:
    yield 1
reveal_type(gen)  # R: () ->

# -- joining preserves function signature --
@joining(", ")
def gen_strs() -> Any:
    yield "a"
reveal_type(gen_strs)  # R: () ->

# -- wrap_with preserves function signature --
import threading
@wrap_with(threading.Lock())
def locked(x: int) -> str: return str(x)
reveal_type(locked)  # R: (x: int) -> str

# -- once / once_per / once_per_args --
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
reveal_type(ErrorRateExceeded())  # R: ErrorRateExceeded

# -- fallback --
reveal_type(fallback(lambda: 1, lambda: 2))  # R: Any

# -- Should be errors --
raiser(42)  # E: wrong arg type
