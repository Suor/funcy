import re
from typing import Any, assert_type
from collections.abc import Iterator, Sequence
from funcy import (
    take, drop, first, second, nth, last, rest, butlast, ilen,
    repeatedly, iterate,
    lmap, lfilter, remove, lremove, lkeep, without, lwithout,
    concat, lconcat, cat, lcat, flatten, lflatten, mapcat, lmapcat,
    interleave, interpose, distinct, ldistinct,
    split, lsplit, split_at, lsplit_at, split_by, lsplit_by,
    group_by, group_by_keys, group_values, count_by, count_reps,
    partition, lpartition, chunks, lchunks, partition_by, lpartition_by,
    with_prev, with_next, pairwise, lzip,
    reductions, lreductions, sums, lsums,
)
from funcy.seqs import map, filter, keep, takewhile, dropwhile  # shadow builtins

_ReResult = str | tuple[str, ...] | dict[str, str]

nums: list[int] = [1, 2, 3, 4, 5]
strs: list[str] = ["a", "b", "c"]
int_pairs: list[tuple[int, int]] = [(1, 2), (3, 4)]

# -- Generators --
def make_int() -> int: return 1
def double_int(x: int) -> int: return x * 2
assert_type(repeatedly(make_int), Iterator[int])
assert_type(repeatedly(make_int, 5), Iterator[int])
assert_type(iterate(double_int, 1), Iterator[int])

# -- Slicing --
assert_type(take(3, nums), list[int])
assert_type(drop(1, nums), Iterator[int])
assert_type(first(nums), int | None)
assert_type(second(nums), int | None)
assert_type(nth(0, nums), int | None)
assert_type(last(nums), int | None)
assert_type(rest(nums), Iterator[int])
assert_type(butlast(nums), Iterator[int])
assert_type(ilen(nums), int)

### lmap: comprehensive extended function protocol tests ###

# Callable: type-changing
assert_type(lmap(str, nums), list[str])
assert_type(lmap(str.upper, strs), list[str])
def double(x: int) -> int: return x * 2
assert_type(lmap(double, nums), list[int])
# FIX: should add examples to type check both correct and incorrect (with expected error E:)

# None: identity, preserves element type
assert_type(lmap(None, nums), list[int])
assert_type(lmap(None, strs), list[str])

# Set: membership test -> bool
assert_type(lmap({1, 2, 3}, nums), list[bool])
assert_type(lmap(frozenset({"a", "b"}), strs), list[bool])

# str: regex finder
assert_type(lmap(r"\d+", strs), list[_ReResult | None])
# bytes: regex finder
assert_type(lmap(b"\\d+", strs), list[_ReResult | None])
# re.Pattern: regex finder
assert_type(lmap(re.compile(r"\d+"), strs), list[_ReResult | None])

# int: itemgetter on sequences
assert_type(lmap(0, int_pairs), list[int])
str_pairs: list[list[str]] = [["a", "b"], ["c", "d"]]
assert_type(lmap(0, str_pairs), list[str])
assert_type(lmap(0, strs), list[str])

# slice: itemgetter on sequences, returns subsequence
int_lists: list[list[int]] = [nums, nums]
assert_type(lmap(slice(0, 2), int_lists), list[Sequence[int]])

# Mapping: lookup, returns value type
lookup: dict[str, int] = {"a": 1, "b": 2, "c": 3}
assert_type(lmap(lookup, strs), list[int])

# Multi-seq callable
def add_int(a: int, b: int) -> int: return a + b
assert_type(lmap(add_int, nums, nums), list[int])

### map: same as lmap but returns Iterator ###

# Callable
assert_type(map(str, nums), Iterator[str])
assert_type(map(double, nums), Iterator[int])
# None: identity
assert_type(map(None, nums), Iterator[int])
# Set: membership
assert_type(map({1, 2, 3}, nums), Iterator[bool])
# Regex
assert_type(map(r"\d+", strs), Iterator[_ReResult | None])
# int: itemgetter
assert_type(map(0, int_pairs), Iterator[int])
# slice: itemgetter
assert_type(map(slice(0, 2), int_lists), Iterator[Sequence[int]])
# Mapping: lookup
assert_type(map(lookup, strs), Iterator[int])

### filter/lfilter: predicate, element type preserved ###

assert_type(filter(bool, nums), Iterator[int])
assert_type(lfilter(bool, nums), list[int])

assert_type(remove(bool, nums), Iterator[int])
assert_type(lremove(bool, nums), list[int])

# -- Keep --
assert_type(keep(nums), Iterator[int])
assert_type(lkeep(nums), list[int])

# -- Without --
assert_type(without(nums, 1, 2), Iterator[int])
assert_type(lwithout(nums, 1, 2), list[int])

# -- Concat / Flatten --
assert_type(concat(nums, nums), Iterator[int])
assert_type(lconcat(nums, nums), list[int])
assert_type(cat([nums, nums]), Iterator[int])
assert_type(lcat([nums, nums]), list[int])
assert_type(flatten([1, [2, [3]]]), Iterator[Any])
assert_type(lflatten([1, [2, [3]]]), list[Any])

# -- Interleave / Interpose --
assert_type(interleave(nums, nums), Iterator[int])
assert_type(interpose(0, nums), Iterator[int])

# -- Distinct --
assert_type(distinct(nums), Iterator[int])
def int_to_str(x: int) -> str: return str(x)
assert_type(distinct(nums, key=int_to_str), Iterator[int])
assert_type(ldistinct(nums), list[int])

# -- Takewhile / Dropwhile --
assert_type(takewhile(nums), Iterator[int])
assert_type(takewhile(bool, nums), Iterator[int])
assert_type(dropwhile(nums), Iterator[int])
assert_type(dropwhile(bool, nums), Iterator[int])

# -- Split --
yes, no = split(bool, nums)
assert_type(yes, Iterator[int])
assert_type(no, Iterator[int])

lyes, lno = lsplit(bool, nums)
assert_type(lyes, list[int])
assert_type(lno, list[int])

a, b = split_at(2, nums)
assert_type(a, Iterator[int])
la, lb = lsplit_at(2, nums)
assert_type(la, list[int])

sa, sb = split_by(bool, nums)
assert_type(sa, Iterator[int])
lsa, lsb = lsplit_by(bool, nums)
assert_type(lsa, list[int])

# -- Grouping with named callables --
assert_type(group_by(int_to_str, nums), dict[str, list[int]])
assert_type(group_values([("a", 1), ("a", 2), ("b", 3)]), dict[str, list[int]])
assert_type(count_by(int_to_str, nums), dict[str, int])
assert_type(count_reps(nums), dict[int, int])

# -- Partitioning --
assert_type(partition(2, nums), Iterator[list[int]])
assert_type(partition(2, 1, nums), Iterator[list[int]])
assert_type(lpartition(2, nums), list[list[int]])
assert_type(chunks(2, nums), Iterator[list[int]])
assert_type(lchunks(2, nums), list[list[int]])

# -- Pairing --
assert_type(with_prev(nums), Iterator[tuple[int, int | None]])
assert_type(with_next(nums), Iterator[tuple[int, int | None]])
assert_type(pairwise(nums), Iterator[tuple[int, int]])

# -- Zip --
# FIX: should do better than Any for common cases, here we can say it's list[tuple[int, str]]
#      check how stdlib zip works
assert_type(lzip(nums, strs), list[tuple[Any, ...]])

# -- Reductions --
def add(a: int, b: int) -> int: return a + b
assert_type(lreductions(add, nums), list[int])
assert_type(lsums(nums), list[int])

# -- Should be errors --
take("nope", nums)  # E: wrong arg type
first(42)  # E: not iterable
