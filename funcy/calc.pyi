from collections.abc import Callable, Mapping
from datetime import timedelta
from typing import Any, TypeVar, overload

__all__ = ['memoize', 'make_lookuper', 'silent_lookuper', 'cache']

_F = TypeVar('_F', bound=Callable[..., Any])
_K = TypeVar('_K')
_V = TypeVar('_V')

class SkipMemory(Exception): ...

@overload
def memoize(func: _F) -> _F: ...
@overload
def memoize(*, key_func: Callable[..., Any]) -> Callable[[_F], _F]: ...

def cache(timeout: int | float | timedelta, *, key_func: Callable[..., Any] | None = ...) -> Callable[[_F], _F]: ...

def make_lookuper(func: Callable[..., Mapping[_K, _V]]) -> Callable[..., _V]: ...
def silent_lookuper(func: Callable[..., Mapping[_K, _V]]) -> Callable[..., _V | None]: ...
