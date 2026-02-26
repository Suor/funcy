from typing import assert_type
from collections.abc import Callable, Iterator
from funcy import tap, log_calls, print_calls, log_errors, print_errors
from funcy import log_durations, print_durations
from funcy import log_iter_durations, print_iter_durations

# -- tap preserves type --
assert_type(tap(42), int)  # XFAIL[ty]: Unknown TypeVars
assert_type(tap("hello"), str)  # XFAIL[ty]: Unknown TypeVars
assert_type(tap(42, "label"), int)  # XFAIL[ty]: Unknown TypeVars

# -- log_calls / print_calls preserve function signature --
@log_calls(print)
def logged(x: int) -> str: return str(x)
reveal_type(logged)  # R: (x: int) -> str

@print_calls
def printed(x: int) -> str: return str(x)
reveal_type(printed)  # R: (x: int) -> str

# -- log_errors as decorator preserves function signature --
@log_errors(print)
def risky(x: int) -> str: return str(x)
reveal_type(risky)  # R: (x: int) -> str

# -- log_errors is a context manager --
with log_errors(print) as ctx:
    assert_type(ctx, log_errors)

# -- print_errors is a log_errors instance --
assert_type(print_errors, log_errors)

# -- log_durations as decorator preserves function signature --
@log_durations(print)
def timed(x: int) -> str: return str(x)
reveal_type(timed)  # R: (x: int) -> str

# -- log_durations is a context manager --
with log_durations(print) as dur_ctx:
    assert_type(dur_ctx, log_durations)

# -- print_durations is a log_durations instance --
assert_type(print_durations, log_durations)

# -- iter durations preserves type --
nums = [1, 2, 3]
assert_type(log_iter_durations(nums, print), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(print_iter_durations(nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
