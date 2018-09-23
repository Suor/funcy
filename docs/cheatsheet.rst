.. raw:: html
    :file: _popups.html


.. _cheatsheet:

Cheatsheet
==========

Hover over function to get its description. Click to jump to docs.


Sequences
---------

========== ==============================================================
Create     :func:`count` :func:`cycle` :func:`repeat` :func:`repeatedly` :func:`iterate` :func:`re_all` :func:`re_iter`
Access     :func:`first` :func:`second` :func:`last` :func:`nth` :func:`some` :func:`take`
Slice      :func:`take` :func:`drop` :func:`rest` :func:`butlast` :func:`takewhile` :func:`dropwhile` :func:`split_at` :func:`split_by`
Transform  :func:`map` :func:`mapcat` :func:`keep` :func:`pluck` :func:`pluck_attr` :func:`invoke`
Filter     :func:`filter` :func:`remove` :func:`keep` :func:`distinct` :func:`where` :func:`without`
Join       :func:`cat` :func:`concat` :func:`flatten` :func:`mapcat` :func:`interleave` :func:`interpose`
Partition  :func:`chunks` :func:`partition` :func:`partition_by` :func:`split_at` :func:`split_by`
Group      :func:`split` :func:`count_by` :func:`count_reps` :func:`group_by` :func:`group_by_keys` :func:`group_values`
Aggregate  :func:`ilen` :func:`reductions` :func:`sums` :func:`all` :func:`any` :func:`none` :func:`one` :func:`count_by` :func:`count_reps`
Iterate    :func:`pairwise` :func:`with_prev` :func:`with_next` :func:`zip_values` :func:`zip_dicts` :func:`tree_leaves` :func:`tree_nodes`
========== ==============================================================


.. _colls:

Collections
-----------

===================== ==============================================================
Join                  :func:`merge` :func:`merge_with` :func:`join` :func:`join_with`
Transform             :func:`walk` :func:`walk_keys` :func:`walk_values`
Filter                :func:`select` :func:`select_keys` :func:`select_values` :func:`compact`
Dicts :ref:`*<colls>` :func:`flip` :func:`zipdict` :func:`pluck` :func:`where` :func:`itervalues` :func:`iteritems` :func:`zip_values` :func:`zip_dicts` :func:`project` :func:`omit`
Misc                  :func:`empty` :func:`get_in` :func:`set_in` :func:`update_in`
===================== ==============================================================


Functions
---------

.. :ref:`*<extended_fns>`

========== ==============================================================
Create     :func:`identity` :func:`constantly` :func:`func_partial` :func:`partial` :func:`rpartial` :func:`iffy` :func:`caller` :func:`re_finder` :func:`re_tester`
Transform  :func:`complement` :func:`iffy` :func:`autocurry` :func:`curry` :func:`rcurry`
Combine    :func:`compose` :func:`rcompose` :func:`juxt` :func:`all_fn` :func:`any_fn` :func:`none_fn` :func:`one_fn` :func:`some_fn`
========== ==============================================================


Other topics
------------

================== ==============================================================
Content tests      :func:`all` :func:`any` :func:`none` :func:`one` :func:`is_distinct`
Type tests         :func:`isa` :func:`is_iter` :func:`is_list` :func:`is_tuple` :func:`is_set` :func:`is_mapping` :func:`is_seq` :func:`is_seqcoll` :func:`is_seqcont` :func:`iterable`
Decorators         :func:`decorator<funcy.decorator>` :func:`wraps<funcy.wraps>` :func:`unwrap<funcy.unwrap>` :func:`autocurry`
Control flow       :func:`once` :func:`once_per` :func:`once_per_args` :func:`collecting` :func:`joining` :func:`post_processing`
Error handling     :func:`retry` :func:`silent` :func:`ignore` :func:`suppress` :func:`limit_error_rate` :func:`fallback` :func:`raiser` :func:`reraise`
Debugging          :func:`tap` :func:`log_calls` :func:`log_enters` :func:`log_exits` :func:`log_errors` :func:`log_durations` :func:`log_iter_durations`
Caching            :func:`memoize` :func:`cache` :func:`cached_property` :func:`make_lookuper` :func:`silent_lookuper`
Regexes            :func:`re_find` :func:`re_test` :func:`re_all` :func:`re_iter` :func:`re_finder` :func:`re_tester`
Strings            :func:`cut_prefix` :func:`cut_suffix` :func:`str_join`
Objects            :func:`cached_property` :func:`monkey` :func:`invoke` :func:`pluck_attr` :class:`namespace` :class:`LazyObject`
Primitives         :func:`isnone` :func:`notnone` :func:`inc` :func:`dec` :func:`even` :func:`odd`
================== ==============================================================


.. raw:: html
    :file: descriptions.html
