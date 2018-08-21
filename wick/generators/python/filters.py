import re

from collections import namedtuple


def snake_case(text):
    """Returns text converted to snake_case"""

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def pascal_case(text):
    """Returns text converted to PascalCase"""

    s1 = text.split('_')
    return ''.join([s.lower().capitalize() for s in s1])


def spaces(text):
    """Returns whitespace equal to the length of the given text.

    This is useful for making things line up.
    """

    return ' ' * len(text)


def format_string(properties):
    result = ''

    for prop in properties:
        type = prop.type

        if type.startswith('string'):
            dimension = type[6:]
            format = f'{dimension}s'

        else:
            format = {
                'char': 'c',
                'signed char': 'b',
                'unsigned char': 'B',
                'unsigned short': 'H',
                'int': 'i',
                'unsigned int': 'I',
                'long': 'l',
                'unsigned long': 'L',
                'long long': 'q',
                'unsigned long long': 'Q',
                'ssize_t': 'n',
                'size_t': 'N',
                'float': 'f',
                'double': 'd'
            }[type]

        result += format * prop.length

    return simplify_format_string(result)


RepeatedChar = namedtuple('RepeatedChar', ['count', 'char'])


def simplify_format_string(input):
    if not input:
        return ''

    pairs = [RepeatedChar(1, input[0])]

    for c in input[1:]:
        repeat = pairs[-1]
        if c == repeat.char and c != 's':
            pairs[-1] = RepeatedChar(repeat.count + 1, repeat.char)
        else:
            pairs.append(RepeatedChar(1, c))

    return ''.join(f'{p.count if p.count > 1 else ""}{p.char}' for p in pairs)
