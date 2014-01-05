Python 3 support
================

Funcy works with python 3 as of version 0.9. However, it has slightly different interface. It follows python 3 convention of "iterator by default" for utilities like :func:`map`, :func:`filter` and such. When funcy has two versions of utility (list and iterator) they are named like :func:`keep` and :func:`ikeep` in python 2 and :func:`lkeep` and :func:`keep` in python 3. You can look up a full table of differently named functions below.


Writing cross-python code
-------------------------

You can do that two ways: writing python 2 code that works in python 3 or vice versa. You can import python 2 or 3 style functions from ``funcy.py2`` or ``funcy.py3``::

    from funcy.py2 import whatever, you, need

    # write python 2 style code here

::

    from funcy.py3 import whatever, you, need

    # write python 3 style code here

You can even import :func:`map`, :func:`imap`, :func:`filter`, :func:`ifilter`, :func:`zip` and :func:`~itertools.izip`.


Full table of python dependent function names
---------------------------------------------

======================  ======================= ===================== ==========================
Python 2 / list         Python 2 / iterator     Python 3 / list       Python 3 / iterator
======================  ======================= ===================== ==========================
:func:`map`             :func:`imap`            :func:`lmap`          :func:`map`
:func:`filter`          :func:`ifilter`         :func:`lfilter`       :func:`filter`
:func:`zip` (built-in)  :func:`~itertools.izip` :func:`lzip`          :func:`py3:zip` (built-in)
:func:`remove`          :func:`iremove`         :func:`lremove`       :func:`remove`
:func:`keep`            :func:`ikeep`           :func:`lkeep`         :func:`keep`
:func:`without`         :func:`iwithout`        :func:`lwithout`      :func:`without`

:func:`concat`          :func:`iconcat`         :func:`lconcat`       :func:`concat`
:func:`cat`             :func:`icat`            :func:`lcat`          :func:`cat`
:func:`flatten`         :func:`iflatten`        :func:`lflatten`      :func:`flatten`
:func:`mapcat`          :func:`imapcat`         :func:`lmapcat`       :func:`mapcat`

:func:`distinct`        :func:`idistinct`       :func:`ldistinct`     :func:`distinct`
:func:`split`           :func:`isplit`          :func:`lsplit`        :func:`split`
:func:`split_at`        :func:`isplit_at`       :func:`lsplit_at`     :func:`split_at`
:func:`split_by`        :func:`isplit_by`       :func:`lsplit_by`     :func:`split_by`
:func:`partition`       :func:`ipartition`      :func:`lpartition`    :func:`partition`
:func:`chunks`          :func:`ichunks`         :func:`lchunks`       :func:`chunks`
:func:`partition_by`    :func:`ipartition_by`   :func:`lpartition_by` :func:`partition_by`

:func:`reductions`      :func:`ireductions`     :func:`lreductions`   :func:`reductions`
:func:`sums`            :func:`isums`           :func:`lsums`         :func:`sums`

:func:`juxt`            :func:`ijuxt`           :func:`ljuxt`         :func:`juxt`

:func:`where`           *-*                     *-*                   :func:`where`
:func:`pluck`           *-*                     *-*                   :func:`pluck`
:func:`invoke`          *-*                     *-*                   :func:`invoke`

*-*                     :func:`izip_values`     *-*                   :func:`zip_values`
*-*                     :func:`izip_dicts`      *-*                   :func:`zip_dicts`
======================  ======================= ===================== ==========================
