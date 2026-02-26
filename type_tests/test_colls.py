from typing import Any, assert_type
from collections.abc import Iterable, Iterator, Mapping
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

# -- merge: with args -> not None; no args -> None --
assert_type(merge({"a": 1}, {"b": 2}), dict[str, int])  # XFAIL[ty]: Unknown TypeVars
assert_type(merge([1, 2], [3, 4]), list[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(merge({1, 2}, {3}), set[int])  # XFAIL[ty]: Unknown TypeVars

# -- join: may be None (depends on value) --
assert_type(join([{"a": 1}, {"b": 2}]), dict[str, int] | None)  # XFAIL[ty]: Unknown TypeVars
assert_type(join([[1, 2], [3]]), list[int] | None)  # XFAIL[ty]: Unknown TypeVars
assert_type(join([{1, 2}, {3}]), set[int] | None)  # XFAIL[ty]: Unknown TypeVars

# -- walk_keys: f transforms keys, values preserved --
assert_type(walk_keys(str.upper, {"a": 1}), dict[str, int])  # XFAIL[ty]: Unknown TypeVars
assert_type(walk_keys(len, {"abc": 1}), dict[int, int])  # XFAIL[ty]: Unknown TypeVars
# walk_keys: None = identity
assert_type(walk_keys(None, {"a": 1}), dict[str, int])  # XFAIL[ty]: Unknown TypeVars
# walk_keys: Set = membership -> bool keys
assert_type(walk_keys({"a", "b"}, {"a": 1, "c": 2}), dict[bool, int])  # XFAIL[ty]: Unknown TypeVars
# walk_keys: Mapping = lookup -> mapped key type
key_map: dict[str, int] = {"a": 1, "b": 2}
assert_type(walk_keys(key_map, {"a": 10}), dict[int, int])  # XFAIL[ty]: Unknown TypeVars

# -- walk_values: f transforms values, keys preserved --
assert_type(walk_values(str, {"a": 1}), dict[str, str])  # XFAIL[ty]: Unknown TypeVars
assert_type(walk_values(lambda v: v > 0, {"a": 1}), dict[str, bool])  # XFAIL: mypy can't infer lambda return through overload
# walk_values: None = identity
assert_type(walk_values(None, {"a": 1}), dict[str, int])  # XFAIL[ty]: Unknown TypeVars
# walk_values: Set = membership -> bool values
assert_type(walk_values({1, 2}, {"a": 1, "b": 3}), dict[str, bool])  # XFAIL[ty]: Unknown TypeVars
# walk_values: int = itemgetter on sequence values
assert_type(walk_values(0, {"a": [1, 2], "b": [3, 4]}), dict[str, int])  # XFAIL[ty]: Unknown TypeVars
# walk_values: Mapping = lookup -> mapped value type
val_map: dict[int, str] = {1: "one", 2: "two"}
assert_type(walk_values(val_map, {"a": 1, "b": 2}), dict[str, str])  # XFAIL[ty]: Unknown TypeVars

# -- walk: f transforms items --
assert_type(walk(str, [1, 2, 3]), list[str])  # XFAIL[ty]: Unknown TypeVars
assert_type(walk(str, {1, 2, 3}), set[str])  # XFAIL[ty]: Unknown TypeVars

# -- select: filtering preserves type --
assert_type(select(lambda p: True, {"a": 1}), dict[str, int])  # XFAIL[ty]: Unknown TypeVars
assert_type(select(lambda x: x > 0, [1, 2, 3]), list[int])  # XFAIL[ty]: Unknown TypeVars
assert_type(select(lambda x: x > 0, {1, 2, 3}), set[int])  # XFAIL[ty]: Unknown TypeVars

# -- select_keys / select_values: dict in, dict out --
d = {"a": 1, "b": 2, "c": 3}
assert_type(select_keys(lambda k: k != "c", d), dict[str, int])  # XFAIL[ty]: Unknown TypeVars
assert_type(select_values(lambda v: v > 1, d), dict[str, int])  # XFAIL[ty]: Unknown TypeVars

# -- compact: preserves type --
assert_type(compact(d), dict[str, int])  # XFAIL[ty]: Unknown TypeVars
assert_type(compact([0, 1, None, 2]), list[int | None])  # XFAIL[ty]: Unknown TypeVars

# -- empty: preserves type --
assert_type(empty(d), dict[str, int])  # XFAIL[ty]: Unknown TypeVars
assert_type(empty([1, 2]), list[int])  # XFAIL[ty]: Unknown TypeVars

# -- iteritems / itervalues --
assert_type(iteritems(d), Iterable[tuple[str, int]])  # XFAIL[ty]: Unknown TypeVars
assert_type(itervalues(d), Iterable[int])  # XFAIL[ty]: Unknown TypeVars

# -- split_keys --
assert_type(split_keys(lambda k: k == "a", d), tuple[dict[str, int], dict[str, int]])  # XFAIL[ty]: Unknown TypeVars

# -- flip / project / omit --
assert_type(flip({"a": 1, "b": 2}), dict[int, str])  # XFAIL[ty]: Unknown TypeVars
assert_type(project(d, ["a", "b"]), dict[str, int])  # XFAIL[ty]: Unknown TypeVars
assert_type(omit(d, ["c"]), dict[str, int])  # XFAIL[ty]: Unknown TypeVars

# -- zipdict: generic key/value types --
assert_type(zipdict(["a", "b"], [1, 2]), dict[str, int])  # XFAIL[ty]: Unknown TypeVars
assert_type(zipdict(range(3), ["x", "y", "z"]), dict[int, str])  # XFAIL[ty]: Unknown TypeVars

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
assert_type(some([0, None, 3]), int | None)  # XFAIL[ty]: Unknown TypeVars
assert_type(some(lambda x: x > 0, [1, 2, 3]), int | None)  # XFAIL[ty]: Unknown TypeVars

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
d1 = {"a": 1, "b": 2}
d2 = {"a": 3, "b": 4}
assert_type(zip_values(d1, d2), Iterator[tuple[Any, ...]])
assert_type(zip_dicts(d1, d2), Iterator[tuple[Any, tuple[Any, ...]]])

# -- get_in / set_in / update_in / del_in --
nested: dict[str, Any] = {"a": {"b": 1}}
assert_type(get_in(nested, ["a", "b"]), Any)
assert_type(get_lax(nested, ["a", "b"]), Any)
assert_type(has_path(nested, ["a", "b"]), bool)

# -- join_with / merge_with --
assert_type(join_with(sum, [d1, d2]), dict[str, Any])  # XFAIL[ty]: Unknown TypeVars
assert_type(merge_with(sum, d1, d2), dict[str, Any])  # XFAIL[ty]: Unknown TypeVars

# -- Extended function protocol in predicates (int, str) --
assert_type(all(r"\d+", ["1", "2", "abc"]), bool)
assert_type(any(0, [(1,), (0,)]), bool)

# -- Should be errors --
# FIX: should match actual error messages, or their standartized form
zipdict(123, [1, 2]) # E: not iterable
has_path(nested, 42)  # E: path not iterable
