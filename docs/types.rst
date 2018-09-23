Type testing
============

.. function:: isa(*types)

    Returns function checking if its argument is of any of given ``types``.

    Split labels from ids::

        labels, ids = lsplit(isa(str), values)


.. function:: is_mapping(value)
              is_set(value)
              is_list(value)
              is_tuple(value)
              is_seq(value)
              is_iter(value)

    These functions check if value is ``Mapping``, ``Set``, ``list``, ``tuple``, ``Sequence`` or iterator respectively.


.. function:: is_seqcoll(value)

    Checks if ``value`` is a list or a tuple, which are both sequences and collections.


.. function:: is_seqcont(value)

    Checks if ``value`` is a list, a tuple or an iterator, which are sequential containers. It can be used to distinguish between value and multiple values in dual-interface functions::

        def add_to_selection(view, region):
            if is_seqcont(region):
                # A sequence of regions
                view.sel().add_all(region)
            else:
                view.sel().add(region)


.. function:: iterable(value)

    Tests if ``value`` is iterable.


.. raw:: html
    :file: descriptions.html
