Functions
=========

.. function:: identity(x)

    Returns its argument.


.. function:: constantly(x)

    Returns function accepting any args, but always returning ``x``.


.. function:: caller(*args, **kwargs)

    Returns function calling its argument with passed arguments.


.. function:: partial(func, *args, **kwargs)

    A re-export of :func:`functools.partial`. Can be used in a variety of ways. DSLs is one of them::

        field = dict
        json_field = partial(field, json=True)


.. function:: func_partial(func, *args, **kwargs)

    Like :func:`partial` but returns a real function. Which is useful when, for example, you want to create a method of it::

        setattr(self, 'get_%s_display' % field.name, func_partial(_get_FIELD_display, field))

    Note: use :func:`partial` if you are ok to get callable object instead of function as it's faster.


.. function:: curry(func[, n])

    Curries function. For example, given function of two arguments ``f(a, b)`` returns function::

        lambda a: lambda b: f(a, b)

    Handy to make a partial factory::

        make_tester = curry(re_test)
        is_word = make_tester(r'^\w+$')
        is_int = make_tester(r'^[1-9]\d*$')

    But see :func:`re_tester` if you really need this.


.. function:: autocurry(func[, n])

    Constructs a version of ``func`` returning it's partial application if insufficient arguments passed::

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


.. function:: juxt(*fs)
.. function:: ijuxt(*fs)


Function logic
--------------

.. function:: complement(pred)

    ::

        is_private = re_tester('^_')
        is_public = complement(is_private)


.. function:: iffy([pred], action, [default=identity])

.. function:: all_fn(*fs)

    ::

        is_even_int = all_fn(isa(int), even)


.. function:: any_fn(*fs)
.. function:: none_fn(*fs)
.. function:: one_fn(*fs)

.. function:: some_fn(*fs)

    Constructs function calling ``fs`` one by one and returning first true result.

    Enables creating functions by short-circuiting several behaviours::

        get_amount = some_fn(
            lambda s: 4 if 'set of' in s else None,
            r'(\d+) wheels?',
            compose({'one': 1, 'two': 2, 'pair': 2}, r'(\w+) wheels?')
        )

