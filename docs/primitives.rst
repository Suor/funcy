Primitives
==========

.. function:: isnone(x)

    Checks if ``x`` is ``None``. Handy with filtering functions::

        _, data = lsplit_by(isnone, dirty_data) # Skip leading nones

    Plays nice with :func:`silent`, which returns ``None`` on fail::

        remove(isnone, map(silent(int), strings_with_numbers))

    Note that it's usually simpler to use :func:`keep` or :func:`compact` if you don't need to distinguish between ``None`` and other falsy values.


.. function:: notnone(x)

    Checks if ``x`` is not ``None``. A shortcut for ``complement(isnone)`` meant to be used when ``bool`` is not specific enough. Compare::

        select_values(notnone, data_dict) # removes None values
        compact(data_dict)                # removes all falsy values


.. function:: inc(x)

    Increments its argument by 1.


.. function:: dec(x)

    Decrements its argument by 1.


.. function:: even(x)

    Checks if ``x`` is even.


.. function:: odd(x)

    Checks if ``x`` is odd.


.. raw:: html
    :file: descriptions.html
