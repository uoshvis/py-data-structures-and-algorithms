# An example of prune-and-search design pattern
import random


def binary_search(data, target, low, high):
    """Return True if target is found in indicated portion of a Python list.
    The search only considers the portion from data[low] to data[high] inclusive.
    """
    if low > high:
        return False                        # interval is empty; no match
    else:
        mid = (low + high) // 2
        if target == data[mid]:             # found a matcha
            return True
        elif target < data[mid]:
            # recur on the portion left of the middle
            return binary_search(data, target, low, mid - 1)
        else:
            # recur on the portion right of the middle
            return binary_search(data, target, mid + 1, high)


# randomized quick-select algorithm
# runs in O(n) expected time, O(n^2) time in the worst case

def quick_select(S, k):
    """Return the kth smallest element of list S, for k from 1 to len(S)."""
    if len(S) == 1:
        return S[0]
    pivot = random.choice(S)            # pick random pivot element from S
    L = [x for x in S if x < pivot]
    E = [x for x in S if x == pivot]
    G = [x for x in S if pivot < x]
    if k <= len(L):
        return quick_select(L, k)       # kth smallest lies in L
    elif k <= len(L) + len(E):
        return pivot                    # kth smallest equal to pivot
    else:
        j = k - len(L) - len(E)         # new selection parameter
        return quick_select(G, j)       # kth smallest is jth in G
