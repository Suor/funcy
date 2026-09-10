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

The examples below use funcy's :func:`lmap` and :func:`lfilter`, which return
lists.

A mapping looks up each input as a key, instead of requiring a lookup function::

    >>> from funcy import lmap, lfilter
    >>> names = {'fr': 'French', 'en': 'English'}
    >>> lmap(names, ['en', 'fr'])
    ['English', 'French']
    >>> lmap(lambda code: names[code], ['en', 'fr'])
    ['English', 'French']

When used as a predicate, a mapping tests the truthiness of the value at each
key, not whether the key exists::

    >>> enabled = {'email': True, 'sms': False}
    >>> lfilter(enabled, ['email', 'sms'])
    ['email']

An ordinary dictionary raises ``KeyError`` for missing keys in either case.
Use a set when you want to test membership instead::

    >>> allowed = {'email', 'sms'}
    >>> lfilter(allowed, ['email', 'push', 'sms'])
    ['email', 'sms']
    >>> lmap(allowed, ['email', 'push', 'sms'])
    [True, False, True]

An integer or slice selects part of each input::

    >>> lmap(0, [('Alice', 30), ('Bob', 25)])
    ['Alice', 'Bob']
    >>> lmap(slice(0, 2), ['Alice', 'Bob'])
    ['Al', 'Bo']

A string is a regular expression, not an attribute or dictionary key. As a
function it extracts a match; as a predicate it tests whether a match exists::

    >>> lmap(r'\d+', ['item12', 'none', 'item34'])
    ['12', None, '34']
    >>> lfilter(r'\d+', ['item12', 'none', 'item34'])
    ['item12', 'item34']

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
