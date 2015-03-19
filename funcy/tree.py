from collections import deque
from .types import is_seqcont


__all__ = ['itree_leaves', 'tree_leaves']


def itree_leaves(root, follow=is_seqcont, children=iter):
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

def tree_leaves(root, follow=is_seqcont, children=iter):
    return list(itree_leaves(root, follow, children))
