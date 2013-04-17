from collections import Mapping, Sequence, Iterator, Iterable


__all__ = ('isa', 'is_mapping', 'is_seq', 'is_seqcoll', 'is_list',
           'iterable', 'is_iter')


def isa(*types):
    return lambda x: isinstance(x, types)

is_mapping = isa(Mapping)
is_seq = isa(Sequence)
is_seqcoll = isa(list, tuple)
is_list = isa(list)

iterable = isa(Iterable)
is_iter = isa(Iterator, xrange)
