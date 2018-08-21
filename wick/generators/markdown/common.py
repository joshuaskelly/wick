def get_type_string(data_member):
    if data_member.length > 1:
        return f'{data_member.type}[{data_member.length}]'

    return data_member.type


def to_hex(value, width=4):
    width = max(width, 4)
    result = format(value, f'#0{width}X')
    return 'x'.join(result.split('X'))
