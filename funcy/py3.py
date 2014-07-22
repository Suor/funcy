"""
Rewrite function names to represent Python 3 iterator-by-default interface.
List versions go with l prefix.
"""
import sys

from . import py2
from .py2 import *
from .py2 import __all__
from .colls import iwhere as where, ipluck as pluck, iinvoke as invoke


RENAMES = {}
for name in ('map', 'filter', 'remove', 'keep', 'without', 'concat', 'cat', 'flatten',
             'mapcat', 'distinct', 'split', 'split_at', 'split_by', 'partition', 'chunks',
             'partition_by', 'reductions', 'sums', 'juxt'):
    RENAMES['i' + name] = name
    RENAMES[name] = 'l' + name
RENAMES['izip_values'] = 'zip_values'
RENAMES['izip_dicts'] = 'zip_dicts'


__all__ = [RENAMES.get(name, name) for name in __all__ if name != 'izip']
__all__.append('lzip')


py3 = sys.modules[__name__]
for old, new in RENAMES.items():
    setattr(py3, new, getattr(py2, old))
setattr(py3, 'lzip', py2.zip)
