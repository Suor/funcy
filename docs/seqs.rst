Sequences
=========

This functions are aimed at manipulating finite and infinite sequences of values. Some functions have two flavors: one returning list and other returning possibly infinite iterator, the latter ones follow convention of prepending ``i`` before list-returning function name.

When working with sequences, see also :mod:`py:itertools` standard module. Funcy reexports and aliases some functions from it.


Generate
--------

.. function:: repeat(elem, [n])

    Makes an iterator returning ``elem`` for ``n`` times or indefinitely if ``n`` is omitted. :func:`repeat` simply repeat given value, when you need to reevaluate something repeatedly use :func:`repeatedly` instead.

    When you just need a length ``n`` list or tuple of ``elem`` you can use::

        [elem] * n
        # or
        (elem,) * n

    .. Is a reexport of :func:`itertools.repeat`.


.. function:: count(start=0, step=1)

    Makes infinite iterator of values: ``start, start + step, start + 2*step, ...``.

    Could be used to generate sequence::

        imap(lambda x: x ** 2, count(1))
        # -> 1, 4, 9, 16, ...

    Or annotate sequence using :func:`py:zip` or :func:`~itertools.izip`::

        zip(count(), 'abcd')
        # -> [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd')]

        # print code with BASIC-style numbered lines
        for line in izip(count(10, 10), code.splitlines()):
            print '%d %s' % line

    See also :func:`py:enumerate` and original :func:`py:itertools.count` documentation.


.. function:: cycle(seq)

    Cycles passed ``seq`` indefinitely returning its elements one by one.

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

This section provides some robust tools for sequence slicing. Consider :ref:`py:slicings` or :func:`py:itertools.islice` for more generic cases.


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

    Returns first item in sequence. Returns ``None`` if sequence is empty. Typical usage is choosing first of some generated variants::

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

    Could come in handy with sequences of pairs, e.g. :meth:`py:dict.items`. Following code extract values of a dict sorted by keys::

        map(second, sorted(some_dict.items()))

    And this line constructs an ordered by value dict from a plain one::

        OrderedDict(sorted(plain_dict.items(), key=second))


.. function:: nth(n, seq)

    Returns nth item in sequence or ``None`` if no one exists. Items are counted from 0, so it's like indexed access but works for iterators. E.g. here is how one can get 6th line of `some_file`::

        nth(5, repeatedly(open('some_file').readline))


.. function:: last(seq)

    Returns last item in sequence. Returns ``None`` if sequence is empty. Tries to be efficient when sequence supports indexed or reversed access and fallbacks to iterating over it if not.


.. function:: rest(seq)

    Skips first item in sequence, returning iterator starting just after it. A shortcut for :func:`drop(1, seq) <drop>`.


.. function:: butlast(seq)

    Returns iterator of all elements of a sequence but last.


.. function:: ilen(seq)

    Calculates length of iterator. Will consume it or hang up if it's infinite.

    Especially useful in conjunction with filtering or slicing functions, for example, this way one can find common start length of two strings::

        ilen(takewhile(lambda (x, y): x == y, zip(s1, s2)))


Unite
-----

.. function:: concat(*seqs)
              iconcat(*seqs)

    Concats several sequences into one. :func:`iconcat` returns an iterator yielding concatenation.

    :func:`iconcat` is an alias for :func:`py:itertools.chain`.


.. function:: cat(seqs)
              icat(seqs)

    Returns concatenation of passed sequences. Useful when dealing with sequence of sequences, see :func:`concat` or :func:`iconcat` to join just a few sequences.

    Flattening of various nested sequences is most common use::

        # Flatten two level deep list
        cat(list_of_lists)

        # Get a flat html of errors of a form
        errors = icat(inline.errors() for inline in form)
        error_text = '<br>'.join(errors)

        # Brace expansion on product of sums
        # (a + b)(t + pq)x == atx + apqx + btx + bpqx
        terms = [['a', 'b'], ['t', 'pq'], ['x']]
        map(cat, product(*terms))
        # [list('atx'), list('apqx'), list('btx'), list('bpqx')]


    :func:`icat` is an alias for :meth:`py:itertools.chain.from_iterable`.


.. function:: flatten(seq, follow=is_seqcont)
              iflatten(seq, follow=is_seqcont)

    Flattens arbitrary nested sequence of values and other sequences. ``follow`` argument determines whether to unpack each item. By default it dives into lists, tuples and iterators, see :func:`is_seqcont` for further explanation.

    See also :func:`cat` or :func:`icat` if you need to flatten strictly two-level sequence of sequences.


.. function:: interleave(*seqs)

    Returns an iterator yielding first item in each sequence, then second and so on until some sequence ends. Numbers of items taken from all sequences are always equal.


.. function:: interpose(sep, seq)

    Returns an iterator yielding elements of ``seq`` separated by ``sep``.

    Helpful when :meth:`py:str.join` is not good enough. This code is a part of translator working with operation node::

        def visit_BoolOp(self, node):
            # ... do generic visit
            node.code = mapcat(translate, interpose(node.op, node.values))


Transform and filter
--------------------

Most of functions in this section support :ref:`extended_fns`. Among other things it allows to rewrite examples using :func:`re_tester` and :func:`re_finder` tighter.

.. function:: map(pred, seq)
              imap(pred, seq)

    Extended versions of :func:`py:map` and :func:`~itertools.imap`.


.. function:: filter(pred, seq)
              ifilter(pred, seq)

    Extended versions of :func:`py:filter` and :func:`~itertools.ifilter`.


.. function:: remove(pred, seq)
              iremove(pred, seq)

    Return a list or an iterator of items of ``seq`` that result in false when passed to ``pred``. The results of this functions complement results of standard :func:`filter` and :func:`~itertools.ifilter`.

    A handy use is passing :func:`re_tester` result as ``pred``. For example, this code removes any whitespace-only lines from list::

        remove(re_tester('^\s+$'), lines)

    Note, you can rewrite it shorter using :ref:`extended_fns`::

        remove('^\s+$', lines)


.. function:: keep([f], seq)
              ikeep([f], seq)

    Maps ``seq`` with given function and then filters out falsy elements. Simply filters ``seq`` when ``f`` is absent. In fact these functions are just handy shortcuts::

        keep(f, seq)  == filter(bool, map(f, seq))
        keep(seq)     == filter(bool, seq)

        ikeep(f, seq) == ifilter(bool, imap(f, seq))
        ikeep(seq)    == ifilter(bool, seq)

    Natural use case for :func:`keep` is data extraction or recognition that could eventually fail::

        # Extract numbers from words
        keep(re_finder(r'\d+'), words)

        # Recognize as many colors by name as possible
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

    Maps given sequence(s) and then concatenates results, essentially a shortcut for ``cat(map(f, *seqs))``. Come in handy when extracting multiple values from every sequence item or transforming nested sequences::

        # Get all the lines of all the texts in single flat list
        mapcat(str.splitlines, bunch_of_texts)

        # Extract all numbers from strings
        mapcat(partial(re_all, r'\d+'), bunch_of_strings)


.. function:: without(seq, *items)
              iwithout(seq, *items)

    Returns sequence without ``items`` specified, preserves order. Designed to work with a few ``items``, this allows removing unhashable objects::

        no_empty_lists = without(lists, [])

    In case of large amount of unwanted elements one can use :func:`remove`::

        remove(set(unwanted_elements), seq)

    Or simple set difference if order of sequence is irrelevant.


Split and chunk
---------------

.. function:: split(pred, seq)
              isplit(pred, seq)

    Splits sequence items which pass predicate from ones that don't, essentially returning a tuple ``filter(pred, seq), remove(pred, seq)``.

    For example, this way one can separate private attributes of an instance from public ones::

        private, public = split(re_tester('^_'), dir(instance))

    Split absolute and relative urls::

        absolute, relative = split(re_tester(r'^http://'), urls)


.. function:: split_at(n, seq)
              isplit_at(n, seq)

    Splits sequence at given position, returning a tuple ``take(n, seq), list(drop(n, seq))``.


.. function:: split_by(pred, seq)
              isplit_by(pred, seq)

    Splits start of sequence, consisting of items passing predicate, from the rest of it. Works similar to ``takewhile(pred, seq), dropwhile(pred, seq)``, but returns lists and works with iterator ``seq`` correctly::

        split_by(bool, iter([-2, -1, 0, 1, 2]))
        # [-2, -1], [0, 1, 2]


.. function:: takewhile(pred, seq)

    Returns an iterator of ``seq`` elements as long as ``pred`` for each of them is true. Stop on first one which makes predicate falsy::

        # Extract first paragraph of text
        takewhile(re_tester(r'\S'), text.splitlines())

        # Build path from node to tree root
        takewhile(bool, iterate(attrgetter('parent'), node))


.. function:: dropwhile(pred, seq)

    This is a mirror of :func:`takewhile`. Returns iterator skipping elements of given sequence while ``pred`` is true and then yielding the rest of it::

        # Skip leading whitespace-only lines
        dropwhile(re_tester('^\s*$'), text_lines)


.. function:: group_by(f, seq)

    Groups elements of ``seq`` keyed by the result of ``f``. The value at each key will be a list of the corresponding elements, in the order they appear in ``seq``. Returns :class:`defaultdict(list) <py:collections.defaultdict>`.

    ::

        stats = group_by(len, ['a', 'ab', 'b'])
        stats[1] # -> ['a', 'b']
        stats[2] # -> ['ab']
        stats[3] # -> [], since stats is defaultdict

    One can use :func:`split` when grouping by boolean predicate. See also :func:`py:itertools.groupby`.


.. function:: group_by_keys(get_keys, seq)

    Groups elements of ``seq`` having multiple keys each into :class:`defaultdict(list) <py:collections.defaultdict>`. Can be used to reverse grouping::

        posts_by_tag = group_by_keys(attrgetter(tags), posts)
        sentences_with_word = group_by_keys(str.split, sentences)


.. function:: partition(n, [step], seq)
              ipartition(n, [step], seq)

    Returns a list of lists of ``n`` items each, at offsets ``step`` apart. If ``step`` is not supplied, defaults to ``n``, i.e. the partitions do not overlap. Returns only full length-``n`` partitions, in case there are not enough elements for last partition they are ignored.

    Most common use is deflattening data::

        # Make a dict from flat list of pairs
        dict(ipartition(2, flat_list_of_pairs))

        # Structure user credentials
        {id: (name, password) for id, name, password in ipartition(3, users)}

    A three argument variant of :func:`partition` can be used to process sequence items in context of their neighbors::

        # Smooth data by averaging out with a sliding window
        [sum(window) / n for window in ipartition(n, 1, data_points)]

    Also look at :func:`pairwise` for similar use. Other use of :func:`partition` is processing sequence of data elements or jobs in chunks, but take a look at :func:`chunks` for that.



.. function:: chunks(n, [step], seq)
              ichunks(n, [step], seq)

    Returns a list of lists like :func:`partition`, but may include partitions with fewer than ``n`` items at the end::

        chunks(2, 'abcde')
        # -> ['ab', 'cd', 'e'])

        chunks(2, 4, 'abcde')
        # -> ['ab', 'e'])

    Handy for batch processing.

.. function:: partition_by(f, seq)
              ipartition_by(f, seq)

    Partition ``seq`` into list of lists or iterator of iterators splitting at ``f(item)`` change.


Data handling
-------------

.. function:: distinct(seq, key=identity)
              idistinct(seq, key=identity)

    Returns given sequence with duplicates removed. Preserves order. If ``key`` is supplied then distinguishes values by comparing their keys.

    .. note:: Elements of a sequence or their keys should be hashable.


.. function:: with_prev(seq, fill=None)

    Returns an iterator of a pair of each item with one preceding it. Yields `fill` or `None` as preceding element for first item.

    Great for getting rid of clunky ``prev`` housekeeping in for loops. This way one can indent first line of each paragraph while printing text::

        for line, prev in with_prev(text.splitlines()):
            if not prev:
                print '    ',
            print line

    See also :func:`ipartition_by` and :func:`py:itertools.groupby` for chunking sequence by condition.

.. function:: pairwise(seq)

    Yields pairs of items in ``seq`` like ``(item0, item1), (item1, item2), ...``. A great way to process sequence items in a context of each neighbor::

        # Check if seq is non-descending
        all(left <= right for left, right in pairwise(seq))


.. function:: count_by(f, seq)

    Counts number of occurrences of values of ``f`` on elements of ``seq``. Returns :class:`defaultdict(int) <py:collections.defaultdict>` of counts.

    Calculating a histogram is one common use::

        # Get a length histogram of given words
        count_by(len, words)


.. function:: reductions(f, seq, [acc])
              ireductions(f, seq, [acc])

    Returns a sequence of the intermediate values of the reduction of ``seq`` by ``f``. In other words it yields a sequence like::

        reduce(f, seq[:1], [acc]), reduce(f, seq[:2], [acc]), ...

    You can use :func:`sums` or :func:`isums` for a common use of getting list of partial sums.


.. function:: sums(seq, [acc])
              isums(seq, [acc])

    Same as :func:`reductions` or :func:`ireductions` with reduce function fixed to addition.

    Find out which straw will break camels back::

        first(i for i, total in enumerate(isums(straw_weights))
                if total > camel_toughness)
