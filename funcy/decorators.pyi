from collections.abc import Callable, Sequence
from contextlib import ContextDecorator as ContextDecorator, contextmanager as contextmanager
from inspect import unwrap as unwrap
from typing import Any, TypeVar, overload

__all__ = ['decorator', 'wraps', 'unwrap', 'ContextDecorator', 'contextmanager']

_F = TypeVar('_F', bound=Callable[..., Any])

class Call:
    """Proxy for decorated function with call arguments saved in attributes."""
    _func: Callable[..., Any]
    _args: tuple[Any, ...]
    _kwargs: dict[str, Any]
    def __init__(self, func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> None: ...
    def __call__(self, *a: Any, **kw: Any) -> Any: ...
    def __getattr__(self, name: str) -> Any: ...

class _Decorator:
    """Result of @decorator: can be used as decorator or called with args to create one."""
    @overload
    def __call__(self, __func: _F) -> _F: ...
    @overload
    def __call__(self, *args: Any, **kwargs: Any) -> _Decorator: ...

def decorator(deco: Callable[..., Any]) -> _Decorator: ...

def wraps(wrapped: Callable[..., Any], assigned: Sequence[str] = ..., updated: Sequence[str] = ...) -> Callable[[_F], _F]: ...
