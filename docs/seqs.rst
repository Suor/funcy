Sequences
=========

Generate
--------

.. function:: repeat(elem, [n])

    Makes an iterator returning ``elem`` for ``n`` times or indefinitly if ``n`` is omitted.

    .. Is a reexport of :func:`itertools.repeat`.


.. function:: count(start=0, step=1)

    Makes infinite iterator of values: ``start, start + step, start + 2*step, ...``.

    .. Is a reexport of :func:`itertools.count`.


.. function:: cycle(seq)

    Cycles passed ``seq`` indefinitly returning its elements one by one.

    .. Is a reexport of :func:`itertools.cycle`.


.. function:: repeatedly(f, [n])

    Takes a function of no args, presumably with side effects, and
    returns an infinite (or length ``n`` if supplied) iterator of calls
    to it.

    For example, this call can be used to generate 10 random numbers::

        repeatedly(random.random, 10)

    Or one can create a length ``n`` list of freshly-created objects of same type::

        repeatedly(list, n)

.. function:: iterate(f, x)

    Returns an infinite iterator of ``x, f(x), f(f(x)), ...`` etc.

    Most common use is to generate some recursive sequence::

        iterate(inc, 5)
        # -> 5, 6, 7, 8, 9, ...

        iterate(lambda x: x * 2, 1)
        # -> 1, 2, 4, 8, 16, ...

        # this one generates Fibonacci sequence
        step = lambda ((a, b)): (b, a + b)
        imap(first, iterate(step, (0, 1)))
        # -> 0, 1, 1, 2, 3, 5, 8, ...

Manipulate
----------

.. function:: take(n, seq)
.. function:: drop(n, seq)
.. function:: first(seq)
.. function:: second(seq)
.. function:: rest(seq)


Unite
-----

.. function:: concat(*seqs)
              iconcat(*seqs)

    Concats several sequences into one.

    :func:`iconcat` is an alias for :func:`itertools.chain`.


.. function:: cat(seqs)
              icat(seqs)

    :func:`icat` is an alias for :meth:`itertools.chain.from_iterable`.


Transform and filter
--------------------

.. function:: remove(pred, coll)
              iremove(pred, coll)

    :func:`iremove` is an alias for :func:`itertools.ifilterfalse`.

.. function:: keep([f], seq)
              ikeep([f], seq)

.. function:: mapcat(f, *colls)
              imapcat(f, *colls)


Sequence mangling
-----------------

.. function:: interleave(*seqs)
.. function:: interpose(sep, seq)
.. function:: dropwhile(pred, seq)
.. function:: takewhile(pred, seq)


Data mangling
-------------

.. function:: distinct(seq)
.. function:: split(at, seq)
.. function:: isplit(at, seq)
.. function:: groupby(f, seq)
.. function:: partition(n, [step], seq)
.. function:: chunks(n, [step], seq)

