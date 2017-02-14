Funcy |Build Status| |Gitter|
=====

A collection of fancy functional tools focused on practicality.

Inspired by clojure, underscore and my own abstractions. Keep reading to get an overview
or `read the docs <http://funcy.readthedocs.org/>`_.
Or jump directly to `cheatsheet <http://funcy.readthedocs.io/en/stable/cheatsheet.html>`_.

Works with Python 2.6+, 3.3+ and pypy.


Installation
-------------

::

    pip install funcy


Overview
--------------

Import stuff from funcy to make things happen:

.. code:: python

    from funcy import whatever, you, need


Merge collections of same type
(works for dicts, sets, lists, tuples, iterators and even strings):

.. code:: python

    merge(coll1, coll2, coll3, ...)
    join(colls)
    merge_with(sum, dict1, dict2, ...)


Walk through collection, creating its transform (like map but preserves type):

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


Manipulate sequences:

.. code:: python

    take(4, iterate(double, 1)) # [1, 2, 4, 8]
    first(drop(3, count(10)))   # 13

    remove(even, [1, 2, 3])     # [1, 3]
    concat([1, 2], [5, 6])      # [1, 2, 5, 6]
    cat(map(range, range(4)))   # [0, 0, 1, 0, 1, 2]
    mapcat(range, range(4))     # same
    flatten(nested_structure)   # flat_list
    distinct('abacbdd')         # list('abcd')

    split(odd, range(5))        # ([1, 3], [0, 2, 4])
    split_at(2, range(5))       # ([0, 1], [2, 3, 4])
    group_by(mod3, range(5))    # {0: [0, 3], 1: [1, 4], 2: [2]}

    partition(2, range(5))      # [[0, 1], [2, 3]]
    chunks(2, range(5))         # [[0, 1], [2, 3], [4]]
    pairwise(range(5))          # iter: [0, 1], [1, 2], ...


And functions:

.. code:: python

    partial(add, 1)             # inc
    curry(add)(1)(2)            # 3
    compose(inc, double)(10)    # 21
    complement(even)            # odd
    all_fn(isa(int), even)      # is_even_int

    one_third = rpartial(operator.div, 3.0)
    has_suffix = rcurry(str.endswith)


Create decorators easily:

.. code:: python

    @decorator
    def log(call):
        print call._func.__name__, call._args
        return call()


Abstract control flow:

.. code:: python

    walk_values(silent(int), {'a': '1', 'b': 'no'})
    # => {'a': 1, 'b': None}

    @once
    def initialize():
        "..."

    with suppress(OSError):
        os.remove('some.file')

    @ignore(ErrorRateExceeded)
    @limit_error_rate(fails=5, timeout=60)
    @retry(tries=2, errors=(HttpError, ServiceDown))
    def some_unreliable_action(...):
        "..."

    class MyUser(AbstractBaseUser):
        @cached_property
        def public_phones(self):
            return self.phones.filter(public=True)


Ease debugging:

.. code:: python

    squares = {tap(x, 'x'): tap(x * x, 'x^2') for x in [3, 4]}
    # x: 3
    # x^2: 9
    # ...

    @print_exits
    def some_func(...):
        "..."

    @log_calls(log.info, errors=False)
    @log_errors(log.exception)
    def some_suspicious_function(...):
        "..."

    with print_durations('Creating models'):
        Model.objects.create(...)
        # ...
    # 10.2 ms in Creating models


And `much more <http://funcy.readthedocs.org/>`_.


Running tests
--------------

To run the tests using your default python:

::

    pip install -r test_requirements.txt
    py.test

To fully run ``tox`` you need all the supported pythons to be installed. These are
2.6+, 3.3+, PyPy and PyPy3. You can run it for particular environment even in absense
of all of the above::

    tox -e py27
    tox -e py34
    tox -e lint


.. |Build Status| image:: https://travis-ci.org/Suor/funcy.svg?branch=master
   :target: https://travis-ci.org/Suor/funcy


.. |Gitter| image:: https://badges.gitter.im/JoinChat.svg
   :alt: Join the chat at https://gitter.im/Suor/funcy
   :target: https://gitter.im/Suor/funcy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
