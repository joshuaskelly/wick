def pascal_case(text):
    """Returns text converted to PascalCase"""

    s1 = text.split('_')
    return ''.join([s.lower().capitalize() for s in s1])


def integral_type(member):
    type = {
        'char': 'char',
        'signed char': 'sbyte',
        'unsigned char': 'byte',
        'short': 'short',
        'unsigned short': 'ushort',
        'int': 'int',
        'unsigned int': 'uint',
        'long': 'int',
        'unsigned long': 'uint',
        'long long': 'long',
        'unsigned long long': 'ulong',
        'float': 'float',
        'double': 'double'
    }[member.type]

    return type


def csharp_type(member, show_length=False):
    if member.type == 'char' and member.length > 1:
        return 'string'

    type = integral_type(member)

    if member.length > 1:
        return f'{type}[{member.length if show_length else ""}]'

    return type


def reader_method(member):
    type = integral_type(member)

    method = {
        'char': 'ReadChar',
        'sbyte': 'ReadSByte',
        'byte': 'ReadByte',
        'short': 'ReadInt16',
        'ushort': 'ReadUInt16',
        'int': 'ReadInt32',
        'uint': 'ReadUInt32',
        'long': 'ReadInt64',
        'ulong': 'ReadUInt64',
        'float': 'ReadSingle',
        'double': 'ReadDouble'
    }[type]

    return method


filters = {
    'pascalcase': pascal_case,
    'csharptype': csharp_type,
    'readermethod': reader_method
}
