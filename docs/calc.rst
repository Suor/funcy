Calculation
===========

.. decorator:: memoize

    Memoizes decorated function results, trading memory for performance. Can skip memoization
    for failed calculation attempts::

        @memoize
        def ip_to_city(ip):
            try:
                return request_city_from_slow_service(ip)
            except NotFound:
                return None        # return None and memoize it
            except Timeout:
                raise memoize.skip # return None, but don't memoize it

    Use ``raise memoize.skip(some_value)`` to make function return ``some_value`` on fail instead of ``None``.


.. decorator:: make_lookuper

    As :func:`memoize`, but with prefilled memory. Decorated function should return fully filled memory, resulting function will return ``None`` for any argument missing in it::

        @make_lookuper
        def city_location():
            return {row['city']: row['location'] for row in fetch_city_locations()}


.. decorator:: cache(timeout)

    ``timeout`` can be either number of seconds or :class:`datetime.timedelta`.
