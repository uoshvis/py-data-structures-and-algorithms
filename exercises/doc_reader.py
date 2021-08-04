class DocumentReader:
    def __init__(self, filepath):
        self._filepath = filepath
        self._total = 0
        self._char_count = self._initialize_array()

        self._read_document()

    def _read_document(self):
        fp = open(self._filepath)
        all_text = fp.read().lower()
        for char in all_text:
            if self._check_if_character(char):
                self._char_count[ord(char) - ord('a')] += 1
        self._total = sum(self._char_count)

    def _initialize_array(self):
        return [0] * (ord('z') - ord('a') + 1)

    def _check_if_character(self, char):
        number = ord(char)
        if (number <= ord('z') and number >= ord('a')) or (number <= ord('Z') and number >= ord('A')):
            return True
        else:
            return False

    def output_graph(self):
        max_value = max(self._char_count)
        for i in range(len(self._char_count)):
            print(chr(i + ord('a')), 'X' * int(self._char_count[i] / max_value * 100))


def main():
    fpath = 'alice.txt'
    aiw = DocumentReader(fpath)
    aiw.output_graph()


if __name__ == '__main__':
    main()
