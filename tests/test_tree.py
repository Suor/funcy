from whatever import _

from funcy import rest
from funcy.tree import *


def test_tree_leaves():
    assert ltree_leaves([1, 2, [3, [4]], 5]) == [1, 2, 3, 4, 5]
    assert ltree_leaves(1) == [1]

    assert ltree_leaves(3, follow=_ > 1, children=range) == [0, 1, 0, 1]
    assert ltree_leaves([1, [2, [3, 4], 5], 6], children=rest) == [4, 5, 6]


def test_tree_nodes():
    assert ltree_nodes([1, 2, [3, [4]], 5]) == [
        [1, 2, [3, [4]], 5],
        1, 2,
        [3, [4]], 3, [4], 4,
        5
    ]
    assert ltree_nodes(1) == [1]
    assert ltree_nodes(3, follow=_ > 1, children=range) == [3, 0, 1, 2, 0, 1]


def test_tree_keys():
    assert ltree_keys({"a": 1}) == [["a"]]
    assert ltree_keys({"a": 1, "b": 2}) == [['b'], ['a']]
    assert ltree_keys({"a": {"a1": 3}, "b": 2}) == [['b'], ['a'], ['a', 'a1']]
    assert ltree_keys({}) == []
