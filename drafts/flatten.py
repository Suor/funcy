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



def itree_leaves(root, follow=is_seqcont, children=iter):
    if follow(root):
        for node in children(root):
            # NOTE: can recur here, just an optimization
            if follow(node):
                for sub in itree_leaves(node, follow, children):
                    yield sub
            else:
                yield node
    else:
        yield root

def tree_leaves(root, follow=is_seqcont, children=iter):
    return list(itree_leaves(root, follow, children))


from collections import deque

def itree_leaves2(root, follow=is_seqcont, children=iter):
    if not follow(root):
        yield root
    else:
        q = deque([children(root)])
        while q:
            node_iter = iter(q.pop())
            for sub in node_iter:
                if follow(sub):
                    q.append(node_iter)
                    q.append(children(sub))
                    break
                else:
                    yield sub

def tree_leaves2(root, follow=is_seqcont, children=iter):
    return list(itree_leaves2(root, follow, children))

# NOTE: this suffers the least from depth
def itree_leaves3(root, follow=is_seqcont, children=iter):
    q = deque([[root]])
    while q:
        node_iter = iter(q.pop())
        for sub in node_iter:
            if follow(sub):
                q.append(node_iter)
                q.append(children(sub))
                break
            else:
                yield sub

def tree_leaves3(root, follow=is_seqcont, children=iter):
    return list(itree_leaves3(root, follow, children))


class Item(object):
    def __init__(self, data):
        self.data = data

def itree_leaves4(root, follow=is_seqcont, children=iter):
    q = deque([children(root) if follow(root) else Item(root)])
    while q:
        node = q.pop()
        if isinstance(node, Item):
            yield node.data
        else:
            it = iter(node)
            for sub in it:
                if follow(sub):
                    q.append(it)
                    q.append(children(sub))
                    break
                else:
                    yield sub

def tree_leaves4(root, follow=is_seqcont, children=iter):
    return list(itree_leaves4(root, follow, children))


# NOTE: this performs better on l = [[range(x) for x in range(10)]] * 10
from .seqs import icat, imap, imapcat

def itree_leaves5(root, follow=is_seqcont, children=iter):
    def _yield_chunks(seq):
        for key, group in groupby(seq, key=follow):
            if key:
                yield icat(_yield_chunks(imapcat(children, group)))
            else:
                yield group

    return icat(_yield_chunks([root]))

def tree_leaves5(root, follow=is_seqcont, children=iter):
    return list(itree_leaves5(root, follow, children))


def itree_leaves6(root, follow=is_seqcont, children=iter):
    chunks = [root]

    chunks = icat(
        imapcat(children, group) if key else group
        for key, group in groupby(seq, key=follow)
    )


    def _yield_chunks(seq):
        for key, group in groupby(seq, key=follow):
            if key:
                yield icat(_yield_chunks(imapcat(children, group)))
            else:
                yield group

    return icat(_yield_chunks([root]))

def tree_leaves6(root, follow=is_seqcont, children=iter):
    return list(itree_leaves6(root, follow, children))
