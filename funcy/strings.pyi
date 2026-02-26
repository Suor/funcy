import re
from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeAlias

__all__ = ['re_iter', 're_all', 're_find', 're_finder', 're_test', 're_tester',
           'str_join',
           'cut_prefix', 'cut_suffix']

_re_type: type

# Return type of regex match operations depends on capture groups in the pattern:
#   no groups       -> str
#   1 unnamed group -> str
#   N unnamed groups -> tuple[str, ...]
#   named groups    -> dict[str, str]
# We can't detect group count from the pattern type, so we use a union.
_ReResult: TypeAlias = str | tuple[str, ...] | dict[str, str]

def re_iter(regex: str | re.Pattern[str], s: str, flags: int = ...) -> Iterator[_ReResult]: ...
def re_all(regex: str | re.Pattern[str], s: str, flags: int = ...) -> list[_ReResult]: ...
def re_find(regex: str | re.Pattern[str], s: str, flags: int = ...) -> _ReResult | None: ...
def re_test(regex: str | re.Pattern[str], s: str, flags: int = ...) -> bool: ...

def re_finder(regex: str | re.Pattern[str], flags: int = ...) -> Callable[[str], _ReResult | None]: ...
def re_tester(regex: str | re.Pattern[str], flags: int = ...) -> Callable[[str], bool]: ...

def str_join(sep: str | Iterable[Any], seq: Iterable[Any] = ...) -> str: ...

def cut_prefix(s: str, prefix: str) -> str: ...
def cut_suffix(s: str, suffix: str) -> str: ...
