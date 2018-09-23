Debugging
=========

.. function:: tap(value, label=None)

    Prints a value and then returns it. Useful to tap into some functional pipeline for debugging::

        fields = (f for f in fields_for(category) if section in tap(tap(f).sections))
        # ... do something with fields

    If ``label`` is specified then it's printed before corresponding value::

        squares = {tap(x, 'x'): tap(x * x, 'x^2') for x in [3, 4]}
        # x: 3
        # x^2: 9
        # x: 4
        # x^2: 16
        # => {3: 9, 4: 16}


.. decorator:: log_calls(print_func, errors=True, stack=True, repr_len=25)
               print_calls(errors=True, stack=True, repr_len=25)

    Will log or print all function calls, including arguments, results and raised exceptions. Can be used as a decorator or tapped into call expression::

        sorted_fields = sorted(fields, key=print_calls(lambda f: f.order))

    If ``errors`` is set to ``False`` then exceptions are not logged. This could be used to separate channels for normal and error logging::

        @log_calls(log.info, errors=False)
        @log_errors(log.exception)
        def some_suspicious_function(...):
            # ...
            return result


.. decorator:: log_enters(print_func, repr_len=25)
               print_enters(repr_len=25)
               log_exits(print_func, errors=True, stack=True, repr_len=25)
               print_exits(errors=True, stack=True, repr_len=25)

    Will log or print every time execution enters or exits the function. Should be used same way as :func:`@log_calls()<log_calls>` and :func:`@print_calls()<print_calls>` when you need to track only one event per function call.


.. decorator:: log_errors(print_func, label=None, stack=True, repr_len=25)
               print_errors(label=None, stack=True, repr_len=25)

    Will log or print all function errors providing function arguments causing them. If ``stack``
    is set to ``False`` then each error is reported with simple one line message.

    Can be combined with :func:`@silent<silent>` or :func:`@ignore()<ignore>` to trace occasionally misbehaving function::

        @ignore(...)
        @log_errors(logging.warning)
        def guess_user_id(username):
            initial = first_guess(username)
            # ...

    Can also be used as context decorator::

        with print_errors('initialization', stack=False):
            load_this()
            load_that()
            # ...
        # SomeException: a bad thing raised in initialization


.. decorator:: log_durations(print_func, label=None, unit='auto', threshold=None, repr_len=25)
               print_durations(label=None, unit='auto', threshold=None, repr_len=25)

    Will time each function call and log or print its duration::

        @log_durations(logging.info)
        def do_hard_work(n):
            samples = range(n)
            # ...

        # 121 ms in do_hard_work(10)
        # 143 ms in do_hard_work(11)
        # ...

    A block of code could be timed with a help of context manager::

        with print_durations('Creating models'):
            Model.objects.create(...)
            # ...

        # 10.2 ms in Creating models

    ``unit`` argument can be set to ``'ns'``, ``'mks'``, ``'ms'`` or ``'s'`` to use uniform time unit. If ``threshold`` is set then durations under this number of seconds are not logged. Handy to capture slow queries or API calls::

        @log_durations(logging.warning, threshold=0.5)
        def make_query(sql, params):
            # ...


.. function:: log_iter_durations(seq, print_func, label=None, unit='auto')
              print_iter_durations(seq, label=None, unit='auto')

    Wraps iterable ``seq`` into generator logging duration of processing of each item::


        for item in print_iter_durations(seq, label='hard work'):
            do_smth(item)

        # 121 ms in iteration 0 of hard work
        # 143 ms in iteration 1 of hard work
        # ...

    ``unit`` can be set to ``'ns'``, ``'mks'``, ``'ms'`` or ``'s'``.


.. raw:: html
    :file: descriptions.html
