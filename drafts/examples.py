has_comment = re_tester(r'#')

value.value = walk_values(prepare, value.value)

json_field = partial(field, json=True)

re = lambda pattern: lambda value: re_test(pattern, value)
re = curry(re_test)

def translate_dict(d):
    lines = ('%s: %s' % (k, v) for k, v in walk_values(translate, d).items())
    return '{%s}' % ','.join(lines)

def _locals(func):
    if func.__closure__:
        names = func.__code__.co_freevars
        values = [cell.cell_contents for cell in func.__closure__]
        return zipdict(names, values)
    else:
        return {}

names = _code_names(code)
return merge(project(__builtins__, names), project(func.__globals__, names))

def closure(func):
    return merge(_globals(func), _locals(func))


names = chain.from_iterable(get_all_names(color))
try:
    return ifilter(None, imap(COLOR_BY_NAME.get, names)).next()
except StopIteration:
    return unknown()

etags = map(etag_from_response, responses)
etags = filter(None, etags)

phones = filter(None, map(stub_to_phone, _extract_stubs(text)))

return reduce(concat, map(extract_updates, rows))

op_js = ' %s ' % node.op.js
node.js = op_js.join(v.js for v in node.values)

' '.join(n.js for n in interpose(node.op, node.values))

mapcat(translate, interpose(node.op, node.values))
translate_items(interpose(node.op, node.values))

35:         while self.exists(name):
36              name = name_fmt % i
37              i += 1

users_cond = str_join(',', users)
tests = fetch_named('''
    select user_id, full_min, full_max, datetime from player_testtracking
    where %s and user_id in %s
    order by user_id, datetime
''' % (USEFUL_TEST_COND, users_cond))
get_pairs = partial(partition, 2, 1)
return mapcat(get_pairs, ipartition_by(itemgetter(0), tests))
