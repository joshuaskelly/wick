import re

from collections import namedtuple
from types import SimpleNamespace

from . import parser

Property = namedtuple('Property', ['name', 'type', 'description'])


def dict_to_ns(d):
    return SimpleNamespace(
        name=d['name'],
        description=d['description'],
        properties=[Property(p['name'], p['type'], p['description']) for p in d['properties']]
    )

def expand_type(symbol):
    t = symbol.type.value

    if hasattr(symbol, 'dimension'):
        t = f'{t}[{symbol.dimension.value}]'

    return t

def program_to_ns(program):
    def get_comment(symbol):
        def sanitize_comment(text):
            is_multiline_comment = text.startswith('/*')

            # Remove C style comments
            text = re.sub('(\/\*|\*\/|\/\/)', '', text)

            # Remove leading asterisks in multiline comments.
            if is_multiline_comment:
                lines = text.split('\n')
                lines = [line.lstrip(' *') for line in lines]
                text = '\n'.join(lines)

            # Clean up whitespace
            text = text.lstrip()
            text = text.rstrip()

            return text

        # Grab all symbols in current scope
        symbols = [s for s in symbol.scope.definitions.values()]

        # Grab symbols in the inner scope if the symbol is a struct
        if hasattr(symbol, 'inner_scope') and symbol.type.value == 'struct':
            symbols += [s for s in symbol.inner_scope.definitions.values()]

        # Only consider name symbols
        symbols = [s for s in symbols if s.arity == 'name' and s != symbol]

        symbols_on_line_above = [s for s in symbols if s.range.end.line == symbol.range.start.line - 1]

        for comment in program.comments:
            # Comments are in line number order
            if comment.range.end.line > symbol.range.end.line:
                break

            # Prefer comments immediately above a symbol, unless there is
            # another symbol immediately above.
            if comment.range.end.line == symbol.range.start.line - 1 and not symbols_on_line_above:
                return sanitize_comment(comment.value)

            # Also consider comments on the same line as the symbol
            if comment.range.start.line == symbol.range.start.line:
                return sanitize_comment(comment.value)

        return ''

    result = []
    struct_symbols = [d for d in program.scope.definitions.values() if hasattr(d, 'type') and d.type.value == 'struct' and not hasattr(d, 'is_alias')]

    for struct_symbol in struct_symbols:
        variable_symbols = [d for d in struct_symbol.inner_scope.definitions.values() if d.arity == 'name']
        properties = [Property(v.value, expand_type(v), get_comment(v)) for v in variable_symbols]

        ns = SimpleNamespace(
            name = struct_symbol.value,
            description = get_comment(struct_symbol),
            properties = properties
        )

        result.append(ns)

    return result


def parse(source):
    program = parser.parse(source)
    return program_to_ns(program)