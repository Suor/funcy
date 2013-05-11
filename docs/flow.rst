Flow
====

.. decorator:: silent

    Ignore all real exceptions (descendants of :class:`Exception`). Handy for cleaning data such as user input::


        brand_id = silent(int)(request.GET['brand_id'])
        ids = keep(silent(int), request.GET.getlist('id'))

    And in data import/transform::

        choices = {1: 'a', 2: ' b', 4: ' c '}
        get_caption = compose(silent(string.strip), choices)
        map(get_caption, [0, 1, 2, 3, 4])
        # -> [None, 'a', 'b', None, 'c']

    .. note:: avoid silencing non-primitive functions, use :func:`ignore` instead and even then be careful not to swallow exceptions unintentionally.


.. decorator:: ignore(errors, default=None)

    Same as :func:`silent`, but able to specify ``errors`` to catch and ``default`` to return in case of error catched. ``errors`` can either be exception class or tuple of them.


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
