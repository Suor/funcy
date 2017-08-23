"""
Rewrite function names to represent Python 3 iterator-by-default interface.
List versions go with l prefix.
"""
import sys

from . import py2
from .py2 import *  # noqa
from .py2 import __all__

# NOTE: manually renaming these to make PyCharm happy.
#       Not renaming iversions manually to not shade original definition.
#       Why it's shaded by rename? PyCharm only knows...
from .py2 import (map as lmap, filter as lfilter, remove as lremove, keep as lkeep,  # noqa
    without as lwithout, concat as lconcat, cat as lcat, flatten as lflatten, mapcat as lmapcat,
    distinct as ldistinct, split as lsplit, split_at as lsplit_at, split_by as lsplit_by,
    partition as lpartition, chunks as lchunks, partition_by as lpartition_by,
    reductions as lreductions, sums as lsums, juxt as ljuxt,
    tree_leaves as ltree_leaves, tree_nodes as ltree_nodes,
    where as lwhere, pluck as lpluck, pluck_attr as lpluck_attr, invoke as linvoke)


RENAMES = {}
for name in ('map', 'filter', 'remove', 'keep', 'without', 'concat', 'cat', 'flatten',
             'mapcat', 'distinct', 'split', 'split_at', 'split_by', 'partition', 'chunks',
             'partition_by', 'reductions', 'sums', 'juxt',
             'tree_leaves', 'tree_nodes',
             'where', 'pluck', 'pluck_attr', 'invoke'):
    RENAMES['i' + name] = name
    RENAMES[name] = 'l' + name
RENAMES['izip_values'] = 'zip_values'
RENAMES['izip_dicts'] = 'zip_dicts'


# HACK: list concat instead of .append() to not trigger PyCharm
__all__ = [RENAMES.get(name, name) for name in __all__ if name != 'izip'] + ['lzip']


py3 = sys.modules[__name__]
for old, new in RENAMES.items():
    setattr(py3, new, getattr(py2, old))
setattr(py3, 'lzip', py2.zip)
