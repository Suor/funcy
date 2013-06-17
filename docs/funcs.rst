Functions
=========

.. function:: identity(x)

    Returns its argument.


.. function:: constantly(x)

    Returns function accepting any args, but always returning ``x``.


.. function:: caller(*args, **kwargs)

    Returns function calling its argument with passed arguments.


.. function:: partial(func, *args, **kwargs)

    Like :func:`functools.partial` but returns real function. Which is useful when, for example, you want to create a method of it.


.. function:: curry(func[, n])

    Curries function. For example, given function of two arguments ``f(a, b)`` returns function::

        lambda a: lambda b: f(a, b)


.. function:: compose(*fs)
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
            compose(int, r'(\d+) wheels?'),
            compose({'one': 1, 'two': 2, 'pair': 2}, r'(\w+) wheels?')
        )

