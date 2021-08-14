from collections.abc import MutableSet

'''
The MutableSet base class provides concrete implementations for all needed methods except for
add, discard,__contains__, __len__, and __iter__ must be implemented by concrete subclass
Template method pattern - as the concrete methods of the MutableSet
class rely on the presumed abstract methods that will subsequently be provided by
a subclass
'''


class MySet(MutableSet):

    def __lt__(self, other):
        if len(self) >= len(other):
            return False
        for e in self:
            if e not in other:
                return False
        return True

    def __or__(self, other):
        result = type(self)()   # create new instance of concrete class
        for e in self:
            result.add(e)
        for e in other:
            result.add(e)
        return result

    def __ior__(self, other):
        for e in other:
            self.add(e)
        return self


# Counter is in essence multiset
# Counter is a subclass of dict with values as integers + most_common(n)
