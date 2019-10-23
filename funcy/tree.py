from collections import deque
from .types import is_seqcont
from .seqs import lflatten


__all__ = ['tree_leaves', 'ltree_leaves', 'tree_nodes', 'ltree_nodes', 'tree_keys', 'ltree_keys']


def tree_leaves(root, follow=is_seqcont, children=iter):
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

def ltree_leaves(root, follow=is_seqcont, children=iter):
    """Lists tree leaves."""
    return list(tree_leaves(root, follow, children))


def tree_nodes(root, follow=is_seqcont, children=iter):
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

def ltree_nodes(root, follow=is_seqcont, children=iter):
    """Lists all tree nodes."""
    return list(tree_nodes(root, follow, children))


def tree_keys(payload, parent=None):
    """Iterates of all keys within a dict and returns a list of nested keys"""
    q = deque(payload.keys())
    while q:
        node = q.pop()
        trail = []
        if parent:
            trail.append(parent)
        trail.append(node)
        yield lflatten(trail)
        child = payload.get(node)
        if isinstance(child, dict):
            yield from tree_keys(child, parent=trail)


def ltree_keys(payload):
    """List version of tree_keys"""
    return list(tree_keys(payload))
