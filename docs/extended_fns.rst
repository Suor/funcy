.. _extended_fns:

Extended predicate/mapper semantics
===================================

Many of funcy functions expecting predicate or mapping function as an argument can take something uncallable instead of it with semantics described in this table:

============  ================================= =================================
f passed      Predicate                         Mapping function
============  ================================= =================================
``None``      bool                              :func:`identity <identity>`
string        :func:`re_tester(f) <re_tester>`  :func:`re_finder(f) <re_finder>`
int or slice  ``itemgetter(f)``                 ``itemgetter(f)``
mapping       ``f.get``                         ``f.get``
set           ``lambda x: x in f``              ``lambda x: x in f``
============  ================================= =================================


Supporting functions
--------------------

Here is a full list of functions supporting extended predicate/mapper semantics:

========================= ==============================================================
Group                     Functions
========================= ==============================================================
Sequence transformation   :func:`map`, :func:`imap`, :func:`keep`, :func:`ikeep`, :func:`mapcat`, :func:`imapcat`
Sequence filtering        :func:`filter`, :func:`ifilter`, :func:`remove`, :func:`iremove`
Sequence splitting        :func:`dropwhile`, :func:`takewhile`, :func:`split`, :func:`split_by`
Collection transformation :func:`walk`, :func:`walk_keys`, :func:`walk_values`
Collection filtering      :func:`select`, :func:`select_keys`, :func:`select_values`
Content tests             :func:`all`, :func:`any`, :func:`none`, :func:`one`, :func:`some`
Function logic            :func:`all_fn`, :func:`any_fn`, :func:`none_fn`, :func:`one_fn`, :func:`some_fn`
Function tools            :func:`compose`, :func:`complement`, :func:`juxt`, :func:`ijuxt`
========================= ==============================================================
