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

nums = [1, 2, 3, 4, 5]
strs = ["a", "b", "c"]
int_pairs: list[tuple[int, int]] = [(1, 2), (3, 4)]

# -- Generators --
assert_type(repeatedly(lambda: 1), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(repeatedly(lambda: 1, 5), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(iterate(lambda x: x * 2, 1), Iterator[int])  # XFAIL[ty]: Unknown TypeVars

# -- Slicing --
assert_type(take(3, nums), list[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(drop(1, nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(first(nums), int | None)  # XFAIL[ty]: Unknown TypeVars
assert_type(second(nums), int | None)  # XFAIL[ty]: Unknown TypeVars
assert_type(nth(0, nums), int | None)  # XFAIL[ty]: Unknown TypeVars
assert_type(last(nums), int | None)  # XFAIL[ty]: Unknown TypeVars
assert_type(rest(nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(butlast(nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(ilen(nums), int)

### lmap: comprehensive extended function protocol tests ###

# Callable: type-changing
assert_type(lmap(str, nums), list[str])
assert_type(lmap(str.upper, strs), list[str])  # XFAIL[ty]: Unknown TypeVars
def double(x: int) -> int: return x * 2
assert_type(lmap(double, nums), list[int])  # XFAIL[ty]: Unknown TypeVars
# FIX: should add examples to type check both correct and incorrect (with expected error E:)

# None: identity, preserves element type
assert_type(lmap(None, nums), list[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(lmap(None, strs), list[str])  # XFAIL[ty]: Unknown TypeVars

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
assert_type(lmap(0, int_pairs), list[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(lmap(0, [["a", "b"], ["c", "d"]]), list[str])  # XFAIL[ty]: Unknown TypeVars
assert_type(lmap(0, ["abc", "def"]), list[str])  # XFAIL[ty]: Unknown TypeVars

# slice: itemgetter on sequences, returns subsequence
assert_type(lmap(slice(0, 2), [nums, nums]), list[Sequence[int]])  # XFAIL[ty]: Unknown TypeVars

# Mapping: lookup, returns value type
lookup: dict[str, int] = {"a": 1, "b": 2, "c": 3}
assert_type(lmap(lookup, strs), list[int])  # XFAIL[ty]: Unknown TypeVars

# Multi-seq callable
def add_int(a: int, b: int) -> int: return a + b
assert_type(lmap(add_int, nums, nums), list[int])  # XFAIL[ty]: Unknown TypeVars

### map: same as lmap but returns Iterator ###

# Callable
assert_type(map(str, nums), Iterator[str])
assert_type(map(double, nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
# None: identity
assert_type(map(None, nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
# Set: membership
assert_type(map({1, 2, 3}, nums), Iterator[bool])
# Regex
assert_type(map(r"\d+", strs), Iterator[_ReResult | None])
# int: itemgetter
assert_type(map(0, int_pairs), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
# slice: itemgetter
assert_type(map(slice(0, 2), [nums, nums]), Iterator[Sequence[int]])  # XFAIL[ty]: Unknown TypeVars
# Mapping: lookup
assert_type(map(lookup, strs), Iterator[int])  # XFAIL[ty]: Unknown TypeVars

### filter/lfilter: predicate, element type preserved ###

assert_type(filter(bool, nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(lfilter(bool, nums), list[int])  # XFAIL[ty]: Unknown TypeVars

assert_type(remove(bool, nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(lremove(bool, nums), list[int])  # XFAIL[ty]: Unknown TypeVars

# -- Keep --
assert_type(keep(nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(lkeep(nums), list[int])  # XFAIL[ty]: Unknown TypeVars

# -- Without --
assert_type(without(nums, 1, 2), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(lwithout(nums, 1, 2), list[int])  # XFAIL[ty]: Unknown TypeVars

# -- Concat / Flatten --
assert_type(concat(nums, nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(lconcat(nums, nums), list[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(cat([nums, nums]), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(lcat([nums, nums]), list[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(flatten([1, [2, [3]]]), Iterator[Any])
assert_type(lflatten([1, [2, [3]]]), list[Any])

# -- Interleave / Interpose --
assert_type(interleave(nums, nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(interpose(0, nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars

# -- Distinct --
assert_type(distinct(nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(distinct(nums, key=str), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(ldistinct(nums), list[int])  # XFAIL[ty]: Unknown TypeVars

# -- Takewhile / Dropwhile --
assert_type(takewhile(nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(takewhile(bool, nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(dropwhile(nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(dropwhile(bool, nums), Iterator[int])  # XFAIL[ty]: Unknown TypeVars

# -- Split --
yes, no = split(bool, nums)
assert_type(yes, Iterator[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(no, Iterator[int])  # XFAIL[ty]: Unknown TypeVars

lyes, lno = lsplit(bool, nums)
assert_type(lyes, list[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(lno, list[int])  # XFAIL[ty]: Unknown TypeVars

a, b = split_at(2, nums)
assert_type(a, Iterator[int])  # XFAIL[ty]: Unknown TypeVars
la, lb = lsplit_at(2, nums)
assert_type(la, list[int])  # XFAIL[ty]: Unknown TypeVars

sa, sb = split_by(bool, nums)
assert_type(sa, Iterator[int])  # XFAIL[ty]: Unknown TypeVars
lsa, lsb = lsplit_by(bool, nums)
assert_type(lsa, list[int])  # XFAIL[ty]: Unknown TypeVars

# -- Grouping with named callables --
assert_type(group_by(str, nums), dict[str, list[int]])  # XFAIL[ty]: Unknown TypeVars
assert_type(group_values([("a", 1), ("a", 2), ("b", 3)]), dict[str, list[int]])
assert_type(count_by(str, nums), dict[str, int])
assert_type(count_reps(nums), dict[int, int])  # XFAIL[ty]: Unknown TypeVars

# -- Partitioning --
assert_type(partition(2, nums), Iterator[list[int]])  # XFAIL[ty]: Unknown TypeVars
assert_type(partition(2, 1, nums), Iterator[list[int]])  # XFAIL[ty]: Unknown TypeVars
assert_type(lpartition(2, nums), list[list[int]])  # XFAIL[ty]: Unknown TypeVars
assert_type(chunks(2, nums), Iterator[list[int]])  # XFAIL[ty]: Unknown TypeVars
assert_type(lchunks(2, nums), list[list[int]])  # XFAIL[ty]: Unknown TypeVars
assert_type(lpartition_by(str, nums), list[list[int]])  # XFAIL[ty]: Unknown TypeVars

# -- Pairing --
assert_type(with_prev(nums), Iterator[tuple[int, int | None]])  # XFAIL[ty]: Unknown TypeVars
assert_type(with_next(nums), Iterator[tuple[int, int | None]])  # XFAIL[ty]: Unknown TypeVars
assert_type(pairwise(nums), Iterator[tuple[int, int]])  # XFAIL[ty]: Unknown TypeVars

# -- Zip --
# FIX: should do better than Any for common cases, here we can say it's list[tuple[int, str]]
#      check how stdlib zip works
assert_type(lzip(nums, strs), list[tuple[Any, ...]])

# -- Reductions --
def add(a: int, b: int) -> int: return a + b
assert_type(lreductions(add, nums), list[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(lsums(nums), list[int])  # XFAIL[ty]: Unknown TypeVars

# -- Should be errors --
take("nope", nums)  # E: wrong arg type
first(42)  # E: not iterable
