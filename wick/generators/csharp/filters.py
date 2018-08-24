def pascal_case(text):
    """Returns text converted to PascalCase"""
    if text.count('_') == 0:
        return text

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


def lines(text):
    ls = text.split('\n')

    if not ls:
        return []

    if ls[0].strip() == '':
        ls = ls[1:]
    
    if not ls:
        return []

    if ls[-1].strip() == '':
        ls = ls[:-1]

    return ls


def leading_spaces(text):
    return len(text) - len(text.lstrip())


def remove_miniumum_whitespace(lines):
    try:
        minimum_whitespace = min([leading_spaces(l) for l in lines])
        return [l[minimum_whitespace:] for l in lines]
    
    except ValueError:
        return []


def xml_comment(text):
    ls = lines(text)
    ls = remove_miniumum_whitespace(ls)
    return '\n'.join([f'/// {l}' for l in ls])

def comment(text):
    if text.count('\n') == 0:
        return single_line_comment(text)

    return multi_line_comment(text)


def single_line_comment(text):
    ls = lines(text)
    ls = remove_miniumum_whitespace(ls)

    return '\n'.join([f'// {l}' for l in ls])


def multi_line_comment(text):
    ls = lines(text)
    ls = remove_miniumum_whitespace(ls)
    ls = [f' * {l}' for l in ls]
    ls.insert(0, '/*')
    ls.append(' */')

    return '\n'.join(ls)


filters = {
    'pascalcase': pascal_case,
    'csharptype': csharp_type,
    'readermethod': reader_method,
    'comment': comment,
    'singlelinecomment': single_line_comment,
    'multilinecomment': multi_line_comment,
    'xmlcomment': xml_comment
}
