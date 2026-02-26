from typing import Any, assert_type
from collections.abc import Iterable, Iterator, Mapping, Sequence
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

# Typed collections for join tests (avoid inline literals that ty can't infer)
dict_list: list[dict[str, int]] = [{"a": 1}, {"b": 2}]
int_list_list: list[list[int]] = [[1, 2], [3]]
int_set_list: list[set[int]] = [{1, 2}, {3}]

# Typed functions (not Callable-annotated lambdas — ty can't infer those through overloads)
def pred_true(p: Any) -> bool: return True
def pred_gt0(x: int) -> bool: return x > 0
def pred_gt1(v: int) -> bool: return v > 1
def pred_ne_c(k: str) -> bool: return k != "c"
def pred_eq_a(k: str) -> bool: return k == "a"

# Typed dict for walk_values int/lambda tests
str_to_intlist: dict[str, Sequence[int]] = {"a": [1, 2], "b": [3, 4]}
str_to_int1: dict[str, int] = {"a": 1}

# Typed list for join_with test
dict_pair: list[dict[str, int]] = [si_dict, si_dict2]

# -- merge: with args -> not None; no args -> None --
# FIX: add tests for the above
assert_type(merge(si_dict, si_dict2), dict[str, int])
assert_type(merge(int_list, int_list), list[int])
assert_type(merge(int_set, int_set), set[int])

# -- join: may be None (depends on value) --
assert_type(join(dict_list), dict[str, int] | None)
assert_type(join(int_list_list), list[int] | None)
assert_type(join(int_set_list), set[int] | None)
# Canary: detect when ty starts inferring types of inline list literals
assert_type(join([{"a": 1}, {"b": 2}]), dict[str, int] | None)  # XFAIL[ty]: inline list literal Unknown

# -- walk_keys: Callable transforms keys, values preserved --
def str_key_to_int(k: str) -> int: return ord(k)
assert_type(walk_keys(str_key_to_int, si_dict), dict[int, int])
assert_type(walk_keys(str.upper, si_dict), dict[str, int])
# walk_keys: Canary for ty builtin overload resolution
assert_type(walk_keys(len, si_dict), dict[int, int])  # XFAIL[ty]: len overload not matched
# walk_keys: None = identity
assert_type(walk_keys(None, si_dict), dict[str, int])
# walk_keys: Set = membership -> bool keys
assert_type(walk_keys({"a", "b"}, si_dict), dict[bool, int])
# walk_keys: Mapping = lookup -> mapped key type
key_map: dict[str, int] = {"a": 1, "b": 2}
assert_type(walk_keys(key_map, si_dict), dict[int, int])
# walk_keys: int = itemgetter on sequence keys
seq_key_dict: dict[Sequence[int], int] = {(1, 2): 10, (3, 4): 20}
assert_type(walk_keys(0, seq_key_dict), dict[int, int])
# walk_keys: str/regex = regex finder on keys
assert_type(walk_keys(r"\d+", si_dict), dict[_ReResult | None, int])

# -- walk_values: Callable transforms values, keys preserved --
def int_to_str(v: int) -> str: return str(v)
assert_type(walk_values(int_to_str, si_dict), dict[str, str])
assert_type(walk_values(pred_gt0, str_to_int1), dict[str, bool])
# walk_values: None = identity
assert_type(walk_values(None, si_dict), dict[str, int])
# walk_values: Set = membership -> bool values
assert_type(walk_values({1, 2}, si_dict), dict[str, bool])
# walk_values: int = itemgetter on sequence values
assert_type(walk_values(0, str_to_intlist), dict[str, int])
# walk_values: slice = subsequence of sequence values
assert_type(walk_values(slice(0, 2), str_to_intlist), dict[str, Sequence[int]])
# walk_values: Mapping = lookup -> mapped value type
val_map: dict[int, str] = {1: "one", 2: "two"}
assert_type(walk_values(val_map, si_dict), dict[str, str])
# walk_values: str/regex = regex finder on values
str_dict: dict[str, str] = {"a": "123", "b": "abc"}
assert_type(walk_values(r"\d+", str_dict), dict[str, _ReResult | None])

# -- walk: Callable transforms items --
def int_to_float(x: int) -> float: return float(x)
assert_type(walk(int_to_float, int_list), list[float])
assert_type(walk(int_to_float, int_set), set[float])
# walk: dict uses extended function protocol (returns dict)
assert_type(walk(int_to_str, si_dict), dict[Any, Any])

# -- select: filtering preserves type --
assert_type(select(pred_true, si_dict), dict[str, int])
assert_type(select(pred_gt0, int_list), list[int])
assert_type(select(pred_gt0, int_set), set[int])

# -- select_keys / select_values: dict in, dict out --
d: dict[str, int] = {"a": 1, "b": 2, "c": 3}
assert_type(select_keys(pred_ne_c, d), dict[str, int])
assert_type(select_values(pred_gt1, d), dict[str, int])

# -- compact: preserves type --
assert_type(compact(d), dict[str, int])
maybe_list: list[int | None] = [0, 1, None, 2]
assert_type(compact(maybe_list), list[int | None])

# -- empty: preserves type --
assert_type(empty(d), dict[str, int])
assert_type(empty(int_list), list[int])

# -- iteritems / itervalues --
assert_type(iteritems(d), Iterable[tuple[str, int]])
assert_type(itervalues(d), Iterable[int])

# -- split_keys --
assert_type(split_keys(pred_eq_a, d), tuple[dict[str, int], dict[str, int]])

# -- flip / project / omit --
assert_type(flip(d), dict[int, str])
assert_type(project(d, str_keys), dict[str, int])
assert_type(omit(d, str_keys), dict[str, int])

# -- zipdict: generic key/value types --
assert_type(zipdict(str_keys, int_vals), dict[str, int])
assert_type(zipdict(range(3), str_keys), dict[int, str])

# -- bool-returning functions --
assert_type(is_distinct([1, 2, 3]), bool)
assert_type(is_distinct([1, 2, 3], key=str), bool)
assert_type(all([True, True]), bool)
assert_type(all(lambda x: x > 0, [1, 2, 3]), bool)
assert_type(any([False, True]), bool)
assert_type(any(lambda x: x > 0, [1, 2, 3]), bool)
assert_type(none([False, False]), bool)
assert_type(none(lambda x: x > 0, [1, 2, 3]), bool)
assert_type(one([False, True]), bool)
assert_type(one(lambda x: x > 0, [1, 2, 3]), bool)
assert_type(has_path({"a": {"b": 1}}, ["a", "b"]), bool)

# -- some returns element type --
maybe_ints: list[int | None] = [0, None, 3]
assert_type(some(maybe_ints), int | None)
assert_type(some(pred_gt0, int_list), int | None)

# -- where / lwhere --
records: list[dict[str, Any]] = [{"name": "a", "age": 1}]
assert_type(where(records, name="a"), Iterator[Mapping[str, Any]])
assert_type(lwhere(records, name="a"), list[Mapping[str, Any]])

# -- pluck / lpluck --
assert_type(pluck("name", records), Iterator[Any])
assert_type(lpluck("name", records), list[Any])

# -- pluck_attr / lpluck_attr --
assert_type(pluck_attr("real", [1, 2, 3]), Iterator[Any])
assert_type(lpluck_attr("real", [1, 2, 3]), list[Any])

# -- invoke / linvoke --
assert_type(invoke(["abc", "def"], "upper"), Iterator[Any])
assert_type(linvoke(["abc", "def"], "upper"), list[Any])

# -- zip_values / zip_dicts --
d1: dict[str, int] = {"a": 1, "b": 2}
d2: dict[str, int] = {"a": 3, "b": 4}
assert_type(zip_values(d1, d2), Iterator[tuple[Any, ...]])
assert_type(zip_dicts(d1, d2), Iterator[tuple[Any, tuple[Any, ...]]])

# -- get_in / set_in / update_in / del_in --
nested: dict[str, Any] = {"a": {"b": 1}}
assert_type(get_in(nested, ["a", "b"]), Any)
assert_type(get_lax(nested, ["a", "b"]), Any)
assert_type(has_path(nested, ["a", "b"]), bool)

# -- join_with / merge_with --
dict_pair2: list[dict[str, int]] = [d1, d2]
assert_type(join_with(sum, dict_pair2), dict[str, Any])
assert_type(merge_with(sum, d1, d2), dict[str, Any])

# -- Extended function protocol in predicates (int, str) --
assert_type(all(r"\d+", ["1", "2", "abc"]), bool)
assert_type(any(0, [(1,), (0,)]), bool)

# -- Should be errors --
# FIX: should match actual error messages, or their standartized form
zipdict(123, [1, 2]) # E: not iterable
has_path(nested, 42)  # E: path not iterable
