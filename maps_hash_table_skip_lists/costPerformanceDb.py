from sortedTableMap import SortedTableMap


class CostPerformanceDatabase:
    '''Maintain a database of maximal (cost,performance) pairs.'''
    def __init__(self):
        self._M = SortedTableMap()

    def best(self, c):
        return self._M.find_le(c)

    def add(self, c, p):
        other = self._M.find_le(c)  # other is at least as cheap as c
        if other is not None and other[1] >= p:  # is its performance is as good
            return  # (c,p) is dominated, so ignore
        self._M[c] = p  # else add to db
        # remove any pairs that are dominated by (c,p)
        other = self._M.find_gt(c)  # expensive than c
        while other is not None and other[1] <= p:
            del self._M[other[0]]
            other = self._M.find_gt(c)

# add has O(n) worst-case running time
