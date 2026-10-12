Collections
===========

Unite
-----

.. function:: merge(*colls)

    Merges several collections of same type into one: dicts, sets, lists, tuples, iterators or strings. For dicts values of later dicts override values of former ones with same keys.

    Can be used in variety of ways, but merging dicts is probably most common::

        def utility(**options):
            defaults = {...}
            options = merge(defaults, options)
            ...

    If you merge sequences and don't need to preserve collection type, then use :func:`concat` or :func:`lconcat` instead.


.. function:: join(colls)

    Joins collections of same type into one. Same as :func:`merge`, but accepts iterable of collections.

    Use :func:`cat` and :func:`lcat` for non-type preserving sequence join.


Transform and select
--------------------

All functions in this section support :ref:`extended_fns`.

.. function:: walk(f, coll)

    Returns a collection of same type as ``coll`` consisting of its elements mapped with the given function::

        walk(inc, {1, 2, 3}) # -> {2, 3, 4}
        walk(inc, (1, 2, 3)) # -> (2, 3, 4)

    When walking dict, ``(key, value)`` pairs are mapped, i.e. this lines :func:`flip` dict::

        swap = lambda (k, v): (v, k)
        walk(swap, {1: 10, 2: 20})

    :func:`walk` works with strings too::

        walk(lambda x: x * 2, 'ABC')   # -> 'AABBCC'
        walk(compose(str, ord), 'ABC') # -> '656667'

    One should use :func:`map` when there is no need to preserve collection type.

    .. note about constructor interface?


.. function:: walk_keys(f, coll)

    Walks keys of ``coll``, mapping them with the given function. Works with mappings and collections of pairs::

        walk_keys(str.upper, {'a': 1, 'b': 2}) # {'A': 1, 'B': 2}
        walk_keys(int, json.loads(some_dict))  # restore key type lost in translation

    Important to note that it preserves collection type whenever this is simple :class:`py3:dict`, :class:`~py3:collections.defaultdict`, :class:`~py3:collections.OrderedDict` or any other mapping class or a collection of pairs.


.. function:: walk_values(f, coll)

    Walks values of ``coll``, mapping them with the given function. Works with mappings and collections of pairs.

    Common use is to process values somehow::

        clean_values = walk_values(int, form_values)
        sorted_groups = walk_values(sorted, groups)

    Hint: you can use :func:`partial(sorted, key=...) <partial>` instead of :func:`py3:sorted` to sort in non-default way.

    Note that ``walk_values()`` has special handling for :class:`defaultdicts <py3:collections.defaultdict>`. It constructs new one with values mapped the same as for ordinary dict, but a default factory of new ``defaultdict`` would be a composition of ``f`` and old default factory::

        d = defaultdict(lambda: 'default', a='hi', b='bye')
        walk_values(str.upper, d)
        # -> defaultdict(lambda: 'DEFAULT', a='HI', b='BYE')


.. function:: select(pred, coll)

    Filters elements of ``coll`` by ``pred`` constructing a collection of same type. When filtering a dict ``pred`` receives ``(key, value)`` pairs. See :func:`select_keys` and :func:`select_values` to filter it by keys or values respectively::

        select(even, {1, 2, 3, 10, 20})
        # -> {2, 10, 20}

        select(lambda (k, v): k == v, {1: 1, 2: 3})
        # -> {1: 1}


.. function:: select_keys(pred, coll)

    Select part of a dict or a collection of pairs with keys passing the given predicate.

    This way a public part of instance attributes dictionary could be selected::

        is_public = complement(re_tester('^_'))
        public = select_keys(is_public, instance.__dict__)


.. function:: select_values(pred, coll)

    Select part of a dict or a collection of pairs with values passing the given predicate::

        # Leave only str values
        select_values(isa(str), values)

        # Construct a dict of methods
        select_values(inspect.isfunction, cls.__dict__)


.. function:: split_keys(pred, coll)

    Splits a dictionary into two based on a predicate applied to its keys.

    Say, you can separate custom HTTP headers from standard ones::

        custom, standard = split_keys(r'^X-', headers)
        # custom -> {'X-Custom-Header': 'value'}
        # standard -> {'Content-Type': 'application/json', ...}


.. function:: compact(coll)

    Removes falsy values from given collection. When compacting a dict all keys with falsy values are removed.

    Extract integer data from request::

        compact(walk_values(silent(int), request_dict))


Dict utils
----------

.. function:: merge_with(f, *dicts)
              join_with(f, dicts, strict=False)

    Merge several dicts combining values for same key with given function::

        merge_with(list, {1: 1}, {1: 10, 2: 2})
        # -> {1: [1, 10], 2: [2]}

        merge_with(sum, {1: 1}, {1: 10, 2: 2})
        # -> {1: 11, 2: 2}

        join_with(first, ({n % 3: n} for n in range(100, 110)))
        # -> {0: 102, 1: 100, 2: 101}

    Historically ``join_with()`` will return a dict as is if there is only one, which might be inconvenient. To always apply the summarization func use ``strict`` param::

        join_with(list, [{1: 2}])              # {1: 2}
        join_with(list, [{1: 2}], strict=True) # {1: [2]}
        join_with(len, [{1: 2}], strict=True)  # {1: 1}


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


.. function:: omit(mapping, keys)

    Returns a copy of ``mapping`` with ``keys`` omitted. Each key of `mapping` is checked if it is contained with `keys`, so a string and an array could be used. Preserves collection type::

        omit({'a': 1, 'b': 2, 'c': 3}, 'ac')
        # -> {'b': 2}

        omit({'a': 1, 'b': 2, 'c': 3}, ['a', 'c'])
        # -> {'b': 2}


.. function:: zip_values(*dicts)

    Yields tuples of corresponding values of given dicts. Skips any keys not present in all of the dicts. Comes in handy when comparing two or more dicts::

        error = sum((x - y) ** 2 for x, y in zip_values(result, reference))


.. function:: zip_dicts(*dicts)

    Yields tuples like ``key, (value1, value2, ...)`` for each common key of all given dicts. A neat way to process several dicts at once::

        changed_items = [id for id, (new, old) in zip_dicts(items, old_items)
                         if abs(new - old) >= PRECISION]

        lines = {id: cnt * price for id, (cnt, price) in zip_dicts(amounts, prices)}

    See also :func:`zip_values`.


.. function:: get_in(coll, path, default=None)

    Returns a value corresponding to ``path`` in nested collection::

        get_in({"a": {"b": 42}}, ["a", "b"])    # -> 42
        get_in({"a": {"b": 42}}, ["c"], "foo")  # -> "foo"

    Note that missing key or index, i.e. `KeyError` and `IndexError` result into `default` being return, while trying to use non-int index for a list will result into `TypeError`. This way funcy stays strict on types.


.. function:: get_lax(coll, path, default=None)

    A version of :func:`get_in` that tolerates type along the path not working with an index::

        get_lax([1, 2, 3], ["a"], "foo")  # -> "foo"
        get_lax({"a": None}, ["a", "b"])  # -> None


.. function:: set_in(coll, path, value)

    Creates a nested collection with the ``value`` set at specified ``path``. Original collection is not changed::

        set_in({"a": {"b": 42}}, ["a", "b"], 10)
        # -> {"a": {"b": 10}}

        set_in({"a": {"b": 42}}, ["a", "c"], 10)
        # -> {"a": {"b": 42, "c": 10}}


.. function:: update_in(coll, path, update, default=None)

    Creates a nested collection with a value at specified ``path`` updated::

        update_in({"a": {}}, ["a", "cnt"], inc, default=0)
        # -> {"a": {"cnt": 1}}


.. function:: del_in(coll, path)

    Creates a nested collection with ``path`` removed::

        del_in({"a": [1, 2, 3]}, ["a", 1])
        # -> {"a": [1, 3]}

    Returns the collection as is if the path is missing.


.. function:: has_path(coll, path)

    Checks if path exists in the given nested collection::

        has_path({"a": {"b": 42}}, ["a", "b"]) # -> True
        has_path({"a": {"b": 42}}, ["c"])  # -> False
        has_path({"a": [1, 2]}, ["a", 0])  # -> True


Data manipulation
-----------------

.. function:: where(mappings, **cond)
              lwhere(mappings, **cond)

    Looks through each value in given sequence of dicts and returns an iterator or a list of all the dicts that contain all key-value pairs in ``cond``::

        lwhere(plays, author="Shakespeare", year=1611)
        # => [{"title": "Cymbeline", "author": "Shakespeare", "year": 1611},
        #     {"title": "The Tempest", "author": "Shakespeare", "year": 1611}]

    Iterator version could be used for efficiency or when you don't need the whole list.
    E.g. you are looking for the first match::

        first(where(plays, author="Shakespeare"))
        # => {"title": "The Two Gentlemen of Verona", ...}


.. function:: pluck(key, mappings)
              lpluck(key, mappings)

    Returns an iterator or a list of values for ``key`` in each mapping in the given sequence. Essentially a shortcut for::

        map(operator.itemgetter(key), mappings)

    e.g. extracting a key from a list of dictionaries::

        lpluck('name', [{'name': 'John'}, {'name': 'Mary'}])
        # -> ['John', 'Mary']


.. function:: pluck_attr(attr, objects)
              lpluck_attr(attr, objects)

    Returns an iterator or a list of values for ``attr`` in each object in the given sequence. Essentially a shortcut for::

        map(operator.attrgetter(attr), objects)

    Useful when dealing with collections of ORM objects::

        users = User.query.all()
        ids = lpluck_attr('id', users)


.. function:: invoke(objects, name, *args, **kwargs)
              linvoke(objects, name, *args, **kwargs)

    Calls named method with given arguments for each object in ``objects`` and returns an iterator or a list of results.

    For example::

        invoke(['abc', 'def', 'b'], 'find', 'b')
        # ->[1, -1, 0]


Content tests
-------------

.. function:: is_distinct(coll, key=identity)

    Checks if all elements in the collection are different::

        assert is_distinct(field_names), "All fields should be named differently"

    Uses ``key`` to differentiate values. This way one can check if all first letters of ``words`` are different::

        is_distinct(words, key=0)


.. function:: all([pred], seq)

    Checks if ``pred`` holds for every element in a ``seq``. If ``pred`` is omitted checks if all elements of ``seq`` are truthy -- same as in built-in :func:`py3:all`::

        they_are_ints = all(is_instance(n, int) for n in seq)
        they_are_even = all(even, seq)

    Note that, first example could be rewritten using :func:`isa` like this::

        they_are_ints = all(isa(int), seq)


.. function:: any([pred], seq)

    Returns ``True`` if ``pred`` holds for any item in given sequence. If ``pred`` is omitted checks if any element of ``seq`` is truthy.

    Check if there is a needle in haystack, using :ref:`extended predicate semantics <extended_fns>`::

        any(r'needle', haystack_strings)


.. function:: none([pred], seq)

    Checks if none of items in given sequence pass ``pred`` or is truthy if ``pred`` is omitted.

    Just a stylish way to write ``not any(...)``::

        assert none(' ' in name for name in names), "Spaces in names not allowed"

        # Or same using extended predicate semantics
        assert none(' ', names), "..."

.. function:: one([pred], seq)

    Returns true if exactly one of items in ``seq`` passes ``pred``. Cheks for truthiness if ``pred`` is omitted.


.. function:: some([pred], seq)

    Finds first item in ``seq`` passing ``pred`` or first that is true if ``pred`` is omitted.


Low-level helpers
-----------------

.. function:: empty(coll)

    Returns an empty collection of the same type as ``coll``.


.. function:: iteritems(coll)

    Returns an iterator of items of a ``coll``. This means ``key, value`` pairs for any dictionaries::

        list(iteritems({1, 2, 42}))
        # -> [1, 42, 2]

        list(iteritems({'a': 1}))
        # -> [('a', 1)]


.. function:: itervalues(coll)

    Returns an iterator of values of a ``coll``. This means values for any dictionaries and just elements for other collections::

        list(itervalues({1, 2, 42}))
        # -> [1, 42, 2]

        list(itervalues({'a': 1}))
        # -> [1]


.. raw:: html
    :file: descriptions.html
