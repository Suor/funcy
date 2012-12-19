Sequences
=========

.. module:: seqs

Generate
--------

.. function:: count(start, [step])
.. function:: repeat(elem, [n])
.. function:: repeatedly(f, [n])
.. function:: iterate(f, x)


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

