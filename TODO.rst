TODO
====

- pipe, stream
- @reraise((Err1, Err2), like=OtherErr)
  with reraise(TypeError, ValueError) as MyError:
      ...
- add delay to @retry
- pre_walk, post_walk
- tree-seq
- children arg to i?flatten
- where_not?
- check using eval in @decorator and @wraps to preserve signature

- partial.func interface or (func, arg1, arg2) extended fns
- invalidate/invalidate_all() to (make|silent)_lookuper

- (log|print)_errors to optionally hide causing call?
- log_* and print_* to optionally hide args?


Docs
----

- cheatsheat
- overview to docs


Or not TODO
-----------

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
