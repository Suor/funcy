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

    If you merge sequences and don't need to preserve collection type then use :func:`concat` or :func:`iconcat` instead.


.. function:: join(colls)

    Joins collections of same type into one. Same as :func:`merge`, but accepts iterable of collections.

    Use :func:`cat` and :func:`icat` for non-type preserving sequence join.


Transform and select
--------------------

.. function:: walk(f, coll)
.. function:: walk_keys(f, coll)
.. function:: walk_values(f, coll)

    ::

        groups = walk_values(sorted, groups) # partial(sorted, key=...)


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
