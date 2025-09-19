from functools import _Wrapped
from typing import Callable, Generic, ParamSpec, Protocol, TypeAlias, TypeVar, Any, overload
from _typeshed import Incomplete

__all__ = ['memoize', 'make_lookuper', 'silent_lookuper', 'cache']

class SkipMemory(Exception): ...

_P = ParamSpec('_P')
_R = TypeVar('_R')


class _MemoryWrapped(_Wrapped[_P, _R, _P, _R]):
    memory: CacheMemory
    def invalidate(self, *args: _P.args, **kwargs: _P.kwargs) -> None: ...
    def invalidate_all(self) -> None: ...

class _MemoryDeco:
    # _func: Callable[_PD, _RD]
    # _args: tuple[Incomplete, ...]
    # _kwargs: dict[str, Incomplete]
    # Decorator replaces return type with its wrapper's one and may alter params too
    def __call__(self, func: Callable[_P, _R], /) -> _MemoryWrapped[_P, _R]: ...


@overload
def memoize(func: Callable[_P, _R], /) -> _MemoryWrapped[_P, _R]: ...
@overload
def memoize(*, key_func: Incomplete | None = None) -> _MemoryDeco: ...

memoize.skip: type[SkipMemory]


def cache(timeout, *, key_func: Incomplete | None = None) -> _MemoryDeco: ...

class CacheMemory(dict):
    timeout: Incomplete
    # def __init__(self, timeout) -> None: ...
    # def __setitem__(self, key, value) -> None: ...
    # def __getitem__(self, key): ...
    def expire(self) -> None: ...
    def clear(self) -> None: ...

make_lookuper: Incomplete
silent_lookuper: Incomplete
