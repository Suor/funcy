"""Protocols to cast a decorator to when it alters what it wraps."""
from collections.abc import Callable
from typing import Any, ParamSpec, Protocol, TypeVar

__all__ = ['DecoReturning']

_PF = ParamSpec('_PF')
_R_co = TypeVar('_R_co', covariant=True)


class DecoReturning(Protocol[_R_co]):
    """A decorator keeping the wrapped params and only changing the return type."""
    def __call__(self, func: Callable[_PF, Any], /) -> Callable[_PF, _R_co]:
        ...
