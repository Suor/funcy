from collections import deque
from .types import is_seqcont


__all__ = ['itree_leaves', 'tree_leaves', 'itree_nodes', 'tree_nodes']


def itree_leaves(root, follow=is_seqcont, children=iter):
    """Iterates over tree leaves."""
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
    """Lists tree leaves."""
    return list(itree_leaves(root, follow, children))


def itree_nodes(root, follow=is_seqcont, children=iter):
    """Iterates over all tree nodes."""
    q = deque([[root]])
    while q:
        node_iter = iter(q.pop())
        for sub in node_iter:
            yield sub
            if follow(sub):
                q.append(node_iter)
                q.append(children(sub))
                break

def tree_nodes(root, follow=is_seqcont, children=iter):
    """Lists all tree nodes."""
    return list(itree_nodes(root, follow, children))
