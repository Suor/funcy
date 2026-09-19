import re
from typing import assert_type
from collections.abc import Callable, Iterator
from funcy import re_iter, re_all, re_find, re_test, re_finder, re_tester, str_join, cut_prefix, cut_suffix

_ReResult = str | tuple[str, ...] | dict[str, str]

# -- re_find --
assert_type(re_find(r"\d+", "abc123"), _ReResult | None)
assert_type(re_test(r"\d+", "abc123"), bool)
assert_type(re_all(r"\d+", "abc123"), list[_ReResult])
assert_type(re_iter(r"\d+", "abc123"), Iterator[_ReResult])

# -- factory functions --
assert_type(re_finder(r"\d+"), Callable[[str], _ReResult | None])
assert_type(re_tester(r"\d+"), Callable[[str], bool])

# -- re with compiled pattern --
pattern = re.compile(r"\d+")
assert_type(re_find(pattern, "abc123"), _ReResult | None)
assert_type(re_test(pattern, "abc123"), bool)

# -- Can't narrow return type based on regex capture groups.
#    Would require a mypy plugin (pyright and ty have no plugin systems).
#    No groups or single group -> ideally str
assert_type(re_find(r"\d+", "abc123"), str | None)  # XFAIL: can't narrow by capture groups
assert_type(re_find(r"(\d+)", "abc123"), str | None)  # XFAIL: can't narrow by capture groups
assert_type(re_all(r"\d+", "abc123"), list[str])  # XFAIL: can't narrow by capture groups
# Multiple groups -> ideally tuple[str, str]
assert_type(re_find(r"(\d+)-(\w+)", "1-a"), tuple[str, str] | None)  # XFAIL: can't narrow by capture groups
assert_type(re_all(r"(\d+)-(\w+)", "1-a 2-b"), list[tuple[str, str]])  # XFAIL: can't narrow by capture groups
# Named groups -> ideally dict[str, str]
assert_type(re_find(r"(?P<num>\d+)", "123"), dict[str, str] | None)  # XFAIL: can't narrow by capture groups

# -- str_join --
assert_type(str_join(", ", [1, 2, 3]), str)
assert_type(str_join([1, 2, 3]), str)

# -- cut_prefix / cut_suffix --
assert_type(cut_prefix("hello world", "hello "), str)
assert_type(cut_suffix("hello world", " world"), str)

# -- Should be errors --
re_find(123, "abc")  # E: wrong regex type
cut_prefix(123, "x")  # E: wrong argument type
