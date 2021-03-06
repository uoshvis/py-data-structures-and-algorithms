# running time is O(n+m) where m is number of inversions (number of pairs of elements out of order
# good for small sequences n < 50, and almost sorted
# O(n^2) outside of special contexts

def insertion_sort(A):
    """ Sort list of comparable elements into nondecreasing order. """
    for k in range(1, len(A)):      # from 1 no n-1
        cur = A[k]
        j = k
        while j > 0 and A[j-1] > cur:
            A[j] = A[j-1]
            j -= 1
        A[j] = cur


def insertion_sort(L):
    """Sort PositionalList of comparable elements into nondecreasing order."""
    if len(L) > 1:                  # otherwise, no need to sort it
        marker = L.first()
        while marker != L.last():
            pivot = L.after(marker) # next item to place
            value = pivot.element()
            if value > marker.element():    # pivot is already sorted
                marker = pivot              # pivot becomes new marker
            else:                           # must relocate pivot
                walk = marker               # find leftmost item greater than value
                while walk != L.first() and L.before(walk).element() > value:
                    walk = L.before(walk)
                L.delete(pivot)
                L.add_before(walk, value)
