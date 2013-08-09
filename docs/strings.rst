String utils
============

.. function:: re_find(regex, s, flags=0)
.. function:: re_test(regex, s, flags=0)
.. function:: re_iter(regex, s, flags=0)
.. function:: re_all(regex, s, flags=0)


.. function:: re_finder(regex, flags=0)

    Returns a function that calls :func:`re_find` for it's sole argument. It's main purpose is quickly constructing mapper functions for :func:`map` and friends.

    See also :ref:`extended_fns`.


.. function:: re_tester(regex, flags=0)

    Returns a function that calls :func:`re_test` for it's sole argument. Aimed at quick construction of predicates for use in :func:`filter` and friends.

    See also :ref:`extended_fns`.


.. function:: str_join([sep=""], seq)

    Joins sequence by ``sep``. Same as ``sep.join(seq)``, but forcefully converts all elements to separator type, ``str`` by default.

    See also :func:`joining`.


.. function:: cut_prefix(s, prefix)

    Cuts prefix from given string if it's present.


.. function:: cut_suffix(s, suffix)

    Cuts suffix from given string if it's present.
