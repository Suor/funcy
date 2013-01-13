Sequences
=========

.. .. module:: seqs

This functions are aimed at manipulating finite and infinite sequences of values. Some functions have two flavours: one returning list and other returning possibly infinite iterator, the latter ones follow convention of prepending ``i`` before list-returning function name.

When working with sequences, see also :mod:`itertools` standard module. Funcy reexports and aliases some functions from it.


Generate
--------

.. function:: repeat(elem, [n])

    Makes an iterator returning ``elem`` for ``n`` times or indefinitly if ``n`` is omitted. :func:`repeat` simply repeat given value, when you need to reevaluate something repeatedly use :func:`repeatedly` instead.

    When you just need a length ``n`` list or tuple of ``elem`` you can use::

        [elem] * n
        # or
        (elem,) * n

    .. Is a reexport of :func:`itertools.repeat`.


.. function:: count(start=0, step=1)

    Makes infinite iterator of values: ``start, start + step, start + 2*step, ...``.

    Could be used to gererate sequence::

        imap(lambda x: x ** 2, count(1))
        # -> 1, 4, 9, 16, ...

    Or annotate sequence using :func:`zip` or :func:`~itertools.izip`::

        zip(count(), 'abcd')
        # -> [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd')]

        # print code with BASIC-style numbered lines
        for line in izip(count(10, 10), code.splitlines()):
            print '%d %s' % line

    See also :func:`enumerate` and original :func:`itertools.count` documentation.


.. function:: cycle(seq)

    Cycles passed ``seq`` indefinitly returning its elements one by one.

    Useful when you need to cyclically decorate some sequence::

        for n, parity in izip(count(), cycle(['even', 'odd'])):
            print '%d is %s' % (n, parity)

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

        step = lambda ((a, b)): (b, a + b)
        imap(first, iterate(step, (0, 1)))
        # -> 0, 1, 1, 2, 3, 5, 8, ... (Fibonacci sequence)


Manipulate
----------

This section provides some robust tools for sequence slicing. Consider :ref:`slicings` or :func:`itertools.islice` for more generic cases.

.. function:: take(n, seq)

    Returns a list of the first ``n`` items in sequence, or all items if there are fewer than ``n``.

    ::

        take(3, [2, 3, 4, 5]) # [2, 3, 4]
        take(3, count(5))     # [5, 6, 7]
        take(3, 'ab')         # ['a', 'b']

.. function:: drop(n, seq)

    Skips first ``n`` items in sequence, returning iterator yielding rest of its items.

    ::

        drop(3, [2, 3, 4, 5]) # iter([5])
        drop(3, count(5))     # count(8)
        drop(3, 'ab')         # empty iterator

.. function:: first(seq)

    Returns first item in sequence. Returns ``None`` if sequence is empty. Typical usage is choosing first of some inplace generated variants::

        # Get a text message of first failed validation rule
        fail = first(rule.text for rule in rules if not rule.test(instance))

        # Use simple pattern matching to construct form field widget
        TYPE_TO_WIDGET = (
            [lambda f: f.choices,           lambda f: Select(choices=f.choices)],
            [lambda f: f.type == 'int',     lambda f: TextInput(coerce=int)],
            [lambda f: f.type == 'string',  lambda f: TextInput()],
            [lambda f: f.type == 'text',    lambda f: Textarea()],
            [lambda f: f.type == 'boolean', lambda f: Checkbox(f.label)],
        )
        return first(do(field) for cond, do in TYPE_TO_WIDGET if cond(field))

    Other common use case is passing to :func:`map` or :func:`~itertools.imap`. See last example in :func:`iterate` for such example.


.. function:: second(seq)

    Returns second item in sequence. Returns ``None`` if there are less than two items in it.

    Could come in handy with sequences of pairs, e.g. :meth:`dict.items`. Following code extract values of a dict sorted by keys::

        map(second, sorted(some_dict.items()))

    And this line constructs an ordered by value dict from a plain one::

        OrderedDict(sorted(plain_dict, key=second))


.. function:: rest(seq)

    Skips first item in sequence, returning iterator starting just after it. A shortcut for :func:`drop(1, seq) <drop>`.


Unite
-----

.. function:: concat(*seqs)
              iconcat(*seqs)

    Concats several sequences into one. :func:`iconcat` returns an iterator yielding concatenation.

    :func:`iconcat` is an alias for :func:`itertools.chain`.


.. function:: cat(seqs)
              icat(seqs)

    Returns concatenation of passed seqs. Useful when dealing with sequence of sequences, see :func:`concat` or :func:`iconcat` to join just a few sequences.

    Flattening of various nested sequences is most common use::

        # flatten two level deep list
        cat(list_of_lists)

        # get a flat html of errors of a form
        errors = icat(inline.errors() for inline in form)
        error_text = '<br>'.join(errors)

        # brace expansion on product of sums
        # (a + b)(t + pq)x == atx + apqx + btx + bpqx
        terms = [['a', 'b'], ['t', 'pq'], ['x']]
        map(cat, product(*terms))
        # [list('atx'), list('apqx'), list('btx'), list('bpqx')]


    :func:`icat` is an alias for :meth:`itertools.chain.from_iterable`.


Transform and filter
--------------------

.. function:: remove(pred, seq)
              iremove(pred, seq)

    Return a list or an iterator of items of ``seq`` that result in false when passed to ``pred``. The results of this functions complement results of standard :func:`filter` and :func:`~itertools.ifilter`. The notable diffrence is that predicate can't be ``None``, use ``bool`` instead::

        remove(bool, [0, 1, 2, ''])
        # -> [0, '']

    Other handy use is passing :func:`re_tester` result as ``pred``. For example, this code removes any whitespace only lines from list::

        remove(re_tester('^\s+$'), lines)

    :func:`iremove` is an alias for :func:`itertools.ifilterfalse`.

.. function:: keep([f], seq)
              ikeep([f], seq)

    Maps ``seq`` with given function and then filters out falsy elements. Simply filters ``seq`` when ``f`` is absent. In fact these functions are just handy shortcuts::

        keep(f, seq)  == filter(bool, map(f, seq))
        keep(seq)     == filter(bool, seq)

        ikeep(f, seq) == ifilter(bool, imap(f, seq))
        ikeep(seq)    == ifilter(bool, seq)

    Natural use case for :func:`keep` is data extraction or recognition that could eventually fail::

        # Extract numbers from words:
        keep(re_finder(r'\d+'), words)

        # Recognize as many colors by name as possible:
        keep(COLOR_BY_NAME.get, color_names)

    An iterator version can be useful when you don't need or not sure you need the whole sequence. For example, you can use :func:`first` - :func:`ikeep` combo to find out first match::

        first(ikeep(COLOR_BY_NAME.get, color_name_candidates))

    Alternatively, you can do the same with :func:`some` and :func:`~itertools.imap`.

    One argument variant is a simple tool to keep your data free of falsy junk. This one returns non-empty description lines::

        keep(description.splitlines())

    Other common case is using generator expression instead of mapping function. Consider these two lines::

        keep(f.name for f in fields)     # sugar generator expression
        keep(attrgetter('name'), fields) # pure functions


.. function:: mapcat(f, *seqs)
              imapcat(f, *seqs)

    Maps given sequence(s) and then concatenates them, essentially a shortcut for ``cat(map(f, *seqs))``. Come in handy when extracting multiple values from every sequence item or transforming nested sequences::

        # Get all the lines of all the texts in single flat list:
        mapcat(str.splitlines, bunch_of_texts)

        # Extract all numbers from strings:
        mapcat(partial(re_all, r'\d+'), bunch_of_strings)


Sequence mangling
-----------------

.. function:: interleave(*seqs)

    Returns an iterator yielding first item in each sequence, then second and so on until some sequence ends. Numbers of items taken from all sequences are always equal.

.. function:: interpose(sep, seq)
.. function:: dropwhile(pred, seq)
.. function:: takewhile(pred, seq)


Data mangling
-------------

.. function:: distinct(seq)
.. function:: split(at, seq)
.. .. function:: isplit(at, seq)
.. function:: groupby(f, seq)
.. function:: partition(n, [step], seq)
.. function:: chunks(n, [step], seq)

