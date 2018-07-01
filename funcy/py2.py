"""
Rewrite function names to represent Python 2 list-by-default interface.
Iterator versions go with i prefix.
"""
import sys

from . import py3
from .py3 import *  # noqa
from .py3 import __all__
from .cross import izip  # noqa, reexport

# # NOTE: manually renaming these to make PyCharm happy.
# #       Not renaming iversions manually to not shade original definition.
# #       Why it's shaded by rename? PyCharm only knows...
# from .py3 import (lmap as map, lfilter as filter, lremove as remove, lkeep as keep,  # noqa
#     lwithout as without, lconcat as concat, lcat as cat, lflatten as flatten, lmapcat as mapcat,
#     ldistinct as distinct, lsplit as split, split_at as lsplit_at, split_by as lsplit_by,
#     partition as lpartition, chunks as lchunks, partition_by as lpartition_by,
#     reductions as lreductions, sums as lsums, juxt as ljuxt,
#     tree_leaves as ltree_leaves, tree_nodes as ltree_nodes,
#     where as lwhere, pluck as lpluck, pluck_attr as lpluck_attr, invoke as linvoke)


RENAMES = {}
for name in ('map', 'filter', 'remove', 'keep', 'without', 'concat', 'cat', 'flatten',
             'mapcat', 'distinct', 'split', 'split_at', 'split_by', 'partition', 'chunks',
             'partition_by', 'reductions', 'sums', 'juxt',
             'tree_leaves', 'tree_nodes',
             'where', 'pluck', 'pluck_attr', 'invoke'):
    RENAMES['l' + name] = name
    RENAMES[name] = 'i' + name
RENAMES['zip_values'] = 'izip_values'
RENAMES['zip_dicts'] = 'izip_dicts'


# HACK: list concat instead of .append() to not trigger PyCharm
__all__ = [RENAMES.get(name, name) for name in __all__ if name != 'lzip'] + ['izip']

py2 = sys.modules[__name__]
for old, new in RENAMES.items():
    setattr(py2, new, getattr(py3, old))
