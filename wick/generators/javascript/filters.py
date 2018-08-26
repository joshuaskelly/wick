def get_method(member):
    method = {
        'char': 'getInt8',
        'signed char': 'getInt8',
        'unsigned char': 'getUint8',
        'short': 'getInt16',
        'unsigned short': 'getUint16',
        'int': 'getInt32',
        'unsigned int': 'getUint32',
        'long': 'getInt32',
        'unsigned long': 'getUint32',
        'float': 'getFloat32',
        'double': 'getFloat64'
    }[member.type]
    return method


def set_method(member):
    method = {
        'char': 'setInt8',
        'signed char': 'setInt8',
        'unsigned char': 'setUint8',
        'short': 'setInt16',
        'unsigned short': 'setUint16',
        'int': 'setInt32',
        'unsigned int': 'setUint32',
        'long': 'setInt32',
        'unsigned long': 'setUint32',
        'float': 'setFloat32',
        'double': 'setFloat64'
    }[member.type]
    return method


def javascript_type(member):
    if member.length > 1:
        if member.type == 'char':
            return 'string'

        return 'number[]'

    return 'number'


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


def prepend_lines(text, prepend_string):
    ls = lines(text)
    ls = [prepend_string + l.lstrip() for l in ls]

    return '\n'.join(ls)


filters = {
    'getmethod': get_method,
    'setmethod': set_method,
    'comment': comment,
    'javascripttype': javascript_type,
    'prependlines': prepend_lines
}