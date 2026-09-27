.. _extended_fns:

Extended function semantics
===================================

Many of funcy functions expecting predicate or mapping function as an argument can take something uncallable instead of it with semantics described in this table:

============   =================================  =================================
f passed       Function                           Predicate
============   =================================  =================================
``None``       :func:`identity <identity>`        bool
string         :func:`re_finder(f) <re_finder>`   :func:`re_tester(f) <re_tester>`
int or slice   ``itemgetter(f)``                  ``itemgetter(f)``
mapping        ``lambda x: f[x]``                 ``lambda x: f[x]``
set            ``lambda x: x in f``               ``lambda x: x in f``
============   =================================  =================================


Examples
--------

A mapping looks up each input as a key, instead of requiring a lookup function::

    >>> from funcy import lmap
    >>> names = {'fr': 'French', 'en': 'English'}
    >>> lmap(names, ['en', 'fr'])
    ['English', 'French']

An ordinary dictionary raises ``KeyError`` for missing keys. Pass its ``get``
method instead to return ``None`` for an unknown language code::

    >>> lmap(names.get, ['en', 'de'])
    ['English', None]

A set tests membership. Use it with :func:`select_keys` to pick connection
options out of a larger configuration::

    >>> from funcy import select_keys
    >>> config = {'host': 'localhost', 'port': 8000, 'debug': True}
    >>> select_keys({'host', 'port'}, config)
    {'host': 'localhost', 'port': 8000}

An integer selects an item by index. For example, ``dict.items()`` produces
``(name, department)`` pairs that :func:`group_by` can group by department::

    >>> from funcy import group_by
    >>> departments = {'Alice': 'engineering', 'Bob': 'sales', 'Carol': 'engineering'}
    >>> by_department = group_by(1, departments.items())
    >>> by_department['engineering']
    [('Alice', 'engineering'), ('Carol', 'engineering')]

A slice selects part of each input. Use the year and month of ISO-formatted
dates to count orders by month::

    >>> from funcy import count_by
    >>> order_dates = ['2025-03-01', '2025-04-02', '2025-03-15']
    >>> dict(count_by(slice(0, 7), order_dates))
    {'2025-03': 2, '2025-04': 1}

A string is a regular expression, not an attribute or dictionary key. As a
function it extracts a match. For example, :func:`lkeep` can extract issue
numbers from commit messages, skipping messages without a match::

    >>> from funcy import lkeep
    >>> messages = ['Fix #123: handle empty input', 'Update docs', 'Close #456']
    >>> lkeep(r'#(\d+)', messages)
    ['123', '456']

As a predicate, a regular expression tests whether a match exists. Use it to
select CSV filenames::

    >>> from funcy import lfilter
    >>> lfilter(r'\.csv$', ['users.csv', 'README.md', 'orders.csv'])
    ['users.csv', 'orders.csv']

``None`` leaves values unchanged when used as a function, and tests their
truthiness when used as a predicate::

    >>> lmap(None, [0, 1, '', 'hello'])
    [0, 1, '', 'hello']
    >>> lfilter(None, [0, 1, '', 'hello'])
    [1, 'hello']


Supporting functions
--------------------

Here is a full list of functions supporting extended function semantics:

========================= ==============================================================
Group                     Functions
========================= ==============================================================
Sequence transformation   :func:`map` :func:`keep` :func:`mapcat`
Sequence filtering        :func:`filter` :func:`remove` :func:`distinct`
Sequence splitting        :func:`dropwhile` :func:`takewhile` :func:`split` :func:`split_by` :func:`partition_by`
Aggregration              :func:`group_by` :func:`count_by` :func:`group_by_keys`
Collection transformation :func:`walk` :func:`walk_keys` :func:`walk_values`
Collection filtering      :func:`select` :func:`select_keys` :func:`select_values`
Content tests             :func:`all` :func:`any` :func:`none` :func:`one` :func:`some` :func:`is_distinct`
Function logic            :func:`all_fn` :func:`any_fn` :func:`none_fn` :func:`one_fn` :func:`some_fn`
Function tools            :func:`iffy` :func:`compose` :func:`rcompose` :func:`complement` :func:`juxt` :func:`all_fn` :func:`any_fn` :func:`none_fn` :func:`one_fn` :func:`some_fn`
========================= ==============================================================

List or iterator versions of same functions not listed here for brevity but also support extended semantics.

.. raw:: html
    :file: descriptions.html
