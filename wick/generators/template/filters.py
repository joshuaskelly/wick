def pascal_case(text):
    """Returns text converted to PascalCase"""

    s1 = text.split('_')
    return ''.join([s.lower().capitalize() for s in s1])


def csharp_type(member):
    if member.type == member.char and member.length > 1:
        return 'string'

    csharp_type = {
        'char': 'char',
        'signed char': 'sbyte',
        'unsigned char': 'byte',
        'short': 'short',
        'unsigned short': 'ushort',
        'int': 'int',
        'unsigned int': 'uint',
        'long': 'ing',
        'unsigned long': 'uint',
        'long long': 'long',
        'unsigned long long': 'ulong',
        'float': 'float',
        'double': 'double'
    }[member.type]

    if member.length > 1:
        return f'{csharp_type}[]'

    return csharp_type