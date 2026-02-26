from typing import Any, assert_type
from collections.abc import Callable
from funcy import all_fn, any_fn, none_fn, one_fn, some_fn

# -- all_fn / any_fn / none_fn / one_fn return predicates --
is_positive = lambda x: x > 0
is_even = lambda x: x % 2 == 0

assert_type(all_fn(is_positive, is_even), Callable[..., bool])
assert_type(any_fn(is_positive, is_even), Callable[..., bool])
assert_type(none_fn(is_positive, is_even), Callable[..., bool])
assert_type(one_fn(is_positive, is_even), Callable[..., bool])

# -- some_fn returns the first truthy result --
assert_type(some_fn(is_positive, is_even), Callable[..., Any])

# -- Extended function protocol --
assert_type(all_fn(r"\d+", str.isdigit), Callable[..., bool])
