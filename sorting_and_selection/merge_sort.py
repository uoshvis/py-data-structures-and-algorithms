import math

from linked_list.linkedQueue import LinkedQueue
from priority_queues.priorityQueueBase import PriorityQueueBase


# running time is O(n1+n2)
def merge(S1, S2, S):
    """Merge two sorted Python lists S1 and S2 into properly sized list S."""
    i = j = 0
    while i + j < len(S):
        if j == len(S2) or (i < len(S1) and S1[i] < S2[j]):
            S[i + j] = S1[i]                    # copy ith element of S1 as next item of S
            i += 1
        else:
            S[i+j] = S2[j]                      # copy jth element of S2 as next item of S
            j += 1


# O(n log n) if two elements of S can be compared in O(1) time
def merge_sort(S):
    """Sort the elements of Python list S using merge-sort algorithm"""
    n = len(S)
    if n < 2:
        return              # list is already sorted
    # divide
    mid = n // 2
    S1 = S[0:mid]           # copy of first half
    S2 = S[mid:n]           # copy of second half
    # conquer (with recursion)
    merge_sort(S1)          # sort copy of first half
    merge_sort(S2)          # sort copy of second half
    # merge results
    merge(S1, S2, S)        # merge sorted halves back into S


# merge sort based on use of the LinkedQueue class
def merge(S1, S2, S):
    """Merge two sorted queue instances S1 and S2 into empty queue S."""
    while not S1.is_empty() and not S2.is_empty():
        if S1.first() < S2.first():
            S.enqueue(S1.dequeue())
        else:
            S.enqueue(S2.dequeue())
    while not S1.is_empty():
        S.enqueue(S1.dequeue())
    while not S2.is_empty():
        S.enqueue(S2.dequeue())


def merge_sort(S):
    """Sort the elements of queue S using the merge-sort algorithm"""
    n = len(S)
    if n < 2:
        return
    # divide
    S1 = LinkedQueue()
    S2 = LinkedQueue()
    while len(S1) < n // 2:
        S1.enqueue(S.dequeue())
    while not S.is_empty():
         S2.enqueue(S.dequeue())
    # conquer (with recursion)
    merge_sort(S1)
    merge_sort(S2)
    # merge results
    merge(S1, S2, S)


# bottom-up merge sort - a bit faster than recursive merge-sort
def merge_bottom_up(src, result, start, inc):
    """Merge src[start:start+inc] and src[start+inc:start+2 inc] into result."""
    end1 = start + inc                  # boundary for run 1
    end2 = min(start+2*inc, len(src))   # boundary for run 2
    x, y, z = start, start+inc, start    # index into run 1, run 2, result
    while x < end1 and y < end2:
        if src[x] < src[y]:
            result[z] = src[x]          # copy from run 1 and increment x
            x += 1
        else:
            result[z] = src[y]          # copy from run 2 and increment y
            y += 1
        z += 1                          # increment z to reflect new result
    if x < end1:
        result[z:end2] = src[x:end1]   # copy remainder of run 1 to output
    elif y < end2:
        result[z:end2] = src[y:end2]    # copy remainder of run 2 to output


def merge_sort(S):
    """Sort the elements of Python list S using the merge-sort algorithm."""
    n = len(S)
    logn = math.ceil(math.log(n, 2))
    src, dest = S, [None] * n               # make temporary storage for dest
    for i in (2**k for k in range(logn)):   # pass i creates all runs of length 2i
        for j in range(0, n, 2*i):          # each pass merges two length i runs
            merge(src, dest, j, i)
        src, dest = dest, src               # reverse roles of lists
    if S is not src:
        S[0:n] = src[0:n]                   # additional copy to get results to S


# An approach for implementing the decorate-sort-undecorate pattern based upon the array-based merge-sort
def decorated_merge_sort(data, key=None):
    """Demonstration of the decorate-sort-undecorate pattern."""
    if key is not None:
        for j in range(len(data)):
            data[j] = PriorityQueueBase._Item(key(data[j]), data[j])  # decorate each element _Item is identical to PriorityQueueBase
        merge_sort(data)                            # sort with existing algorithm
    if key is not None:
        for j in range(len(data)):
            data[j] = data[j]._value                # undecorate each element
