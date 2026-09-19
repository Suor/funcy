from collections.abc import Callable, Sequence
from contextlib import ContextDecorator as ContextDecorator, contextmanager as contextmanager
from inspect import unwrap as unwrap
from typing import Any, Concatenate, ParamSpec, Protocol, TypeVar, overload
from typing_extensions import TypeForm

from .typing import DecoReturning

__all__ = ['decorator', 'wraps', 'unwrap', 'ContextDecorator', 'contextmanager']

_F = TypeVar('_F', bound=Callable[..., Any])
_P = ParamSpec('_P')    # decorator's own params, the ones after call
_PF = ParamSpec('_PF')  # decorated function params
_RF = TypeVar('_RF')    # what the decorated function returns
_RD = TypeVar('_RD')    # what returning= declares
_RD_co = TypeVar('_RD_co', covariant=True)

class Call:
    """Proxy for decorated function with call arguments saved in attributes."""
    _func: Callable[..., Any]
    _args: tuple[Any, ...]
    _kwargs: dict[str, Any]
    def __init__(self, func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]) -> None: ...
    def __call__(self, *a: Any, **kw: Any) -> Any: ...
    def __getattr__(self, name: str) -> Any: ...

class _Deco(Protocol):
    def __call__(self, func: Callable[_PF, _RF], /) -> Callable[_PF, _RF]: ...

class _DecoFab(Protocol[_P]):
    @overload
    def __call__(self, func: Callable[_PF, _RF], /) -> Callable[_PF, _RF]: ...
    @overload
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _Deco: ...

class _DecoFabTyped(Protocol[_P, _RD_co]):
    @overload
    def __call__(self, func: Callable[_PF, Any], /) -> Callable[_PF, _RD_co]: ...
    @overload
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> DecoReturning[_RD_co]: ...

class _DecoratorReturning(Protocol[_RD_co]):
    def __call__(self, deco: Callable[Concatenate[Call, _P], Any], /) -> _DecoFabTyped[_P, _RD_co]: ...

@overload
def decorator(deco: Callable[Concatenate[Call, _P], Any]) -> _DecoFab[_P]: ...
@overload
def decorator(*, returning: TypeForm[_RD]) -> _DecoratorReturning[_RD]: ...

def wraps(wrapped: _F, assigned: Sequence[str] = ..., updated: Sequence[str] = ...) -> Callable[[Callable[..., Any]], _F]: ...
