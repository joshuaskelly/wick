class MarkDownElement:
    def __init__(self, t=''):
        self._text = t

    def __str__(self):
        return self.text

    def __add__(self, other):
        return self.text + str(other)

    def __radd__(self, other):
        return str(other) + self.text

    @property
    def text(self):
        return str(self._text)


class H1(MarkDownElement):
    def __str__(self):
        return f'# {self.text}'


class H2(MarkDownElement):
    def __str__(self):
        return f'## {self.text}'


class H3(MarkDownElement):
    def __str__(self):
        return f'### {self.text}'


class H4(MarkDownElement):
    def __str__(self):
        return f'#### {self.text}'


class PlainText(MarkDownElement):
    def __str__(self):
        return self.text


class BlankLine(MarkDownElement):
    pass


class Table(MarkDownElement):
    def __init__(self, headers):
        self._headers = tuple(str(h) for h in headers)
        self._entries = []

    def add_entry(self, entry):
        if len(entry) != len(self._headers):
            raise RuntimeError('Number of element per entry should match that of the header')

        self._entries.append(tuple([str(e) for e in entry]))

    def __str__(self):
        def columns(seq, char='|'):
            return f'{char}{char.join(seq)}{char}'

        widths = [len(h) for h in self._headers]

        for entry in self._entries:
            for i, z in enumerate(zip(widths, entry)):
                w, e = z
                widths[i] = max(w, len(e))

        header = []
        for i, h in enumerate(self._headers):
            header.append(self._headers[i].center(widths[i] + 2))

        header = columns(header)
        divider = columns(['-' * (i + 2) for i in widths])
        entries = []

        for entry in self._entries:
            e = [f' {i[1].ljust(i[0])} ' for i in zip(widths, entry)]
            entries.append(columns(e))

        result = []
        result.append(header)
        result.append(divider)
        result+=entries
        result = '\n'.join(result)

        return result
