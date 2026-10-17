from collections.abc import Callable, Iterable, Iterator
from typing import Any

__all__ = ['tree_leaves', 'ltree_leaves', 'tree_nodes', 'ltree_nodes']

def tree_leaves(
    root: Any,
    follow: Callable[[Any], bool] = ...,
    children: Callable[[Any], Iterable[Any]] = ...,
) -> Iterator[Any]: ...

def ltree_leaves(
    root: Any,
    follow: Callable[[Any], bool] = ...,
    children: Callable[[Any], Iterable[Any]] = ...,
) -> list[Any]: ...

def tree_nodes(
    root: Any,
    follow: Callable[[Any], bool] = ...,
    children: Callable[[Any], Iterable[Any]] = ...,
) -> Iterator[Any]: ...

def ltree_nodes(
    root: Any,
    follow: Callable[[Any], bool] = ...,
    children: Callable[[Any], Iterable[Any]] = ...,
) -> list[Any]: ...
