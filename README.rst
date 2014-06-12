Funcy |Build Status|
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
    compact({2, None, 1, 0})                     # {1,2}


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


Manipulate functions:

.. code:: python

    partial(add, 1)           # inc
    curry(add)(1)(2)          # 3
    compose(inc, double)(10)  # 21
    complement(even)          # odd
    all_fn(isa(int), even)    # is_even_int

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

    split(odd, range(5))        # ([1, 3], [0, 2, 4])
    split_at(2, range(5))       # ([0, 1], [2, 3, 4])
    group_by(mod3, range(5))    # {0: [0, 3], 1: [1, 4], 2: [2]}

    partition(2, range(5))      # [[0, 1], [2, 3]]
    chunks(2, range(5))         # [[0, 1], [2, 3], [4]]
    partition(2, 1, range(4))   # [[0, 1], [1, 2], [2, 3]]
    chunks(2, 1, range(4))      # [[0, 1], [1, 2], [2, 3], [3]]


Manipulate flow:

.. code:: python

    walk_values(silent(int), {'a': '1', 'b': 'no'})
    # => {'a': 1, 'b': None}

    @once
    def initialize():
        # ...

    with suppress(OSError):
        os.remove('some.file')

    @ignore(ErrorRateExceeded)
    @limit_error_rate(fails=5, timeout=60)
    def some_unreliable_action(...):
        # ...


And `many more <http://funcy.readthedocs.org/>`_.


.. |Build Status| image:: https://travis-ci.org/Suor/funcy.svg?branch=master
   :target: https://travis-ci.org/Suor/funcy
