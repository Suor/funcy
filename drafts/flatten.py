def iflatten(seq, follow=is_seqcont):
    for item in seq:
        if follow(item):
            for sub in iflatten(item, is_seqcont):
                yield sub
        else:
            yield item

def iflatten2(seq, follow=is_seqcont):
    iters = [iter(seq)]
    while iters:
        try:
            item = next(iters[-1])
        except StopIteration:
            iters.pop()
            continue
        if follow(item):
            iters.append(iter(item))
        else:
            yield item

# This one is faster when deep nesting is involved
def iflatten3(seq, follow=is_seqcont):
    def _yield_chunks():
        for key, group in groupby(seq, key=follow):
            if key:
                yield iflatten3(icat(group), follow)
            else:
                yield group

    return icat(_yield_chunks())
