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

Most of functions in this section support :ref:`extended_fns`.r

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

    .. note about constructor interface?


.. function:: walk_keys(f, coll)

    Walks keys of ``coll``, mapping them with given function. Works with mappings and collections of pairs::

        walk_keys(str.upper, {'a': 1, 'b': 2}) # {'A': 1, 'B': 2}


    Important to note that it preserves collection type whether it is simple :class:`dict`, :class:`~collections.defaultdict`, :class:`~collections.OrderedDict` or any other mapping class or a collection of pairs.


.. function:: walk_values(f, coll)

    Walks values of ``coll``, mapping them with given function. Works with mappings and collections of pairs.

    Common use is to process values somehow::

        clean_values = walk_values(int, form_values)
        sorted_groups = walk_values(sorted, groups)

    Hint: you can use :func:`partial(sorted, key=...) <partial>` instead of :func:`sorted` to sort in non-default way.


.. function:: select(pred, coll)

    Filters elements of ``coll`` by ``pred`` constructing collection of same type. When filtering a dict ``pred`` receives ``(key, value)`` pairs. See :func:`select_keys` and :func:`select_values` to filter it by keys or values respectively::

        select(even, {1, 2, 3, 10, 20})
        # -> {2, 10, 20}

        select(lambda (k, v): k == v, {1: 1, 2: 3})
        # -> {1: 1}


.. function:: select_keys(pred, coll)

    Select part of a dict or a collection of pairs with keys passing given predicate.

    This way a public part of instance attributes dictionary could be selected::

        is_public = complement(re_tester('^_'))
        public = select_keys(is_public, instance.__dict__)


.. function:: select_values(pred, coll)

    Select part of a dict or a collection of pairs with values passing given predicate.

    Strip falsy values from dict::

        select_values(bool, some_dict)


.. function:: compact(coll)

    Removes falsy values from given collection. When compacting a dict all keys with falsy values are trashed.

    Extract integer data from request::

        compact(walk_values(silent(int), request_dict))


Dict utils
----------

.. function:: zipdict(keys, vals)

    Returns a dict with the ``keys`` mapped to the corresponding ``vals``. Stops pairing on shorter sequence end::

        zipdict('abcd', range(4))
        # -> {'a': 0, 'b': 1, 'c': 2, 'd': 3}

        zipdict('abc', count())
        # -> {'a': 0, 'b': 1, 'c': 2}


.. function:: flip(mapping)

    Flip passed dict swapping its keys and values. Also works for sequences of pairs. Preserves collection type::

        flip(OrderedDict(['aA', 'bB']))
        # -> OrderedDict([('A', 'a'), ('B', 'b')])


.. function:: project(mapping, keys)

    Returns a dict containing only those entries in ``mapping`` whose key is in ``keys``.

    Most useful to shrink some common data or options to predefined subset. One particular case is constructing a dict of used variables::

        merge(project(__builtins__, names), project(globals(), names))


.. function:: zip_values(*dicts)

    Yields tuples of corresponding values of given dicts. Skips any keys not present in all of the dicts. Comes in handy when comparing two or more dicts::

        max_change = max(abs(x - y) for x, y in izip_values(items, old_items))


.. function:: zip_dicts(*dicts)

    Yields tuples like ``(key, value1, value2, ...)`` for each common key of all given dicts. A neat way to process several dicts at once::

        changed_items = [id for id, new, old in izip_dicts(items, old_items)
                         if abs(new - old) >= PRECISION]

        lines = {id: cnt * price for id, cnt, price in izip_dicts(amounts, prices)}

    See also :func:`zip_values`.



Data manipulation
-----------------

.. function:: where(mappings, **cond)

    Looks through each value in given sequence of dicts, returning a list of all the dicts that contain all of the key-value pairs in ``cond``::

        where(plays, author="Shakespeare", year=1611)
        # => [{"title": "Cymbeline", "author": "Shakespeare", "year": 1611},
        #     {"title": "The Tempest", "author": "Shakespeare", "year": 1611}]


.. function:: pluck(key, mappings)

    Returns list of values for ``key`` in each mapping in given sequence. Essentialy a shortcut for::

        map(operator.itemgetter(key), mappings)


.. function:: invoke(objects, name, *args, **kwargs)

    Calls named method with given arguments for each object in ``objects`` and returns a list of results.


Content tests
-------------

.. function:: is_distinct(coll)

    Checks if all elements in collection are diffrent::

        assert is_distinct(field_names), "All fields should be named diffrently"


.. function:: all([pred], seq)

    Checks if ``pred`` holds every element in a ``seq``. If ``pred`` is omitted checks if all elements of ``seq`` is true (which is the same as in builtin :func:`~builtin.all`)::

        they_are_ints = all(is_instance(n, int) for n in seq)
        they_are_even = all(even, seq)

    Note that, first example could be rewritten using :func:`isa` like this::

        they_are_ints = all(isa(int), seq)


.. function:: any([pred], seq)

    Returns ``True`` if ``pred`` holds for any item in given sequence. If ``pred`` is omitted checks if any element of ``seq`` is true.

    Check if there is a needle in haystack, using :ref:`extended predicate semantics <extended_fns>`::

        any(r'needle', haystack_strings)


.. function:: none([pred], seq)

    Checks if none of items in given sequence pass ``pred`` or true if ``pred`` is omitted.

    Just a stylish way to write ``not any(...)``::

        assert none(' ' in name for name in names), "Spaces in names not allowed"


.. function:: one([pred], seq)

    Returns true if exactly one of items in ``seq`` passes ``pred``. Cheks for boolean true if ``pred`` is omitted.


.. function:: some([pred], seq)

    Finds first item in ``seq`` passing ``pred`` or first that is true if ``pred`` is omitted.
