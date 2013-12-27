"""
Rewrite function names to represent Python 3 iterator-by-default interface.
List versions go with l prefix.
"""
from .py2 import *

# colls
del iteritems
zip_values = izip_values; del izip_values
zip_dicts = izip_dicts; del izip_dicts

# seqs
lmap, map = map, imap; del imap
lfilter, filter = filter, ifilter; del ifilter
lremove, remove = remove, iremove; del iremove
lkeep, keep = keep, ikeep; del ikeep
lwithout, without = without, iwithout; del iwithout

lconcat, concat = concat, iconcat; del iconcat
lcat, cat = cat, icat; del icat
lflatten, flatten = flatten, iflatten; del iflatten
lmapcat, mapcat = mapcat, imapcat; del imapcat

ldistinct, distinct = distinct, idistinct; del idistinct
lsplit, split = split, isplit; del isplit
lsplit_at, split_at = split_at, isplit_at; del isplit_at
lsplit_by, split_by = split_by, isplit_by; del isplit_by
lpartition, partition = partition, ipartition; del ipartition
lchunks, chunks = chunks, ichunks; del ichunks
lpartition_by, partition_by = partition_by, ipartition_by; del ipartition_by

lreductions, reductions = reductions, ireductions; del ireductions
lsums, sums = sums, isums; del isums

# py2 re-exports izip, so py3 exports lzip
zip = izip; del izip
def lzip(*seqs):
    return list(zip(*seqs))

# funcs
ljuxt, juxt = juxt, ijuxt; del ijuxt
