Flow
====

.. decorator:: ignore(errors, [default])


.. decorator:: silent

    Ignore all real exceptions.


.. decorator:: retry(tries, errors=Exception)


.. function:: fallback(*approaches)


..
    def limit_error_rate(fails, timeout, exception=ErrorRateExceeded):
    """
    If function fails to complete `fails` times in a row,
    calls to it will be intercepted for `timeout` with `exception` raised instead.
    """

.. decorator:: collecting

    Transforms generator or other iterator returning function into list returning one.

    Handy to prevent quirky properties::

        @property
        @collecting
        def path_up(self):
            node = self
            while node:
                yield node
                node = node.parent

    Or you could just write::

        @property
        def path_up(self):
            going_up = iterate(attrgetter('parent'), self)
            return list(takewhile(bool, going_up))


.. decorator:: joining(sep)

    Wraps common python idiom "collect then join" into a decorator. Transforms generator or alike into function, returning string of joined results. Automatically converts all elements to separator type for convenience.

    Goes well with generators with some ad-hoc logic within::

        @joining(', ')
        def car_desc(self):
            yield self.year_made
            if self.engine_volume: yield '%s cc' % self.engine_volume
            if self.transmission:  yield self.get_transmission_display()
            if self.gear:          yield self.get_gear_display()
            # ...

    Use ``unicode`` separator to get unicode result::

        @joining(u', ')
        def car_desc(self):
            yield self.year_made
            # ...

    See also :func:`str_join`.


.. .. decorator:: postprocessing(func)
