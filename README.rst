Funcy
=====

A collection of fancy functional tools. Manipulate your functions and data with ease.

Inspired by clojure, underscore and my own abstractions. Keep reading to get an overview
or `read the docs <http://funcy.readthedocs.org/>`_ (not complete yet).


Installation
-------------

::

    pip install funcy


Overview
--------

Just import stuff from funcy to make things happen::

    from funcy import * # or whatever you need


Merge collections of same type
(works for dicts, sets, lists, tuples, iterators and even strings)::

    merge(coll1, coll2, coll3, ...)
    join(colls)


Walk through collection, creating it's transform (like map but preserves type)::

    walk(str.upper, {'a', 'b'})            # {'A', 'B'}
    walk(reversed, {'a': 1, 'b': 2})       # {1: 'a', 2: 'b'}
    walk_keys(double, {'a': 1, 'b': 2})    # {'aa': 1, 'bb': 2}
    walk_values(inc, {'a': 1, 'b': 2})     # {'a': 2, 'b': 3}


Select a part of collection::

    select(even, {1,2,3,10,20})                  # {2,10,20}
    select(re_tester('^a'), ('a','b','ab','ba')) # ('a','ab')
    select_keys(callable, {str: '', None: None}) # {str: ''}


Test collection contents::

    all(callable, [abs, open, int]) # True
    all(even, [1, 2, 5])            # False
    any(even, [1, 2, 5])            # True
    none(even, [1, 2, 5])           # False


Or search for something::

    some(even, [1, 2, 5])      # 2
    some([0, '', -1, None, 2]) # -1


More tools for mappings::

    flip({'a': 1, 'b': 2})                        # {1: 'a', 2: 'b'}
    project({'a': 1, 'b': 2, 'c': 3}, ['a', 'c']) # {'a': 1, 'c': 3}


Manipulate functions::

    partial(add, 1)                # inc
    curry(add)(1)(2)               # 3
    compose(inc, double)(10)       # 21
    complement(even)               # odd
    map(iffy(len), ['ab',None,'c'] # [2,None,1]
    iffy(callable, caller())(val)  # val() if callable(val) else val


Easy decorators::

    @decorator
    def log(call):
        print call.func.__name__, call.args
        return call()


Work with sequences::

    take(4, iterate(double, 1)) # [1, 2, 4, 8]
    first(drop(3, count(10)))   # 13

    remove(even, [1, 2, 3])     # [1, 3]
    concat([1, 2], [5, 6])      # [1, 2, 5, 6]
    cat(map(range, range(4)))   # [0, 0, 1, 0, 1, 2]
    mapcat(range, range(4)))    # same
    distinct('abacbdd')         # list('abcd')

    split(2, range(5))          # [[0, 1], [2, 3, 4]]
    split(odd, range(5))        # [[1, 3], [0, 2, 4]]
    groupby(mod2, range(5))     # {0: [0, 2, 4], 1: [1, 3]}

    partition(2, range(5))      # [[0, 1], [2, 3]]
    chunks(2, range(5))         # [[0, 1], [2, 3], [4]]
    partition(2, 1, range(4))   # [[0, 1], [1, 2], [2, 3]]
    chunks(2, 1, range(4))      # [[0, 1], [1, 2], [2, 3], [3]]


And many more, see tests and source.


How you can help
----------------

Bring your ideas and/or code that can make functional python more fun.


TODO
----

- create cheatsheet html
- write docs
- vector chained boolean test (like perl 6 [<])
- lazy, lazy_seq, lazy_dict
- make better or get rid of generator version of @decorator
- reject*(), split collections
- merge_with(), join_with()
