from typing import Callable, Generic, ParamSpec, Protocol, TypeVar, overload

_PD = ParamSpec('_PD')
_PF = ParamSpec('_PF')
_RD = TypeVar('_RD')
_RF = TypeVar('_RF')

# from functools import _Wrapped as _W
class _W(Generic[_PF, _RF, _PD, _RD]):
    ...

class _DecoOrFab(Protocol[_PD, _RD]):
    @overload
    def __call__(self, f: Callable[_PF, _RF]) -> _W[_PF, _RF, ..., _RD]: ...
    @overload
    def __call__(self, **kwargs) -> _W[_PD, _RD, ..., ...]: ...
