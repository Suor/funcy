def join_by(op, dicts, start=EMPTY):
    dicts = list(dicts)
    if not dicts:
        return {}
    elif len(dicts) == 1:
        return dicts[0]

    result = {}
    for d in dicts:
        for k, v in iteritems(d):
            if k in result:
                result[k] = op(result[k], v)
            else:
                result[k] = v if start is EMPTY else op(start, v)
                # result[k] = v if start is EMPTY else start(v)
                # result[k] = v if start is EMPTY else op(start(), v)
                # result[k] = v if start is EMPTY else op(start() if callable(start) else start, v)

    return result

join_by(operator.__add__, dnfs, start=list)
join_with(cat, dnfs)
join_by(list.extend, dnfs, start=list)
join_by(lambda c, _: c + 1, dnfs, start=lambda _: 1)
join_by(lambda l, v: l + len(v), dnfs, start=len)
# join_by(list.append, dnfs, initial=[])

join_by(lambda l, v: l + len(v), dnfs, 0)
