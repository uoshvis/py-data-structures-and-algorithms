class Range:
    """A class that mimic's the built-in range class."""

    def __init__(self, start, stop=None, step=None):
        """Initialize a Range Instance
        Semantics is similar to built-in range class
        """
        if step == 0:
            raise ValueError('step cannot be 0')

        if start < 0 and stop < 0 and step is None:
            step = - 1
        elif step is None:
            step = 1
        else:
            step = step

        if stop is None:
            start, stop = 0, start

        # the effective length

        end = (abs(stop - start) + abs(step) - 1) // abs(step)

        if start < 0 and stop < 0 and stop < start and step > 0:
            self._length = 0
        else:
            self._length = max(0, end)

        self._start = start
        self._step = step

    def __len__(self):
        return self._length

    def __getitem__(self, i):
        if i < 0:
            i += len(self)

        if not 0 <= i < self._length:
            raise IndexError('index is out of range')

        return self._start + i * self._step

    def __contains__(self, item):
        print(f'item {item} self {self[self._length-1]} step {self._step}')
        if ((item - self._start) % self._step == 0) and (item != (self[self._length-1] + self._step)):
            return True
        else:
            return False

    # def __contains__(self, value):
    #     factor, remainder = divmod((value - self._start), self._step)
    #     if remainder == 0:
    #         if factor < len(self) and factor >= 0:
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False


def main():
    r = Range(0, 16, 5)
    for i in range(len(r)):
        print(r[i])
    print(15 in r)

    print(9999998 in Range(2, 10000000, 2))


if __name__ == '__main__':
    main()
