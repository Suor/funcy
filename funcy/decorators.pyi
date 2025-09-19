from functools import _Wrapped, _Wrapper, wraps as _wraps
from typing import Callable, Concatenate, Generic, ParamSpec, Protocol, TypeAlias, TypeVar, Any
from typing import overload, TYPE_CHECKING, assert_type
from _typeshed import Incomplete
from contextlib import ContextDecorator as ContextDecorator, contextmanager as contextmanager
from inspect import unwrap as unwrap

__all__ = ['decorator', 'wraps', 'unwrap', 'ContextDecorator', 'contextmanager']

_PD = ParamSpec('_PD')
_PF = ParamSpec('_PF')
_RD = TypeVar('_RD')
_RF = TypeVar('_RF')
_T = TypeVar('_T')
_T_co = TypeVar('_T_co', covariant=True)


class _MyWrapped(_Wrapped[_PF, _RF, _PD, _RD]):
    __original__: Callable[_PF, _RF]

class _W(Generic[_PF, _RF, _PD, _RD]):
    __original__: Callable[_PF, _RF]
    __wrapped__: Callable[_PF, _RF]
    def __call__(self, *args: _PD.args, **kwargs: _PD.kwargs) -> _RD: ...
    __name__: str
    __qualname__: str

class _MyWrapper(Generic[_PD, _RD]):
    def __call__(self, f: Callable[_PF, _RF]) -> _MyWrapped[_PD, _RD, _PF, _RF]: ...

class _Deco(_MyWrapped[_PD, _RD, ..., ...]):
    _func: Callable[_PD, _RD]
    _args: tuple[Incomplete, ...]
    _kwargs: dict[str, Incomplete]
    # Decorator replaces return type with its wrapper's one and may alter params too
    def __call__(self, f: Callable[_PF, _RF]) -> _MyWrapped[_PF, _RF, ..., _RD]: ...  # type: ignore[override]

class _DecoFab(_MyWrapped[_PD, _RD, _PD, _Deco[_PD, _RD]]):
    ...

class _DecoOrFab(_DecoFab[_PD, _RD]):
    @overload  # type: ignore[override]
    def __call__(self, f: Callable[_PF, _RF], /) -> _W[_PF, _RF, _PF, _RD]: ...
    @overload
    def __call__(self, **kwargs) -> _Deco[_PD, _RD]: ...


@overload
def decorator(deco: Callable[[Call], _RD]) -> _DecoOrFab[[], _RD]: ...
# mypy mistakenly thinks this second one is useless
# @overload
# def decorator(deco: Callable[Concatenate[Call, _PD], _RD]) -> _DecoFab[_PD, _RD]: ...
@overload
def decorator(deco: Callable[Concatenate[Call, _T, _PD], _RD]) -> _DecoFab[Concatenate[_T, _PD], _RD]: ...
# @overload
# def decorator(deco: _SingleCall[_RD]) -> Callable[..., _RD]: ...

def return_x(call) -> int:
    return call.x
reveal_type(return_x)
reveal_type(decorator(return_x))


def f() -> float:
    return 0.1

def add(call: Call, *, n=1) -> str:
    ...
reveal_type(add)
reveal_type(decorator(add))
reveal_type(decorator(add)(f))
reveal_type(decorator(add)(f).__call__)
reveal_type(decorator(add)(n=2))
reveal_type(decorator(add)(n=2)(f))
# assert_type(add, _SingleCall)

class Call:  # TODO: parametrize this, will allow to parametrize _Deco by func signature too
    _func: Callable
    _args: tuple[Incomplete, ...]
    _kwargs: dict[str, Incomplete]
    def __init__(self, func, args, kwargs) -> None: ...
    def __call__(self, *a, **kw): ...
    def __getattr__(self, name): ...

def _fix_return(func: Callable[_PD, _Wrapper[_PF, _RF]]) -> Callable[_PD, _MyWrapper[_PF, _RF]]: ...
wraps = _fix_return(_wraps)
