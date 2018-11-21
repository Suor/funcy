Sequences
=========

This functions are aimed at manipulating finite and infinite sequences of values. Some functions have two flavors: one returning list and other returning possibly infinite iterator, the latter ones follow convention of prepending ``i`` before list-returning function name.

When working with sequences, see also :mod:`py3:itertools` standard module. Funcy reexports and aliases some functions from it.


Generate
--------

.. function:: repeat(item, [n])

    Makes an iterator yielding ``item`` for ``n`` times or indefinitely if ``n`` is omitted. ``repeat`` simply repeats given value, when you need to reevaluate something repeatedly use :func:`repeatedly` instead.

    When you just need a length ``n`` list or tuple of ``item`` you can use::

        [item] * n
        # or
        (item,) * n

    .. Is a reexport of :func:`itertools.repeat`.


.. function:: count(start=0, step=1)

    Makes infinite iterator of values: ``start, start + step, start + 2*step, ...``.

    Could be used to generate sequence::

        map(lambda x: x ** 2, count(1))
        # -> 1, 4, 9, 16, ...

    Or annotate sequence using :func:`py3:zip`::

        zip(count(), 'abcd')
        # -> (0, 'a'), (1, 'b'), (2, 'c'), (3, 'd')

        # print code with BASIC-style numbered lines
        for line in zip(count(10, 10), code.splitlines()):
            print '%d %s' % line

    See also :func:`py3:enumerate` and original :func:`py3:itertools.count` documentation.


.. function:: cycle(seq)

    Cycles passed ``seq`` indefinitely returning its elements one by one.

    Useful when you need to cyclically decorate some sequence::

        for n, parity in zip(count(), cycle(['even', 'odd'])):
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

        step = lambda p: (p[0], sum(p))
        map(first, iterate(step, (0, 1)))
        # -> 0, 1, 1, 2, 3, 5, 8, ... (Fibonacci sequence)


Manipulate
----------

This section provides some robust tools for sequence slicing. Consider :ref:`py3:slicings` or :func:`py3:itertools.islice` for more generic cases.


.. function:: take(n, seq)

    Returns a list of the first ``n`` items in the sequence, or all items if there are fewer than ``n``.

    ::

        take(3, [2, 3, 4, 5]) # [2, 3, 4]
        take(3, count(5))     # [5, 6, 7]
        take(3, 'ab')         # ['a', 'b']


.. function:: drop(n, seq)

    Skips first ``n`` items in the sequence, returning iterator yielding rest of its items.

    ::

        drop(3, [2, 3, 4, 5]) # iter([5])
        drop(3, count(5))     # count(8)
        drop(3, 'ab')         # empty iterator


.. function:: first(seq)

    Returns the first item in the sequence. Returns ``None`` if the sequence is empty. Typical usage is choosing first of some generated variants::

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

    Other common use case is passing to :func:`map` or :func:`lmap`. See last example in :func:`iterate` for such example.


.. function:: second(seq)

    Returns the second item in given sequence. Returns ``None`` if there are less than two items in it.

    Could come in handy with sequences of pairs, e.g. :meth:`py3:dict.items`. Following code extract values of a dict sorted by keys::

        map(second, sorted(some_dict.items()))

    And this line constructs an ordered by value dict from a plain one::

        OrderedDict(sorted(plain_dict.items(), key=second))


.. function:: nth(n, seq)

    Returns nth item in sequence or ``None`` if no one exists. Items are counted from 0, so it's like indexed access but works for iterators. E.g. here is how one can get 6th line of `some_file`::

        nth(5, repeatedly(open('some_file').readline))


.. function:: last(seq)

    Returns the last item in the sequence. Returns ``None`` if the sequence is empty. Tries to be efficient when sequence supports indexed or reversed access and fallbacks to iterating over it if not.


.. function:: rest(seq)

    Skips first item in the sequence, returning iterator starting just after it. A shortcut for :func:`drop(1, seq) <drop>`.


.. function:: butlast(seq)

    Returns an iterator of all elements of the sequence but last.


.. function:: ilen(seq)

    Calculates length of iterator. Will consume it or hang up if it's infinite.

    Especially useful in conjunction with filtering or slicing functions, for example, this way one can find common start length of two strings::

        ilen(takewhile(lambda (x, y): x == y, zip(s1, s2)))


Unite
-----

.. function:: concat(*seqs)
              lconcat(*seqs)

    Concats several sequences into single iterator or list.

    :func:`concat` is an alias for :func:`py3:itertools.chain`.


.. function:: cat(seqs)
              lcat(seqs)

    Concatenates passed sequences. Useful when dealing with sequence of sequences, see :func:`concat` or :func:`lconcat` to join just a few sequences.

    Flattening of various nested sequences is most common use::

        # Flatten two level deep list
        lcat(list_of_lists)

        # Get a flat html of errors of a form
        errors = cat(inline.errors() for inline in form)
        error_text = '<br>'.join(errors)

        # Brace expansion on product of sums
        # (a + b)(t + pq)x == atx + apqx + btx + bpqx
        terms = [['a', 'b'], ['t', 'pq'], ['x']]
        lmap(lcat, product(*terms))
        # [list('atx'), list('apqx'), list('btx'), list('bpqx')]


    :func:`cat` is an alias for :meth:`py3:itertools.chain.from_iterable`.


.. function:: flatten(seq, follow=is_seqcont)
              lflatten(seq, follow=is_seqcont)

    Flattens arbitrary nested sequence of values and other sequences. ``follow`` argument determines whether to unpack each item. By default it dives into lists, tuples and iterators, see :func:`is_seqcont` for further explanation.

    See also :func:`cat` or :func:`lcat` if you need to flatten strictly two-level sequence of sequences.


.. function:: tree_leaves(root, follow=is_seqcont, children=iter)
              ltree_leaves(root, follow=is_seqcont, children=iter)

    A way to iterate or list over all the tree leaves. E.g. this is how you can list all descendants of a class::

        ltree_leaves(Base, children=type.__subclasses__, follow=type.__subclasses__)


.. function:: tree_nodes(root, follow=is_seqcont, children=iter)
              ltree_nodes(root, follow=is_seqcont, children=iter)

    A way to iterate or list over all the tree nodes. E.g. this is how you can iterate over all classes in hierarchy::

        tree_nodes(Base, children=type.__subclasses__, follow=type.__subclasses__)


.. function:: interleave(*seqs)

    Returns an iterator yielding first item in each sequence, then second and so on until some sequence ends. Numbers of items taken from all sequences are always equal.


.. function:: interpose(sep, seq)

    Returns an iterator yielding elements of ``seq`` separated by ``sep``.

    This is like :meth:`py3:str.join` for lists. This code is a part of a translator working with operation node::

        def visit_BoolOp(self, node):
            # ... do generic visit
            node.code = lmapcat(translate, interpose(node.op, node.values))


.. function:: lzip(*seqs)

    Joins given sequences into a list of tuples of corresponding first, second and later values. Essentially a list version of :func:`py3:zip` for Python 3.


Transform and filter
--------------------

Most of functions in this section support :ref:`extended_fns`. Among other things it allows to rewrite examples using :func:`re_tester` and :func:`re_finder` tighter.

.. function:: map(f, seq)
              lmap(f, seq)

    Extended versions of :func:`py3:map` and its list version.


.. function:: filter(pred, seq)
              lfilter(pred, seq)

    Extended versions of :func:`py3:filter` and its list version.


.. function:: remove(pred, seq)
              lremove(pred, seq)

    Returns an iterator or a list of items of ``seq`` that result in false when passed to ``pred``. The results of this functions complement results of :func:`filter` and :func:`lfilter`.

    A handy use is passing :func:`re_tester` result as ``pred``. For example, this code removes any whitespace-only lines from list::

        remove(re_tester('^\s+$'), lines)

    Note, you can rewrite it shorter using :ref:`extended_fns`::

        remove('^\s+$', lines)


.. function:: keep([f], seq)
              lkeep([f], seq)

    Maps ``seq`` with given function and then filters out falsy elements. Simply removes falsy items when ``f`` is absent. In fact these functions are just handy shortcuts::

        keep(f, seq)  == filter(bool, map(f, seq))
        keep(seq)     == filter(bool, seq)

        lkeep(f, seq) == lfilter(bool, map(f, seq))
        lkeep(seq)    == lfilter(bool, seq)

    Natural use case for :func:`keep` is data extraction or recognition that could eventually fail::

        # Extract numbers from words
        lkeep(re_finder(r'\d+'), words)

        # Recognize as many colors by name as possible
        lkeep(COLOR_BY_NAME.get, color_names)

    An iterator version can be useful when you don't need or not sure you need the whole sequence. For example, you can use :func:`first` - :func:`keep` combo to find out first match::

        first(keep(COLOR_BY_NAME.get, color_name_candidates))

    Alternatively, you can do the same with :func:`some` and :func:`map`.

    One argument variant is a simple tool to keep your data free of falsy junk. This one returns non-empty description lines::

        keep(description.splitlines())

    Other common case is using generator expression instead of mapping function. Consider these two lines::

        keep(f.name for f in fields)     # sugar generator expression
        keep(attrgetter('name'), fields) # pure functions


.. function:: mapcat(f, *seqs)
              lmapcat(f, *seqs)

    Maps given sequence(s) and then concatenates results, essentially a shortcut for ``cat(map(f, *seqs))``. Come in handy when extracting multiple values from every sequence item or transforming nested sequences::

        # Get all the lines of all the texts in single flat list
        mapcat(str.splitlines, bunch_of_texts)

        # Extract all numbers from strings
        mapcat(partial(re_all, r'\d+'), bunch_of_strings)


.. function:: without(seq, *items)
              lwithout(seq, *items)

    Returns sequence with ``items`` removed, preserves order.
    Designed to work with a few ``items``, this allows removing unhashable objects::

        non_empty_lists = without(lists, [])

    In case of large amount of unwanted elements one can use :func:`remove`::

        remove(set(unwanted_elements), seq)

    Or simple set difference if order of sequence is irrelevant.


Split and chunk
---------------

.. function:: split(pred, seq)
              lsplit(pred, seq)

    Splits sequence items which pass predicate from the ones that don't, essentially returning a tuple ``filter(pred, seq), remove(pred, seq)``.

    For example, this way one can separate private attributes of an instance from public ones::

        private, public = lsplit(re_tester('^_'), dir(instance))

    Split absolute and relative urls using extended predicate semantics::

        absolute, relative = lsplit(r'^http://', urls)


.. function:: split_at(n, seq)
              lsplit_at(n, seq)

    Splits sequence at given position, returning a tuple of its start and tail.


.. function:: split_by(pred, seq)
              lsplit_by(pred, seq)

    Splits start of sequence, consisting of items passing predicate, from the rest of it. Works similar to ``takewhile(pred, seq), dropwhile(pred, seq)``, but works with iterator ``seq`` correctly::

        lsplit_by(bool, iter([-2, -1, 0, 1, 2]))
        # [-2, -1], [0, 1, 2]


.. function:: takewhile([pred], seq)

    Yeilds elements of ``seq`` as long as they pass ``pred``. Stops on first one which makes predicate falsy::

        # Extract first paragraph of text
        takewhile(re_tester(r'\S'), text.splitlines())

        # Build path from node to tree root
        takewhile(bool, iterate(attrgetter('parent'), node))


.. function:: dropwhile([pred], seq)

    This is a mirror of :func:`takewhile`. Skips elements of given sequence while ``pred`` is true and yields the rest of it::

        # Skip leading whitespace-only lines
        dropwhile(re_tester('^\s*$'), text_lines)


.. function:: group_by(f, seq)

    Groups elements of ``seq`` keyed by the result of ``f``. The value at each key will be a list of the corresponding elements, in the order they appear in ``seq``. Returns :class:`defaultdict(list) <py3:collections.defaultdict>`.

    ::

        stats = group_by(len, ['a', 'ab', 'b'])
        stats[1] # -> ['a', 'b']
        stats[2] # -> ['ab']
        stats[3] # -> [], since stats is defaultdict

    One can use :func:`split` when grouping by boolean predicate. See also :func:`py3:itertools.groupby`.


.. function:: group_by_keys(get_keys, seq)

    Groups elements of ``seq`` having multiple keys each into :class:`defaultdict(list) <py3:collections.defaultdict>`. Can be used to reverse grouping::

        posts_by_tag = group_by_keys(attrgetter('tags'), posts)
        sentences_with_word = group_by_keys(str.split, sentences)


.. function:: group_values(seq)

    Groups values of ``(key, value)`` pairs. May think of it like ``dict()`` but collecting collisions:

    ::

        group_values(keep(r'^--(\w+)=(.+)', sys.argv))


.. function:: partition(n, [step], seq)
              lpartition(n, [step], seq)

    Iterates or lists over partitions of ``n`` items, at offsets ``step`` apart. If ``step`` is not supplied, defaults to ``n``, i.e. the partitions do not overlap. Returns only full length-``n`` partitions, in case there are not enough elements for last partition they are ignored.

    Most common use is deflattening data::

        # Make a dict from flat list of pairs
        dict(partition(2, flat_list_of_pairs))

        # Structure user credentials
        {id: (name, password) for id, name, password in partition(3, users)}

    A three argument variant of :func:`partition` can be used to process sequence items in context of their neighbors::

        # Smooth data by averaging out with a sliding window
        [sum(window) / n for window in partition(n, 1, data_points)]

    Also look at :func:`pairwise` for similar use. Other use of :func:`partition` is processing sequence of data elements or jobs in chunks, but take a look at :func:`chunks` for that.



.. function:: chunks(n, [step], seq)
              lchunks(n, [step], seq)

    Like :func:`partition`, but may include partitions with fewer than ``n`` items at the end::

        chunks(2, 'abcde')
        # -> 'ab', 'cd', 'e'

        chunks(2, 4, 'abcde')
        # -> 'ab', 'e'

    Handy for batch processing.

.. function:: partition_by(f, seq)
              lpartition_by(f, seq)

    Partition ``seq`` into list of lists or iterator of iterators splitting at ``f(item)`` change.


Data handling
-------------

.. function:: distinct(seq, key=identity)
              ldistinct(seq, key=identity)

    Returns unique items of the sequence with order preserved. If ``key`` is supplied then distinguishes values by comparing their keys.

    .. note:: Elements of a sequence or their keys should be hashable.


.. function:: with_prev(seq, fill=None)

    Returns an iterator of a pair of each item with one preceding it. Yields `fill` or `None` as preceding element for first item.

    Great for getting rid of clunky ``prev`` housekeeping in for loops. This way one can indent first line of each paragraph while printing text::

        for line, prev in with_prev(text.splitlines()):
            if not prev:
                print '    ',
            print line

    Use :func:`pairwise` to iterate only on full pairs.


.. function:: with_next(seq, fill=None)

    Returns an iterator of a pair of each item with one next to it. Yields `fill` or `None` as next element for last item. See also :func:`with_prev` and :func:`pairwise`.


.. function:: pairwise(seq)

    Yields pairs of items in ``seq`` like ``(item0, item1), (item1, item2), ...``. A great way to process sequence items in a context of each neighbor::

        # Check if seq is non-descending
        all(left <= right for left, right in pairwise(seq))


.. function:: count_by(f, seq)

    Counts numbers of occurrences of values of ``f`` on elements of ``seq``. Returns :class:`defaultdict(int) <py3:collections.defaultdict>` of counts.

    Calculating a histogram is one common use::

        # Get a length histogram of given words
        count_by(len, words)


.. function:: count_reps(seq)

    Counts number of repetitions of each value in ``seq``. Returns :class:`defaultdict(int) <py3:collections.defaultdict>` of counts. This is faster and shorter alternative to ``count_by(identity, ...)``


.. function:: reductions(f, seq, [acc])
              lreductions(f, seq, [acc])

    Returns a sequence of the intermediate values of the reduction of ``seq`` by ``f``. In other words it yields a sequence like::

        reduce(f, seq[:1], [acc]), reduce(f, seq[:2], [acc]), ...

    You can use :func:`sums` or :func:`lsums` for a common use of getting list of partial sums.


.. function:: sums(seq, [acc])
              lsums(seq, [acc])

    Same as :func:`reductions` or :func:`lreductions` with reduce function fixed to addition.

    Find out which straw will break camels back::

        first(i for i, total in enumerate(sums(straw_weights))
                if total > camel_toughness)


.. function:: fixpoint(f, x)

   Finds the fixed point of ``x`` under ``f``, i.e. the ``y`` such that ``y = f^n(x) = f^(n+1)(x)``.  NB: it will not terminate if no fixed point exists.

.. raw:: html
    :file: descriptions.html
