Debugging
=========

.. function:: tap(value)

    Print value and then returns it. Useful to tap into some functional pipeline for debugging::

        fields = (f for f in fields_for(category) if section in tap(tap(f).sections))
        # ... do something with fields


.. decorator:: log_calls(print_func=print)
               print_calls

   Will log or print all function calls, including argument and result values. Can be used as decorator or tapped into call expression::

       sorted_fields = sorted(fields, key=print_calls(lambda f: f.order))


.. decorator:: log_errors(print_func=print)
               print_errors

    Will log or print all function errors.

    Can be combined with :func:`silent` or :func:`ignore` to trace occasionally misbehaving function::

        @silent
        @log_errors(logging.warning)
        def guess_user_id(username):
            # ...

