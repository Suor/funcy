from collections.abc import Callable
from typing import Any, Generic, TypeVar, overload

__all__ = ['cached_property', 'cached_readonly', 'wrap_prop', 'monkey', 'LazyObject']

_T = TypeVar('_T')
_F = TypeVar('_F', bound=Callable[..., Any])

class cached_property(Generic[_T]):
    fget: Callable[..., _T]
    fset: None
    fdel: None
    def __init__(self, fget: Callable[..., _T]) -> None: ...
    @overload
    def __get__(self, instance: None, owner: type) -> cached_property[_T]: ...
    @overload
    def __get__(self, instance: Any, owner: type) -> _T: ...

class cached_readonly(cached_property[_T]):
    def __set__(self, instance: Any, value: Any) -> None: ...

def wrap_prop(ctx: Any) -> Callable[..., Any]: ...

def monkey(cls: type | Any, name: str | None = ...) -> Callable[[_F], _F]: ...

class LazyObject:
    # Becomes what init builds; no __init__, since mypy would prefer it over a non-instance __new__
    def __new__(cls, init: Callable[[], _T]) -> _T: ...  # type: ignore[misc]
