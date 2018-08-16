import struct

type_to_format_char = {
    'pad byte': 'x',
    'char': 'c',
    'signed char': 'b',
    'unsigned char': 'B',
    'bool': '?',
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
    'double': 'd',
    'char[]': 's'
}


def get_type(type):
    if '[' in type:
        return type.split('[')[0]

    return type


def get_dimension(type):
    if '[' in type:
        return int(type[:-1].split('[')[1])

    return 1


def get_size(type):
    format_char = type_to_format_char.get(get_type(type))

    if not format_char:
        return 0

    format = f'<{get_dimension(type)}{format_char}'

    return struct.calcsize(format)


def to_hex(value, width=4):
    width = max(width, 4)
    result = format(value, f'#0{width}X')
    return 'x'.join(result.split('X'))
