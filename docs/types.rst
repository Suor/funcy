Type testing
============

.. function:: isa(*types):

    Returns function checking if it's argument is of any of given ``types``.

    Split labels from ids::

        labels, ids = split_by(isa(str), values)


.. function:: is_mapping(value)
              is_seq(value)
              is_list(value)
              is_iter(value)

    These functions check if value is ``Mapping``, ``Sequence``, ``list`` or iterator respectively.


.. function:: is_seqcoll(value)

    Checks if ``value`` is a list or a tuple.


.. function:: iterable(value)

    Tests if ``value`` is iterable.
