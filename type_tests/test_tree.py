from typing import Any, assert_type
from collections.abc import Iterator
from funcy import tree_leaves, ltree_leaves, tree_nodes, ltree_nodes

nested = [1, [2, [3, 4]], [5]]

# -- tree_leaves --
assert_type(tree_leaves(nested), Iterator[Any])

# -- ltree_leaves --
assert_type(ltree_leaves(nested), list[Any])

# -- tree_nodes --
assert_type(tree_nodes(nested), Iterator[Any])

# -- ltree_nodes --
assert_type(ltree_nodes(nested), list[Any])

# -- With custom follow/children --
assert_type(tree_leaves(nested, follow=lambda x: isinstance(x, list)), Iterator[Any])
assert_type(tree_leaves(nested, follow=lambda x: isinstance(x, list), children=iter), Iterator[Any])

# -- Should be errors --
tree_leaves(nested, follow="not a callable")  # E: wrong argument type
tree_leaves(nested, children="not a callable")  # E: wrong argument type
