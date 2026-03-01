from typing import Any, assert_type
from collections.abc import Iterable, Iterator, Mapping, MutableMapping, Sequence

# Real abstract-type implementations (not concrete types cast to abstract — checkers see through that)
class StrIntMapping(Mapping[str, int]):
    def __getitem__(self, k: str) -> int: return 0
    def __iter__(self) -> Iterator[str]: return iter([])
    def __len__(self) -> int: return 0

class StrIntMutableMapping(MutableMapping[str, int]):
    def __getitem__(self, k: str) -> int: return 0
    def __setitem__(self, k: str, v: int) -> None: pass
    def __delitem__(self, k: str) -> None: pass
    def __iter__(self) -> Iterator[str]: return iter([])
    def __len__(self) -> int: return 0
from funcy import (
    empty, iteritems, itervalues,
    join, merge, join_with, merge_with,
    walk, walk_keys, walk_values, select, select_keys, select_values,
    split_keys, compact,
    is_distinct, zipdict, flip, project, omit, zip_values, zip_dicts,
    where, pluck, pluck_attr, invoke,
    lwhere, lpluck, lpluck_attr, linvoke,
    get_in, get_lax, set_in, update_in, del_in, has_path,
)
from funcy.colls import all, any, none, one, some  # shadow builtins

_ReResult = str | tuple[str, ...] | dict[str, str]

# Typed variables for ty TypeVar inference
si_dict: dict[str, int] = {"a": 1, "b": 2, "c": 3}
si_dict2: dict[str, int] = {"x": 10}
int_list: list[int] = [1, 2, 3]
int_set: set[int] = {1, 2, 3}
str_keys: list[str] = ["a", "b"]
int_vals: list[int] = [1, 2]
strs: list[str] = ["abc", "def"]
int_pairs: list[tuple[int, int]] = [(1, 2)]

# Typed collections for join tests (avoid inline literals that ty can't infer)
dict_list: list[dict[str, int]] = [{"a": 1}, {"b": 2}]
int_list_list: list[list[int]] = [[1, 2], [3]]
int_set_list: list[set[int]] = [{1, 2}, {3}]

# Typed functions (not Callable-annotated lambdas — ty can't infer those through overloads)
def pred_true(p: object) -> bool: return True
def pred_gt0(x: int) -> bool: return x > 0
def pred_gt1(v: int) -> bool: return v > 1
def pred_ne_c(k: str) -> bool: return k != "c"
def pred_eq_a(k: str) -> bool: return k == "a"

# Typed dict for walk_values int/lambda tests
str_to_intlist: dict[str, Sequence[int]] = {"a": [1, 2], "b": [3, 4]}
str_to_int1: dict[str, int] = {"a": 1}

# -- merge --
reveal_type(merge(si_dict, si_dict2))  # R: dict[str, int]
reveal_type(merge(int_list, int_list))  # R: list[int]
reveal_type(merge(int_set, int_set))  # R: set[int]

# -- join: may be None --
reveal_type(join(dict_list))  # R: dict[str, int] | None
reveal_type(join(int_list_list))  # R: list[int] | None
reveal_type(join(int_set_list))  # R: set[int] | None
# Canary: detect when ty starts inferring types of inline list literals
assert_type(join([{"a": 1}, {"b": 2}]), dict[str, int] | None)  # XFAIL[ty]: inline list literal Unknown

# -- walk_keys: Callable transforms keys, values preserved --
def str_key_to_int(k: str) -> int: return ord(k)
reveal_type(walk_keys(str_key_to_int, si_dict))  # R: dict[int, int]
reveal_type(walk_keys(str.upper, si_dict))  # R: dict[str, int]
# walk_keys: Canary for ty builtin overload resolution
reveal_type(walk_keys(len, si_dict))  # R: dict[int, int]  # XFAIL[ty]: len overload not matched
# walk_keys: None = identity
reveal_type(walk_keys(None, si_dict))  # R: dict[str, int]
# walk_keys: Set = membership -> bool keys
reveal_type(walk_keys({"a", "b"}, si_dict))  # R: dict[bool, int]
# walk_keys: Mapping = lookup -> mapped key type
key_map: dict[str, int] = {"a": 1, "b": 2}
reveal_type(walk_keys(key_map, si_dict))  # R: dict[int, int]
# walk_keys: int = itemgetter on sequence keys
seq_key_dict: dict[Sequence[int], int] = {(1, 2): 10, (3, 4): 20}
reveal_type(walk_keys(0, seq_key_dict))  # R: dict[int, int]
# walk_keys: str/regex = regex finder on keys
reveal_type(walk_keys(r"\d+", si_dict))  # R: dict[str | tuple[str, ...] | dict[str, str] | None, int]

# -- walk_values: Callable transforms values, keys preserved --
def int_to_str(v: int) -> str: return str(v)
reveal_type(walk_values(int_to_str, si_dict))  # R: dict[str, str]
reveal_type(walk_values(pred_gt0, str_to_int1))  # R: dict[str, bool]
# walk_values: None = identity
reveal_type(walk_values(None, si_dict))  # R: dict[str, int]
# walk_values: Set = membership -> bool values
reveal_type(walk_values({1, 2}, si_dict))  # R: dict[str, bool]
# walk_values: int = itemgetter on sequence values
reveal_type(walk_values(0, str_to_intlist))  # R: dict[str, int]
# walk_values: slice = subsequence of sequence values
reveal_type(walk_values(slice(0, 2), str_to_intlist))  # R: dict[str, Sequence[int]]
# walk_values: Mapping = lookup -> mapped value type
val_map: dict[int, str] = {1: "one", 2: "two"}
reveal_type(walk_values(val_map, si_dict))  # R: dict[str, str]
# walk_values: str/regex = regex finder on values
str_dict: dict[str, str] = {"a": "123", "b": "abc"}
reveal_type(walk_values(r"\d+", str_dict))  # R: dict[str, str | tuple[str, ...] | dict[str, str] | None]

# -- walk: Callable transforms items, preserves collection type --
reveal_type(walk(int_to_str, int_list))  # R: list[str]
reveal_type(walk(int_to_str, int_set))  # R: set[str]
# walk: XFunc variants on list/set
reveal_type(walk(None, int_list))  # R: list[int]
reveal_type(walk(None, int_set))  # R: set[int]
# walk: dict with properly typed pair function
def swap_pair(pair: tuple[str, int]) -> tuple[int, str]: return (pair[1], str(pair[0]))
reveal_type(walk(swap_pair, si_dict))  # R: dict[int, str]
# walk: dict with untyped/extended function falls back to dict[Any, Any]
reveal_type(walk(int_to_str, si_dict))  # R: dict[Any, Any]
# walk: frozenset
int_fset: frozenset[int] = frozenset({1, 2, 3})
reveal_type(walk(int_to_str, int_fset))  # R: frozenset[str]
# -- walk_keys: always returns dict --
reveal_type(walk_keys(str_key_to_int, si_dict))  # R: dict[int, int]
real_mapping = StrIntMapping()
real_mutable_mapping = StrIntMutableMapping()
# walk: Mapping with typed pair function returns dict
reveal_type(walk(swap_pair, real_mapping))  # R: dict[int, str]
# walk: MutableMapping with typed pair function returns dict
reveal_type(walk(swap_pair, StrIntMutableMapping()))  # R: dict[int, str]
reveal_type(walk_keys(str_key_to_int, real_mapping))  # R: dict[int, int]
# walk: collection of pairs (list[tuple[K, V]]) — handled by list XFunc overload
str_int_pairs: list[tuple[str, int]] = [("a", 1), ("b", 2)]
def transform_pair(p: tuple[str, int]) -> tuple[int, str]: return (p[1], str(p[0]))
reveal_type(walk(transform_pair, str_int_pairs))  # R: list[tuple[int, str]]
reveal_type(walk(None, str_int_pairs))  # R: list[tuple[str, int]]
reveal_type(walk(str, str_int_pairs))  # R: list[str]  # XFAIL[ty]: TypeVar inference gives list[tuple[str, int]]

# -- walk_keys: MutableMapping returns dict --
reveal_type(walk_keys(str_key_to_int, real_mutable_mapping))  # R: dict[int, int]
reveal_type(walk_keys(None, real_mutable_mapping))  # R: dict[str, int]
# -- walk_keys: collection of pairs preserves collection type --
reveal_type(walk_keys(str_key_to_int, str_int_pairs))  # R: list[tuple[int, int]]
reveal_type(walk_keys(str.upper, str_int_pairs))  # R: list[tuple[str, int]]
reveal_type(walk_keys(None, str_int_pairs))  # R: list[tuple[str, int]]
reveal_type(walk_keys({"a", "b"}, str_int_pairs))  # R: list[tuple[bool, int]]
reveal_type(walk_keys(key_map, str_int_pairs))  # R: list[tuple[int, int]]
# walk_keys: collection of pairs with set
str_int_pair_set: set[tuple[str, int]] = {("a", 1), ("b", 2)}
reveal_type(walk_keys(str_key_to_int, str_int_pair_set))  # R: set[tuple[int, int]]
reveal_type(walk_keys(None, str_int_pair_set))  # R: set[tuple[str, int]]

# -- walk_values: always returns dict --
reveal_type(walk_values(int_to_str, si_dict))  # R: dict[str, str]
reveal_type(walk_values(int_to_str, real_mapping))  # R: dict[str, str]
# -- walk_values: MutableMapping returns dict --
reveal_type(walk_values(int_to_str, real_mutable_mapping))  # R: dict[str, str]
reveal_type(walk_values(None, real_mutable_mapping))  # R: dict[str, int]
# -- walk_values: collection of pairs preserves collection type --
reveal_type(walk_values(int_to_str, str_int_pairs))  # R: list[tuple[str, str]]
reveal_type(walk_values(None, str_int_pairs))  # R: list[tuple[str, int]]
reveal_type(walk_values({1, 2}, str_int_pairs))  # R: list[tuple[str, bool]]
reveal_type(walk_values(val_map, str_int_pairs))  # R: list[tuple[str, str]]
# walk_values: collection of pairs with set
reveal_type(walk_values(int_to_str, str_int_pair_set))  # R: set[tuple[str, str]]

# -- select: filtering preserves type --
reveal_type(select(pred_true, si_dict))  # R: dict[str, int]
reveal_type(select(pred_gt0, int_list))  # R: list[int]
reveal_type(select(pred_gt0, int_set))  # R: set[int]
# select: XPred variants on list
reveal_type(select(None, int_list))  # R: list[int]
reveal_type(select({1, 2}, int_list))  # R: list[int]  # XFAIL[ty]: Set pred Any|int
int_lookup: dict[int, str] = {1: "yes", 2: "yes"}
reveal_type(select(int_lookup, int_list))  # R: list[int]
# select: frozenset
reveal_type(select(pred_gt0, int_fset))  # R: frozenset[int]
reveal_type(select(None, int_fset))  # R: frozenset[int]
# select: dict with Callable on pairs
def pair_pred(pair: tuple[str, int]) -> bool: return pair[1] > 1
reveal_type(select(pair_pred, si_dict))  # R: dict[str, int]
# select: Mapping with Callable on pairs
reveal_type(select(pred_true, real_mapping))  # R: Mapping[str, int]
# select: MutableMapping with Callable on pairs
reveal_type(select(pred_true, real_mutable_mapping))  # R: MutableMapping[str, int]

# -- select_keys / select_values: preserves collection type --
d: dict[str, int] = {"a": 1, "b": 2, "c": 3}
reveal_type(select_keys(pred_ne_c, d))  # R: dict[str, int]
reveal_type(select_values(pred_gt1, d))  # R: dict[str, int]
# select_keys / select_values with real Mapping input preserves Mapping type
reveal_type(select_keys(pred_ne_c, real_mapping))  # R: Mapping[str, int]
reveal_type(select_values(pred_gt1, real_mapping))  # R: Mapping[str, int]
# select_keys / select_values with MutableMapping
reveal_type(select_keys(pred_ne_c, real_mutable_mapping))  # R: MutableMapping[str, int]
reveal_type(select_values(pred_gt1, real_mutable_mapping))  # R: MutableMapping[str, int]

# -- compact: preserves type --
reveal_type(compact(d))  # R: dict[str, int]
maybe_list: list[int | None] = [0, 1, None, 2]
reveal_type(compact(maybe_list))  # R: list[int | None]
# compact: set, frozenset
maybe_set: set[int | None] = {0, 1, None, 2}
# FIX: can we type that it removes | None? if not we should add a failing test. But maybe guards
#      will do the trick
reveal_type(compact(maybe_set))  # R: set[int | None]
maybe_fset: frozenset[int | None] = frozenset({0, 1, None, 2})
reveal_type(compact(maybe_fset))  # R: frozenset[int | None]
# compact: Mapping and MutableMapping (collection of pairs — filters by value truthiness)
reveal_type(compact(real_mapping))  # R: Mapping[str, int]
reveal_type(compact(real_mutable_mapping))  # R: MutableMapping[str, int]
# compact: collection of pairs as list[tuple[K, V]]
compact_pairs: list[tuple[str, int | None]] = [("a", 1), ("b", None), ("c", 0)]
reveal_type(compact(compact_pairs))  # R: list[tuple[str, int | None]]

# -- empty: preserves type --
reveal_type(empty(d))  # R: dict[str, int]
reveal_type(empty(int_list))  # R: list[int]

# -- iteritems / itervalues --
reveal_type(iteritems(d))  # R: Iterable[tuple[str, int]]
reveal_type(itervalues(d))  # R: Iterable[int]

# -- split_keys --
reveal_type(split_keys(pred_eq_a, d))  # R: tuple[dict[str, int], dict[str, int]]
reveal_type(split_keys(r"\d+", d))  # R: tuple[dict[str, int], dict[str, int]]

# -- select_keys: XPred variants --
reveal_type(select_keys(None, d))  # R: dict[str, int]
reveal_type(select_keys({"a", "b"}, d))  # R: dict[str, int]  # XFAIL[ty]: Set pred Any|str
reveal_type(select_keys(r"\w+", d))  # R: dict[str, int]
key_lookup: dict[str, int] = {"a": 1, "b": 2}
reveal_type(select_keys(key_lookup, d))  # R: dict[str, int]

# -- select_values: XPred variants --
reveal_type(select_values(None, d))  # R: dict[str, int]
reveal_type(select_values({1, 2}, d))  # R: dict[str, int]  # XFAIL[ty]: Set pred Any|int
int_to_int_map: dict[int, str] = {1: "yes", 2: "yes"}
reveal_type(select_values(int_to_int_map, d))  # R: dict[str, int]

# -- select_keys / select_values: collection of pairs --
sk_pairs: list[tuple[str, int]] = [("a", 1), ("b", 2), ("c", 3)]
reveal_type(select_keys(pred_ne_c, sk_pairs))  # R: list[tuple[str, int]]
reveal_type(select_values(pred_gt1, sk_pairs))  # R: list[tuple[str, int]]
reveal_type(select_keys(None, sk_pairs))  # R: list[tuple[str, int]]
reveal_type(select_values(None, sk_pairs))  # R: list[tuple[str, int]]
reveal_type(select_keys({"a", "b"}, sk_pairs))  # R: list[tuple[str, int]]  # XFAIL[ty]: Set pred Any|str
reveal_type(select_values({1, 2}, sk_pairs))  # R: list[tuple[str, int]]  # XFAIL[ty]: Set pred Any|int
reveal_type(select_keys(r"[ab]", sk_pairs))  # R: list[tuple[str, int]]
sk_pair_set: set[tuple[str, int]] = {("a", 1), ("b", 2)}
reveal_type(select_keys(pred_ne_c, sk_pair_set))  # R: set[tuple[str, int]]
reveal_type(select_values(pred_gt1, sk_pair_set))  # R: set[tuple[str, int]]
reveal_type(select_keys(None, sk_pair_set))  # R: set[tuple[str, int]]
reveal_type(select_values(None, sk_pair_set))  # R: set[tuple[str, int]]

# -- select_keys / select_values with Mapping: XPred variants --
reveal_type(select_keys(None, real_mapping))  # R: Mapping[str, int]
reveal_type(select_keys({"a"}, real_mapping))  # R: Mapping[str, int]  # XFAIL[ty]: Set pred Any|str
reveal_type(select_values(None, real_mapping))  # R: Mapping[str, int]
reveal_type(select_values({1, 2}, real_mapping))  # R: Mapping[str, int]  # XFAIL[ty]: Set pred Any|int

# -- split_keys: XPred variants --
reveal_type(split_keys(None, d))  # R: tuple[dict[str, int], dict[str, int]]
reveal_type(split_keys({"a"}, d))  # R: tuple[dict[str, int], dict[str, int]]  # XFAIL[ty]: Set pred Any|str
reveal_type(split_keys(key_lookup, d))  # R: tuple[dict[str, int], dict[str, int]]

# -- some: XPred variants --
reveal_type(some(r"\d+", strs))  # R: str | None
reveal_type(some({1, 2}, int_list))  # R: int | None  # XFAIL[ty]: Set pred Any|int

# -- flip / project / omit: preserve collection type --
reveal_type(flip(d))  # R: dict[int, str]
reveal_type(project(d, str_keys))  # R: dict[str, int]
reveal_type(omit(d, str_keys))  # R: dict[str, int]
# flip / project / omit with real Mapping
reveal_type(flip(real_mapping))  # R: Mapping[int, str]
reveal_type(project(real_mapping, ["a"]))  # R: Mapping[str, int]  # XFAIL[ty]: TypeVar unification across Mapping + Iterable params gives str | Unknown
reveal_type(omit(real_mapping, ["a"]))  # R: Mapping[str, int]  # XFAIL[ty]: TypeVar unification across Mapping + Iterable params gives str | Unknown
# flip / project / omit with real MutableMapping
reveal_type(flip(real_mutable_mapping))  # R: MutableMapping[int, str]
reveal_type(project(real_mutable_mapping, ["a"]))  # R: MutableMapping[str, int]  # XFAIL[ty]: TypeVar unification across MutableMapping + Iterable params gives str | Unknown
reveal_type(omit(real_mutable_mapping, ["a"]))  # R: MutableMapping[str, int]  # XFAIL[ty]: TypeVar unification across MutableMapping + Iterable params gives str | Unknown
# flip with collection of pairs
reveal_type(flip(str_int_pairs))  # R: list[tuple[int, str]]
reveal_type(flip(str_int_pair_set))  # R: set[tuple[int, str]]
int_str_fset_pairs: frozenset[tuple[int, str]] = frozenset({(1, "a"), (2, "b")})
reveal_type(flip(int_str_fset_pairs))  # R: frozenset[tuple[str, int]]

# -- zipdict --
reveal_type(zipdict(str_keys, int_vals))  # R: dict[str, int]
reveal_type(zipdict(range(3), str_keys))  # R: dict[int, str]

# -- bool-returning functions --
reveal_type(is_distinct(int_list))  # R: bool
reveal_type(is_distinct(int_list, int_to_str))  # R: bool
reveal_type(is_distinct(strs, None))  # R: bool
reveal_type(is_distinct(int_list, {1, 2}))  # R: bool
reveal_type(all(int_list))  # R: bool
reveal_type(all(pred_gt0, int_list))  # R: bool
reveal_type(any(int_list))  # R: bool
reveal_type(any(pred_gt0, int_list))  # R: bool
reveal_type(none(int_list))  # R: bool
reveal_type(none(pred_gt0, int_list))  # R: bool
reveal_type(one(int_list))  # R: bool
reveal_type(one(pred_gt0, int_list))  # R: bool
reveal_type(has_path(si_dict, str_keys))  # R: bool

# -- some returns element type --
maybe_ints: list[int | None] = [0, None, 3]
reveal_type(some(maybe_ints))  # R: int | None
reveal_type(some(pred_gt0, int_list))  # R: int | None

# -- where / lwhere: preserves element type --
records: list[dict[str, int]] = [{"name": 1, "age": 2}]
reveal_type(where(records, name=1))  # R: Iterator[dict[str, int]]
reveal_type(lwhere(records, name=1))  # R: list[dict[str, int]]

# -- pluck / lpluck --
reveal_type(pluck("name", records))  # R: Iterator[int]
reveal_type(lpluck("name", records))  # R: list[int]

# -- pluck_attr / lpluck_attr (dynamic attr, Any is correct) --
reveal_type(pluck_attr("real", int_list))  # R: Iterator[Any]
reveal_type(lpluck_attr("real", int_list))  # R: list[Any]

# -- invoke / linvoke (dynamic method, Any is correct) --
reveal_type(invoke(strs, "upper"))  # R: Iterator[Any]
reveal_type(linvoke(strs, "upper"))  # R: list[Any]

# -- zip_values / zip_dicts --
d1: dict[str, int] = {"a": 1, "b": 2}
d2: dict[str, int] = {"a": 3, "b": 4}
reveal_type(zip_values(d1, d2))  # R: Iterator[tuple[int, ...]]
reveal_type(zip_dicts(d1, d2))  # R: Iterator[tuple[str, tuple[int, ...]]]

# -- get_in / set_in / update_in / del_in: nested access --
nested: dict[str, dict[str, int]] = {"a": {"b": 1}}
reveal_type(get_in(nested, ["a", "b"]))  # R: Any
reveal_type(get_lax(nested, ["a", "b"]))  # R: Any
# set_in / update_in / del_in preserve collection type
reveal_type(set_in(nested, ["a", "b"], 42))  # R: dict[str, dict[str, int]]
def inc(x: int) -> int: return x + 1
reveal_type(update_in(nested, ["a", "b"], inc))  # R: dict[str, dict[str, int]]
reveal_type(del_in(nested, ["a", "b"]))  # R: dict[str, dict[str, int]]
# set_in / update_in / del_in with MutableMapping
reveal_type(set_in(real_mutable_mapping, ["a"], 42))  # R: MutableMapping[str, int]
reveal_type(update_in(real_mutable_mapping, ["a"], inc))  # R: MutableMapping[str, int]
reveal_type(del_in(real_mutable_mapping, ["a"]))  # R: MutableMapping[str, int]
# set_in / update_in / del_in with list
nested_list: list[int] = [1, 2, 3]
reveal_type(set_in(nested_list, [0], 42))  # R: list[int]
reveal_type(update_in(nested_list, [0], inc))  # R: list[int]
reveal_type(del_in(nested_list, [0]))  # R: list[int]

# -- join_with / merge_with --
dict_pair2: list[dict[str, int]] = [d1, d2]
def add_all(xs: list[int]) -> int: return 0
reveal_type(join_with(add_all, dict_pair2))  # R: dict[str, int]
reveal_type(merge_with(add_all, d1, d2))  # R: dict[str, int]

# -- Extended function protocol in predicates (int, str) --
reveal_type(all(r"\d+", strs))  # R: bool
reveal_type(any(0, int_pairs))  # R: bool

# -- Extended function return type tests --
reveal_type(walk_keys(None, si_dict))  # R: dict[str, int]
reveal_type(walk_values(None, si_dict))  # R: dict[str, int]

# -- Should be errors --
walk(int_to_str, int_list, int_list)  # E: too many arguments
zipdict(123, [1, 2]) # E: not iterable
has_path(nested, 42)  # E: path not iterable

# Extended function type mismatches
walk_keys({1: "a"}, si_dict)  # E: Mapping[int, str] keys don't match str keys
split_keys({1, 2}, d)  # E: Set[int] pred vs str keys
select_keys({1, 2}, d)  # E: Set[int] pred vs str keys
select_values(r"\d+", d)  # E: regex pred vs int values
