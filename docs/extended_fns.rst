.. raw:: html
    :file: _popups.html


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
