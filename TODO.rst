TODO
====

- count_by(identity, ...) shortcut (count_eq? count_items? frequencies?)
  Counter?

- @reraise((Err1, Err2), like=OtherErr)
  with reraise(TypeError, ValueError) as MyError:
      ...
- pre_walk, post_walk
- tree-seq
- where_not?

- invalidate/invalidate_all() to (make|silent)_lookuper

- decorators with optional arguments?
- (log|print)_errors to optionally hide causing call?
- log_* and print_* to optionally hide args?


Or not TODO
-----------

- partial.func interface or (func, arg1, arg2) extended fns
- padding to chunks
- reject*(), disjoint*() collections
- zip_with = map(f, izip(seqs))
- starfilter()
- one argument select*()? other name?
- reversed() to work with iterators?
- vector chained boolean test (like perl 6 [<])


Unknown future
--------------

- cython implementation? separate - cyfuncy? fallback transparently?
- funcyx?
