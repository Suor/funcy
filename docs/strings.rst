String utils
============

.. function:: re_find(regex, s, flags=0)

    Finds ``regex`` in ``s``, returning the match in the simplest possible form guessed by captures in given regular expression:

    ================================= ==================================
    Captures                          Return value
    ================================= ==================================
    no captures                       a matched string
    single positional capture         a substring matched by capture
    only positional captures          a tuple of substrings for captures
    only named captures               a dict of substrings for captures
    mixed pos/named captures          a match object
    ================================= ==================================

    Returns ``None`` on mismatch.

    ::

        # Find first number in a line
        silent(int)(re_find(r'\d+', line))

        # Find number of men in a line
        re_find(r'(\d+) m[ae]n', line)

        # Parse uri into nice dict
        re_find(r'^/post/(?P<id>\d+)/(?P<action>\w+)$', uri)


.. function:: re_test(regex, s, flags=0)

    Tests whether ``regex`` can be found in ``s``.


.. function:: re_all(regex, s, flags=0)
              re_iter(regex, s, flags=0)

    Returns a list or iterator of all matches of ``regex`` in ``s``. Matches are presented in most simple form possible, see table in :func:`re_find` docs.

    ::

        # A fast and dirty way to parse ini section into dict
        dict(re_iter('(\w+)=(\w+)', ini_text))


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
