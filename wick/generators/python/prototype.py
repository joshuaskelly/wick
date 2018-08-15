import re

from collections import namedtuple
from typing import List

TypeEntry = namedtuple('TypeEntry', ['format', 'c_type', 'python_type'])

entries = [
    TypeEntry('x', 'pad byte', ''),
    TypeEntry('c', 'char', 'byte'),
    TypeEntry('b', 'signed char',	'integer'),
    TypeEntry('B', 'unsigned char', 'integer'),
    TypeEntry('?', 'bool', 'bool'),
    TypeEntry('h', 'short', 'integer'),
    TypeEntry('H', 'unsigned short', 'integer'),
    TypeEntry('i', 'int', 'integer'),
    TypeEntry('I', 'unsigned int','integer'),
    TypeEntry('l', 'long', 'integer'),
    TypeEntry('L', 'unsigned long', 'integer'),
    TypeEntry('q', 'long long', 'integer'),
    TypeEntry('Q', 'unsigned long long', 'long'),
    TypeEntry('n', 'ssize_t', 'integer'),
    TypeEntry('N', 'size_t', 'integer'),
    TypeEntry('f', 'float', 'float	'),
    TypeEntry('d', 'double', 'float	'),
    TypeEntry('s', 'char[]', 'string')
]

t = {e.c_type:e for e in entries}

Property = namedtuple('Property', ['name', 'type', 'description'])


def indent(source, tab='    ', tab_stops=1):
    ws = tab * tab_stops
    lines = source.split('\n')
    return '\n'.join([ws + l for l in lines])


def snake_case(text):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# Templates
# Docstring
docstring_attributes_template = '    {name}: {description}'
docstring_template = """\"\"\"{description}

Attributes:
{attributes}
\"\"\""""

# Class Attributes
class_attributes_template = """format = {format}
size = struct.calcsize(format)"""

# Slots
slots_template = """slots = (
{attributes}
)"""

# Constructor
constructor_assignment_exprs_template = 'self.{attribute} = {attribute}'
constructor_template = """def __init__(self,
{constructor_args}):

{assignment_exprs}
"""

# Write method
pack_args_template = '{name}.{attribute},'
pack_template = '{name}_data = struct.pack(cls.format, \n{args})'
write_data_template = 'file.write({name}_data)'
write_template = """@classmethod
def write(cls, file, {name}):
{data}

{write}
"""

# Read method
read_template = """@classmethod
def read(cls, file):
    {name}_data = file.read(cls.size)
    {name}_struct = struct.unpack(cls.format, {name}_data)

    return {class_name}(*{name}_struct)"""

# Class
class_template = """class {name}:
{docstring}

{class_attributes}

{slots}

{constructor}

{write_method}

{read_method}
"""

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


def expand_properties(properties: List[Property]) -> List[Property]:
    result = []

    for prop in properties:
        if '[' in prop.type:
            type, dimension = prop.type[:-1].split('[')

            if type == 'char':
                n = Property(prop.name, f'string{dimension}', prop.description)
                result.append(n)

            else:
                for i in range(int(dimension)):
                    n = Property(f'{prop.name}_{i}', type, prop.description)
                    result.append(n)
        else:
            result.append(prop)

    return result


def get_format(properties: List[Property]) -> str:
    result = ''

    for p in properties:
        type = p.type

        if type.startswith('string'):
            dimension = type[6:]
            format = f'{dimension}s'

        else:
            format = t[type].format

        result += format

    return simplify_format_string(result)

def get_pack_args(d) -> str:
    pack_args = []

    struct_name = snake_case(d.name)

    for prop in d.properties:
        attr_name = prop.name
        arg = pack_args_template.format(name=struct_name, attribute=attr_name)

        if prop.type.startswith('string'):
            arg = f"{arg[:-1]}.encode('ascii'),"

        pack_args.append(arg)

    return '\n'.join(pack_args)

def get_constructor_assignment_exprs(d) -> str:
    result = []

    for prop in d.properties:
        expr = constructor_assignment_exprs_template.format(attribute=prop.name)

        if prop.type.startswith('string'):
            decode_string = " if not type({name}) == bytes else {name}.split(b'\\x00')[0].decode('ascii')".format(name=prop.name)
            expr += decode_string

        result.append(expr)

    return '\n'.join(result)

def generate_source(d):
    result = ['import struct']
    for class_source in d:
        source = generate_class_source(class_source)
        result.append(source)

    return '\n\n'.join(result)


def generate_class_source(d):
    d.properties = expand_properties(d.properties)

    # Docstring
    doc_attrs = '\n\n'.join([docstring_attributes_template.format(name=p.name, description=p.description) for p in d.properties])
    doc = docstring_template.format(description=d.description, attributes=doc_attrs)
    doc = indent(doc)

    # Class Attributes
    class_format = "'<{}'".format(get_format(d.properties))
    class_attrs = class_attributes_template.format(format=class_format)
    class_attrs = indent(class_attrs)

    # Slots
    slot_attrs = '\n'.join([f"'{p.name}'," for p in d.properties])
    slot_attrs = indent(slot_attrs[:-1])
    slots = indent(slots_template.format(attributes=slot_attrs))

    # Constructor
    constructor_args = ',\n'.join([p.name for p in d.properties])
    constructor_args = indent(constructor_args, tab=' ' * 13)
    assignment_exprs = get_constructor_assignment_exprs(d)
    assignment_exprs = indent(assignment_exprs)
    constructor = constructor_template.format(constructor_args=constructor_args, assignment_exprs=assignment_exprs)
    constructor = indent(constructor)

    # Write methods
    pack_args = get_pack_args(d)
    pack_args = pack_args[:-1]
    indent_amount = len(snake_case(d.name)) + 20
    pack_args = indent(pack_args, tab=' ' * indent_amount)
    pack = pack_template.format(name=snake_case(d.name), args=pack_args)
    pack = indent(pack)
    write = write_data_template.format(name=snake_case(d.name))
    write = indent(write)
    write_method = write_template.format(name=snake_case(d.name), data=pack, write=write)
    write_method = indent(write_method)

    # Read methods
    read_method = read_template.format(class_name=d.name, name=snake_case(d.name))
    read_method = indent(read_method)

    class_source = class_template.format(
        name=d.name,
        docstring=doc,
        class_attributes=class_attrs,
        slots=slots,
        constructor=constructor,
        write_method=write_method,
        read_method=read_method
    )

    return class_source
