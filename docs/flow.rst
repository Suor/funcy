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
