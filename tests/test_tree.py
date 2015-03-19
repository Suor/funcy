import ast
from whatever import _

from funcy import rest
from funcy.tree import *


def test_tree_leaves():
    assert tree_leaves([1, 2, [3, [4]], 5]) == [1, 2, 3, 4, 5]
    assert tree_leaves(1) == [1]

    assert tree_leaves(3, follow=_ > 1, children=range) == [0, 1, 0, 1]
    assert tree_leaves([1, [2, [3, 4], 5], 6], children=rest) == [4, 5, 6]
