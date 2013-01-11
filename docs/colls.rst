Collections
===========

Unite
-----

.. .. function:: empty(coll)


.. function:: merge(*colls)

    Merges several collections of same type into one: dicts, sets, lists, tuples, iterators or strings. For dicts values of later dicts override values of former ones with same keys.

    Can be used in variety of ways, but merging dicts is probably most common::

        def utility(**options):
            defaults = {...}
            options = merge(defaults, options)
            ...

    If you merge sequences and don't need to preserve collection type, then use :func:`concat` or :func:`iconcat` instead.


.. function:: join(colls)

    Joins collections of same type into one. Same as :func:`merge`, but accepts iterable of collections.

    Use :func:`cat` and :func:`icat` for non-type preserving sequence join.


Transform and select
--------------------

.. function:: walk(f, coll)

    Returns collection of same type as ``coll`` consisting of its elements mapped with given function::

        walk(inc, {1, 2, 3}) # -> {2, 3, 4}
        walk(inc, (1, 2, 3)) # -> (2, 3, 4)

    When walking dict, ``(key, value)`` pairs are mapped, i.e. this lines :func:`flip` dict::

        swap = lambda (k, v): (v, k)
        walk(swap, {1: 10, 2: 20})

    :func:`walk` works with strings too::

        walk(lambda x: x * 2, 'ABC')   # -> 'AABBCC'
        walk(compose(str, ord), 'ABC') # -> '656667'

    One should probably use :func:`map` or :func:`~itertools.imap` when doesn't need to preserve collection type.

.. function:: walk_keys(f, coll)

    Walks keys of ``coll`` mapping them with given function. Works with mappings and collections of pairs::

        walk_keys(str.upper, {'a': 1, 'b': 2}) # {'A': 1, 'B': 2}


    .. :class:`dicts <dict>`, :class:`defaultdicts <collections.defaultdict>`

.. function:: walk_values(f, coll)

    Walks values of ``coll`` mapping them with given function. Works with mappings and collections of pairs.

    Common use is to process values somehow::

        clean_values = walk_values(int, form_values)
        sorted_groups = walk_values(sorted, groups)

    Hint: you can use :func:`partial(sorted, key=...) <partial>` instead of :func:`sorted` to sort in non-default way.


.. function:: select(pred, coll)
.. function:: select_keys(pred, coll)
.. function:: select_values(pred, coll)

    Strip falsy values from dict::

        select_values(bool, some_dict)


Dict utils
----------

.. function:: zipdict(colls)
.. function:: flip(colls)
.. function:: project(colls)


Data mangling
-------------

.. function:: where(mappings, **cond)
.. function:: pluck(mappings, key)
.. function:: invoke(objects, name, *args, **kwargs)


Content tests
-------------

.. function:: is_distinct(colls)
.. function:: all(colls)
.. function:: any(colls)
.. function:: none(colls)
.. function:: one(colls)
.. function:: some(colls)


Collections of functions
------------------------

.. function:: all_fn(*fs)
.. function:: any_fn(*fs)
.. function:: none_fn(*fs)
.. function:: one_fn(*fs)
.. function:: some_fn(*fs)
