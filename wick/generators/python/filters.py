import math
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


def format_string(members):
    result = ''

    for prop in members:
        type = prop.type

        if type == 'char' and prop.length > 1:
            format = f'{prop.length}s'
            result += format

        else:
            format = {
                'char': 'c',
                'signed char': 'b',
                'unsigned char': 'B',
                'short': 'h',
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


value_generators = {}


def test_data(member):
    global value_generators

    if member.type == 'char' and member.length > 1:
        test_characters = bytes(range(32, 127)).decode("ascii")
        count = math.ceil(member.length / len(test_characters))
        test_characters = test_characters * count
        return f'"""{test_characters[:member.length]}"""'

    try:
        value_generator = value_generators.get(member.type)

        return next(value_generator)

    except TypeError:
        interesting_values = {
            'char': [bytes([i]) for i in range(128)],
            'signed char': [-128, 0, 127],
            'unsigned char': [0, 255],
            'short': [-32768, 0, 32767],
            'unsigned short': [0, 65535],
            'int': [-2147483648, 0, 2147483647],
            'unsigned int': [0, 4294967295],
            'long': [-2147483648, 0, 2147483647],
            'unsigned long': [0, 4294967295],
            'long long': [-9223372036854775808, 0, 9223372036854775807],
            'unsigned long long': [0, 18446744073709551615],
            'ssize_t': [0],
            'size_t': [0],
            'float': [-1.0, 0.0, 1.0],
            'double': [-1.0, 0.0, 1.0]
        }[member.type]

        def value_generator():
            i = 0
            while True:
                yield interesting_values[i]
                i = (i + 1) % len(interesting_values)

        value_generators[member.type] = value_generator()

        return next(value_generators[member.type])