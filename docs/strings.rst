String utils
============

.. function:: re_find(regex, s, flags=0)
.. function:: re_test(regex, s, flags=0)
.. function:: re_iter(regex, s, flags=0)
.. function:: re_all(regex, s, flags=0)

.. function:: re_finder(regex, flags=0)
.. function:: re_tester(regex, flags=0)

.. function:: str_join([sep=""], seq)

    Joins sequence by ``sep``. Same as ``sep.join(seq)``, but forcefully stringifies elements.

.. function:: cut_prefix(s, prefix)
.. function:: cut_suffix(s, suffix)
