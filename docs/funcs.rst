Functions
=========

.. function:: identity(x)

    Returns its argument.


.. function:: constantly(x)

    Returns function accepting any args, but always returning ``x``.


.. function:: caller(*args, **kwargs)

    Returns function calling its argument with passed arguments.


.. function:: partial(func, *args, **kwargs)

    Returns partial application of ``func``. A re-export of :func:`py3:functools.partial`. Can be used in a variety of ways. DSLs is one of them::

        field = dict
        json_field = partial(field, json=True)


.. function:: rpartial(func, *args)

    Partially applies last arguments in ``func``::

        from operator import div
        one_third = rpartial(div, 3.0)

    Arguments are passed to ``func`` in the same order as they came to :func:`rpartial`::

        separate_a_word = rpartial(str.split, ' ', 1)


.. function:: func_partial(func, *args, **kwargs)

    Like :func:`partial` but returns a real function. Which is useful when, for example, you want to create a method of it::

        setattr(self, 'get_%s_display' % field.name,
                func_partial(_get_FIELD_display, field))

    Use :func:`partial` if you are ok to get callable object instead of function as it's faster.


.. function:: curry(func[, n])

    Curries function. For example, given function of two arguments ``f(a, b)`` returns function::

        lambda a: lambda b: f(a, b)

    Handy to make a partial factory::

        make_tester = curry(re_test)
        is_word = make_tester(r'^\w+$')
        is_int = make_tester(r'^[1-9]\d*$')

    But see :func:`re_tester` if you need this particular one.


.. function:: rcurry(func[, n])

    Curries function from last argument to first::

        has_suffix = rcurry(str.endswith, 2)
        lfilter(has_suffix("ce"), ["nice", "cold", "ice"])
        # -> ["nice", "ice"]

    Can fix number of arguments when it's ambiguous::

        to_power = rcurry(pow, 2) # curry 2 first args in reverse order
        to_square = to_power(2)
        to_cube = to_power(3)


.. function:: autocurry(func)

    Constructs a version of ``func`` returning its partial applications until sufficient arguments are passed::

        def remainder(what, by):
            return what % by
        rem = autocurry(remainder)

        assert rem(10, 3) == rem(10)(3) == rem()(10, 3) == 1
        assert map(rem(by=3), range(5)) == [0, 1, 2, 0, 1]

    Can clean your code a bit when :func:`partial` makes it too cluttered.


.. function:: compose(*fs)

    Returns composition of functions::

        extract_int = compose(int, r'\d+')

    Supports :ref:`extended_fns`.


.. function:: rcompose(*fs)

    Returns composition of functions, with functions called from left to right. Designed to facilitate transducer-like pipelines::

        # Note the use of iterator function variants everywhere
        process = rcompose(
            partial(remove, is_useless),
            partial(map, process_row),
            partial(chunks, 100)
        )

        for chunk in process(data):
            write_chunk_to_db(chunk)

    Supports :ref:`extended_fns`.


.. function:: juxt(*fs)
              ljuxt(*fs)

    Takes several functions and returns a new function that is the juxtaposition of those. The resulting function takes a variable number of arguments, and returns an iterator or a list containing the result of applying each function to the arguments.


.. function:: iffy([pred], action, [default=identity])

    Returns function, which conditionally, depending on ``pred``, applies ``action`` or  ``default``. If ``default`` is not callable then it is returned as is from resulting function. E.g. this will call all callable values leaving rest of them as is::

        map(iffy(callable, caller()), values)

    Common use it to deal with messy data::

        dirty_data = ['hello', None, 'bye']
        lmap(iffy(len), dirty_data)              # => [5, None, 3]
        lmap(iffy(isa(str), len, 0), dirty_data) # => [5, 0, 3], also safer

    See also :func:`silent` for easier use cases.


Function logic
--------------

This family of functions supports creating predicates from other predicates and regular expressions.


.. function:: complement(pred)

    Constructs a negation of ``pred``, i.e. a function returning a boolean opposite of original function::

        is_private = re_tester(r'^_')
        is_public = complement(is_private)

        # or just
        is_public = complement(r'^_')


.. function:: all_fn(*fs)
              any_fn(*fs)
              none_fn(*fs)
              one_fn(*fs)

    Construct a predicate returning ``True`` when all, any, none or exactly one of ``fs`` return ``True``. Support short-circuit behavior.

    ::

        is_even_int = all_fn(isa(int), even)



.. function:: some_fn(*fs)

    Constructs function calling ``fs`` one by one and returning first true result.

    Enables creating functions by short-circuiting several behaviours::

        get_amount = some_fn(
            lambda s: 4 if 'set of' in s else None,
            r'(\d+) wheels?',
            compose({'one': 1, 'two': 2, 'pair': 2}, r'(\w+) wheels?')
        )

    If you wonder how on Earth one can :func:`compose` dict and string see :ref:`extended_fns`.


.. raw:: html
    :file: descriptions.html
