from typing import Any, assert_type
from collections.abc import Callable
from funcy import isa, is_mapping, is_set, is_seq, is_list, is_tuple, is_seqcoll, is_seqcont, iterable, is_iter

# -- isa returns a callable predicate --
assert_type(isa(int), Callable[[Any], bool])
assert_type(isa(int, str), Callable[[Any], bool])

# -- Module-level predicates are callable --
assert_type(is_mapping, Callable[[Any], bool])
assert_type(is_set, Callable[[Any], bool])
assert_type(is_seq, Callable[[Any], bool])
assert_type(is_list, Callable[[Any], bool])
assert_type(is_tuple, Callable[[Any], bool])
assert_type(is_seqcoll, Callable[[Any], bool])
assert_type(is_seqcont, Callable[[Any], bool])
assert_type(iterable, Callable[[Any], bool])
assert_type(is_iter, Callable[[Any], bool])

# -- Predicates return bool --
assert_type(is_mapping({}), bool)
assert_type(is_list([1, 2]), bool)
assert_type(isa(int)(42), bool)

# -- Should be errors --
isa(42)  # E: not a type
