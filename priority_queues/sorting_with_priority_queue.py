from heap_priority_queue import HeapPriorityQueue as PriorityQueue


def pq_sort(C):
    n = len(C)
    P = PriorityQueue()
    for j in range(n):
        element = C.delete(C.first())
        P.add(element, element)
    for j in range(n):
        (k, v) = P.remove_min()
        C.add_last(v)

'''
selection-sort

If P - unsorted list
Phase 1: O(n) = n * O(1) time to add each element
Phase 2: remove_min O(n^2) 
Bottleneck: repeated "selection" of min element in Phase 2 
'''

'''
insertion-sort

If P - sorted list
Phase 1: O(n^2)
Phase 2: n * O(1) = O(n)
best-case: O(n)
'''

'''
heap-sort

Phase 1: n * O(log(i)) = n*log(n)
Phase 2: O(n*log(n))
assuming two elements of C can be compared in O(1) time
'''