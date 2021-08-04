class Range:
    def __init__(self, start, stop=None, step=1):
        if step == 0:
            raise ValueError('step cannot be 0')
        if stop is None:
            start, stop = 0, start
        self._length = max(0, (stop - start + step - 1)//step)

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

    def __contain__(self, value):
        factor, remainder = divmod((value - self._start), self._step)
        if remainder == 0:
            if factor < len(self) and factor >= 0: return True
            else: return False
        else:
            return False


def main():
    r = Range(start= 0, stop =-100, step = -1)
    for i in range(len(r)):
        print(r[i])


if __name__ == '__main__':
    main()