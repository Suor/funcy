Funcy
=====

A collection of fancy functional tools focused on practicality.

Inspired by clojure, underscore and my own abstractions. Keep reading to get an overview
or `read the docs <http://funcy.readthedocs.org/>`_.

Works with Python 2.6+, 3.3+ and pypy.


Installation
-------------

::

    pip install funcy


Overview
--------

Just import stuff from funcy to make things happen:

.. code:: python

    from funcy import * # or whatever you need


Merge collections of same type
(works for dicts, sets, lists, tuples, iterators and even strings):

.. code:: python

    merge(coll1, coll2, coll3, ...)
    join(colls)


Walk through collection, creating it's transform (like map but preserves type):

.. code:: python

    walk(str.upper, {'a', 'b'})            # {'A', 'B'}
    walk(reversed, {'a': 1, 'b': 2})       # {1: 'a', 2: 'b'}
    walk_keys(double, {'a': 1, 'b': 2})    # {'aa': 1, 'bb': 2}
    walk_values(inc, {'a': 1, 'b': 2})     # {'a': 2, 'b': 3}


Select a part of collection:

.. code:: python

    select(even, {1,2,3,10,20})                  # {2,10,20}
    select(r'^a', ('a','b','ab','ba'))           # ('a','ab')
    select_keys(callable, {str: '', None: None}) # {str: ''}
    compact({2, None, '', 0})                    # {2,'',0}


Test collection contents:

.. code:: python

    all(callable, [abs, open, int]) # True
    all(even, [1, 2, 5])            # False
    any(even, [1, 2, 5])            # True
    none(even, [1, 2, 5])           # False
    is_distinct('adbec')            # True


Or search for something:

.. code:: python

    some(even, [1, 2, 5])      # 2
    some([0, '', -1, None, 2]) # -1


More tools for mappings:

.. code:: python

    flip({'a': 1, 'b': 2})                        # {1: 'a', 2: 'b'}
    project({'a': 1, 'b': 2, 'c': 3}, ['a', 'c']) # {'a': 1, 'c': 3}
    pluck('a', [{'a': 1, 'b': 2}, {'a': 10}])     # [1, 10]
    where([{'a': 1, 'b': 2}, {'a': 10}], a=1)     # [{'a': 1, 'b': 2}]


Manipulate functions:

.. code:: python

    partial(add, 1)                # inc
    curry(add)(1)(2)               # 3
    compose(inc, double)(10)       # 21
    complement(even)               # odd
    map(iffy(len), ['ab',None,'c'] # [2,None,1]
    iffy(callable, caller())(val)  # val() if callable(val) else val


Easy decorators:

.. code:: python

    @decorator
    def log(call):
        print call._func.__name__, call._args
        return call()


Work with sequences:

.. code:: python

    take(4, iterate(double, 1)) # [1, 2, 4, 8]
    first(drop(3, count(10)))   # 13

    remove(even, [1, 2, 3])     # [1, 3]
    concat([1, 2], [5, 6])      # [1, 2, 5, 6]
    cat(map(range, range(4)))   # [0, 0, 1, 0, 1, 2]
    mapcat(range, range(4)))    # same
    distinct('abacbdd')         # list('abcd')

    split(odd, range(5))        # [[1, 3], [0, 2, 4]]
    split_at(2, range(5))       # [[0, 1], [2, 3, 4]]
    group_by(mod3, range(5))    # {0: [0, 3], 1: [1, 4], 2: [2]}

    partition(2, range(5))      # [[0, 1], [2, 3]]
    chunks(2, range(5))         # [[0, 1], [2, 3], [4]]
    partition(2, 1, range(4))   # [[0, 1], [1, 2], [2, 3]]
    chunks(2, 1, range(4))      # [[0, 1], [1, 2], [2, 3], [3]]


And `many more <http://funcy.readthedocs.org/>`_.


How you can help
----------------

Bring your ideas and/or code that can make functional python more fun.


TODO
----

- create cheatsheet html
- reject*(), disjoint*() collections
- merge_with(), zip_with()
- starfilter()
- one argument select*()? other name?
- reversed() to work with iterators?
- vector chained boolean test (like perl 6 [<])
