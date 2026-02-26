from collections.abc import Iterator, Sequence
from funcy import iterate, repeatedly
from typing import Callable, assert_type, reveal_type

nums = [1, 2, 3, 4, 5]
strs = ["a", "b", "c"]
int_pairs: list[tuple[int, int]] = [(1, 2), (3, 4)]

# -- Generators --
def make_int() -> int:
    return 1
assert_type(repeatedly(make_int), Iterator[int])
assert_type(repeatedly(make_int, 5), Iterator[int])

def double(x: int) -> int:
    return x * 2
# reveal_type(double)
assert_type(iterate(double, 1), Iterator[int])

# NOTE: ty doesn't understand this
double2: Callable[[int], int] = lambda x: x * 2
# reveal_type(double2)
assert_type(iterate(double2, 1), Iterator[int])
