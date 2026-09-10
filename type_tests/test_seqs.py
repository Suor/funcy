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

# Typed helper functions
def int_to_str(x: int) -> str: return str(x)

# -- Generators --
def make_int() -> int: return 1
def double_int(x: int) -> int: return x * 2
reveal_type(repeatedly(make_int))  # R: Iterator[int]
reveal_type(repeatedly(make_int, 5))  # R: Iterator[int]
reveal_type(iterate(double_int, 1))  # R: Iterator[int]

# -- Slicing --
reveal_type(take(3, nums))  # R: list[int]
reveal_type(drop(1, nums))  # R: Iterator[int]
reveal_type(first(nums))  # R: int | None
reveal_type(second(nums))  # R: int | None
reveal_type(nth(0, nums))  # R: int | None
reveal_type(last(nums))  # R: int | None
reveal_type(rest(nums))  # R: Iterator[int]
reveal_type(butlast(nums))  # R: Iterator[int]
reveal_type(ilen(nums))  # R: int

### lmap: comprehensive extended function protocol tests ###

# Callable: type-changing
reveal_type(lmap(int_to_str, nums))  # R: list[str]
reveal_type(lmap(str.upper, strs))  # R: list[str]
def double(x: int) -> int: return x * 2
reveal_type(lmap(double, nums))  # R: list[int]

# None: identity, preserves element type
reveal_type(lmap(None, nums))  # R: list[int]
reveal_type(lmap(None, strs))  # R: list[str]

# Set: membership test -> bool
reveal_type(lmap({1, 2, 3}, nums))  # R: list[bool]
reveal_type(lmap(frozenset({"a", "b"}), strs))  # R: list[bool]

# str: regex finder
reveal_type(lmap(r"\d+", strs))  # R: list[str | tuple[str, ...] | dict[str, str] | None]
# bytes: regex finder
reveal_type(lmap(b"\\d+", strs))  # R: list[str | tuple[str, ...] | dict[str, str] | None]
# re.Pattern: regex finder
reveal_type(lmap(re.compile(r"\d+"), strs))  # R: list[str | tuple[str, ...] | dict[str, str] | None]

# int: itemgetter on sequences
reveal_type(lmap(0, int_pairs))  # R: list[int]
str_pairs: list[list[str]] = [["a", "b"], ["c", "d"]]
reveal_type(lmap(0, str_pairs))  # R: list[str]
reveal_type(lmap(0, strs))  # R: list[str]

# slice: itemgetter on sequences, returns subsequence
int_lists: list[list[int]] = [nums, nums]
reveal_type(lmap(slice(0, 2), int_lists))  # R: list[Sequence[int]]

# Mapping: lookup, returns value type
lookup: dict[str, int] = {"a": 1, "b": 2, "c": 3}
reveal_type(lmap(lookup, strs))  # R: list[int]

# Multi-seq callable
def add_int(a: int, b: int) -> int: return a + b
reveal_type(lmap(add_int, nums, nums))  # R: list[int]

### map: same as lmap but returns Iterator ###

reveal_type(map(int_to_str, nums))  # R: Iterator[str]
reveal_type(map(double, nums))  # R: Iterator[int]
# None: identity
reveal_type(map(None, nums))  # R: Iterator[int]
# Set: membership
reveal_type(map({1, 2, 3}, nums))  # R: Iterator[bool]
# Regex
reveal_type(map(r"\d+", strs))  # R: Iterator[str | tuple[str, ...] | dict[str, str] | None]
# int: itemgetter
reveal_type(map(0, int_pairs))  # R: Iterator[int]
# slice: itemgetter
reveal_type(map(slice(0, 2), int_lists))  # R: Iterator[Sequence[int]]
# Mapping: lookup
reveal_type(map(lookup, strs))  # R: Iterator[int]

### filter/lfilter: predicate, element type preserved ###

reveal_type(filter(bool, nums))  # R: Iterator[int]
reveal_type(lfilter(bool, nums))  # R: list[int]

reveal_type(remove(bool, nums))  # R: Iterator[int]
reveal_type(lremove(bool, nums))  # R: list[int]

# -- Keep --
reveal_type(keep(nums))  # R: Iterator[int]
reveal_type(keep(int_to_str, nums))  # R: Iterator[str]
reveal_type(keep(None, nums))  # R: Iterator[int]
reveal_type(keep(lookup, strs))  # R: Iterator[int]
reveal_type(lkeep(nums))  # R: list[int]
reveal_type(lkeep(int_to_str, nums))  # R: list[str]
reveal_type(lkeep(None, nums))  # R: list[int]
reveal_type(lkeep(lookup, strs))  # R: list[int]

# -- Without --
reveal_type(without(nums, 1, 2))  # R: Iterator[int]
reveal_type(lwithout(nums, 1, 2))  # R: list[int]

# -- Concat / Flatten --
reveal_type(concat(nums, nums))  # R: Iterator[int]
reveal_type(lconcat(nums, nums))  # R: list[int]
reveal_type(cat([nums, nums]))  # R: Iterator[int]
reveal_type(lcat([nums, nums]))  # R: list[int]
# Note: flatten is recursive, can't type the leaf element statically
reveal_type(flatten([1, [2, [3]]]))  # R: Iterator[Any]
reveal_type(lflatten([1, [2, [3]]]))  # R: list[Any]

# -- Mapcat --
def int_to_list(x: int) -> list[str]: return [str(x)]
reveal_type(mapcat(int_to_list, nums))  # R: Iterator[str]
reveal_type(lmapcat(int_to_list, nums))  # R: list[str]

# -- Interleave / Interpose --
reveal_type(interleave(nums, nums))  # R: Iterator[int]
reveal_type(interpose(0, nums))  # R: Iterator[int]

# -- Distinct --
reveal_type(distinct(nums))  # R: Iterator[int]
reveal_type(distinct(nums, key=int_to_str))  # R: Iterator[int]
reveal_type(ldistinct(nums))  # R: list[int]

# -- Takewhile / Dropwhile --
reveal_type(takewhile(nums))  # R: Iterator[int]
reveal_type(takewhile(bool, nums))  # R: Iterator[int]
reveal_type(dropwhile(nums))  # R: Iterator[int]
reveal_type(dropwhile(bool, nums))  # R: Iterator[int]

# -- Split --
yes, no = split(bool, nums)
reveal_type(yes)  # R: Iterator[int]
reveal_type(no)  # R: Iterator[int]

lyes, lno = lsplit(bool, nums)
reveal_type(lyes)  # R: list[int]
reveal_type(lno)  # R: list[int]

a, b = split_at(2, nums)
reveal_type(a)  # R: Iterator[int]
la, lb = lsplit_at(2, nums)
reveal_type(la)  # R: list[int]

sa, sb = split_by(bool, nums)
reveal_type(sa)  # R: Iterator[int]
lsa, lsb = lsplit_by(bool, nums)
reveal_type(lsa)  # R: list[int]

# -- Grouping with named callables --
reveal_type(group_by(int_to_str, nums))  # R: dict[str, list[int]]
def int_to_tags(x: int) -> list[str]: return ["even"] if x % 2 == 0 else ["odd"]
reveal_type(group_by_keys(int_to_tags, nums))  # R: dict[str, list[int]]
reveal_type(count_by(int_to_str, nums))  # R: dict[str, int]
reveal_type(count_reps(nums))  # R: dict[int, int]

# group_values needs typed input (inline literal Unknown in ty)
str_int_pairs: list[tuple[str, int]] = [("a", 1), ("a", 2), ("b", 3)]
reveal_type(group_values(str_int_pairs))  # R: dict[str, list[int]]

# -- Partitioning --
reveal_type(partition(2, nums))  # R: Iterator[list[int]]
reveal_type(partition(2, 1, nums))  # R: Iterator[list[int]]
reveal_type(lpartition(2, nums))  # R: list[list[int]]
reveal_type(chunks(2, nums))  # R: Iterator[list[int]]
reveal_type(lchunks(2, nums))  # R: list[list[int]]
reveal_type(partition_by(int_to_str, nums))  # R: Iterator[Iterator[int]]
reveal_type(lpartition_by(int_to_str, nums))  # R: list[list[int]]

# -- Pairing --
reveal_type(with_prev(nums))  # R: Iterator[tuple[int, int | None]]
reveal_type(with_next(nums))  # R: Iterator[tuple[int, int | None]]
reveal_type(pairwise(nums))  # R: Iterator[tuple[int, int]]

# -- Zip --
reveal_type(lzip(nums, strs))  # R: list[tuple[int, str]]

# -- Reductions --
def add(a: int, b: int) -> int: return a + b
reveal_type(reductions(add, nums))  # R: Iterator[int]
reveal_type(reductions(add, nums, 0))  # R: Iterator[int]
reveal_type(lreductions(add, nums))  # R: list[int]
reveal_type(lreductions(add, nums, 0))  # R: list[int]
reveal_type(sums(nums))  # R: Iterator[int]
reveal_type(sums(nums, 0))  # R: Iterator[int]
reveal_type(lsums(nums))  # R: list[int]
reveal_type(lsums(nums, 0))  # R: list[int]

# -- Extended function return type tests --
reveal_type(map(None, nums))  # R: Iterator[int]
reveal_type(map({1, 2}, nums))  # R: Iterator[bool]
reveal_type(filter(None, nums))  # R: Iterator[int]
reveal_type(filter({1, 2}, nums))  # R: Iterator[int]
reveal_type(group_by(None, nums))  # R: dict[int, list[int]]
reveal_type(group_by({1, 2}, nums))  # R: dict[bool, list[int]]
reveal_type(count_by(None, nums))  # R: dict[int, int]

# -- Should be errors --
take("nope", nums)  # E: wrong arg type
first(42)  # E: not iterable
lmap(double, 42)  # E: not iterable

# Extended function type mismatches — predicates
filter(re.compile(r"x"), nums)  # E: regex pred requires str elements
lfilter(r"\d+", nums)  # E: regex pred requires str elements
remove(re.compile(r"x"), nums)  # E: regex pred requires str elements
filter({1: True}, strs)  # E: Mapping[int] pred vs Iterable[str]  # XFAIL[ty]: infers literal as dict[int | str, bool]
lremove({1: True}, strs)  # E: Mapping[int] pred vs Iterable[str]  # XFAIL[ty]: infers literal as dict[int | str, bool]
int_bool_map: dict[int, bool] = {1: True}
filter(int_bool_map, strs)  # E: Mapping[int] pred vs Iterable[str]
lremove(int_bool_map, strs)  # E: Mapping[int] pred vs Iterable[str]

# Extended function type mismatches — mappers
map({1: "a"}, strs)  # E: Mapping[int, str] vs Iterable[str]  # XFAIL[ty]: not caught
lmap({1: "a"}, strs)  # E: Mapping[int, str] vs Iterable[str]  # XFAIL[ty]: not caught
group_by({1: "a"}, strs)  # E: Mapping[int, str] vs Iterable[str]  # XFAIL[ty]: not caught
count_by({1: "a"}, strs)  # E: Mapping[int, str] vs Iterable[str]  # XFAIL[ty]: not caught
