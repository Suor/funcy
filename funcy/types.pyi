from collections.abc import Callable
from typing import Any

__all__ = ('isa', 'is_mapping', 'is_set', 'is_seq', 'is_list', 'is_tuple',
           'is_seqcoll', 'is_seqcont',
           'iterable', 'is_iter')

def isa(*types: type) -> Callable[[Any], bool]: ...

is_mapping: Callable[[Any], bool]
is_set: Callable[[Any], bool]
is_seq: Callable[[Any], bool]
is_list: Callable[[Any], bool]
is_tuple: Callable[[Any], bool]
is_seqcoll: Callable[[Any], bool]
is_seqcont: Callable[[Any], bool]
iterable: Callable[[Any], bool]
is_iter: Callable[[Any], bool]
