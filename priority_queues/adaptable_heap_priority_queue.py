from priorityQueueBase import PriorityQueueBase


class Empty(Exception):
    pass


# An implementation of a priority queue using array-based heap
class HeapPriorityQueue(PriorityQueueBase):
    # ---------- nonpublic behaviors --------------
    def _parent(self, j):
        return (j-1) // 2

    def _left(self, j):
        return 2*j + 1

    def _right(self, j):
        return 2*j + 2

    def _has_left(self, j):
        return self._left(j) < len(self._data)

    def has_right(self, j):
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent)

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child)

    # -------- public behaviors -------------

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def add(self, key, value):
        self._data.append(self._Item(key, value))
        self._upheap(len(self._data) - 1)

    def min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        item = self._data[0]
        return (item._key, item._value)

    def remove_min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        self._swap(0, len(self._data) - 1)
        item = self._data.pop()
        self._downheap(0)
        return (item._key, item._value)


# Provides the same asymptotic efficiency and space usage as nonadaptive version
# And provides logarithmic performance for the new locator-based update and remove methods
# space requirement: O(n)
class AdaptableHeapPriorityQueue(HeapPriorityQueue):

    class Locator(HeapPriorityQueue._Item):
        __slots__ = '_index'

        def __init__(self, k, v, j):
            super().__init__(k, v)
            self._index = j

    # -------- nonpublic behaviors -------
    # override swap to record new indices
    def _swap(self, i, j):
        super()._swap(i, j)
        self._data[i]._index = i
        self._data[j]._index = j

    def _bubble(self, j):
        if j > 0 and self._data[j] < self._data[self._parent(j)]:
            self._upheap(j)
        else:
            self._downheap(j)

    # O(log n)
    def add(self, key, value):
        ''' Add a key-value pair.'''
        token = self.Locator(key, value, len(self._data)) # initialize locator index
        self._data.append(token)
        self._upheap(len(self._data) - 1)
        return token

    # O(log n)
    def update(self, loc, newkey, newval):
        # Update the key and value for the entry identified by Locator loc.
        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')
        if j == len(self) - 1:  # item at last pos
            self._data.pop()    # just remove it
        else:
            self._swap(j, len(self) - 1)    # swap item to the last pos
            self._data.pop()    # remove it from the list
            self._bubble(j)    # fix item displaced by the swap
        return (loc._key, loc._value)
