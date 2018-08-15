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


def program_to_ns(program):
    def get_comment(symbol):
        def sanitize_comment(text):
            # Remove C style comments
            text = re.sub('(\/\*|\*\/|\/\/)', '', text)

            # Clean up leading whitespace
            text = text.lstrip()

            return text

        for comment in program.comments:
            # Comments are in line number order
            if comment.range.end.line > symbol.range.end.line:
                break

            # Prefer comments immediately above a symbol
            if comment.range.end.line == symbol.range.start.line - 1:
                return sanitize_comment(comment.value)

            # Also consider comments on the same line as the symbol
            if comment.range.start.line == symbol.range.start.line:
                return sanitize_comment(comment.value)

        return ''

    result = []
    struct_symbols = [d for d in program.scope.definitions.values() if hasattr(d, 'type') and d.type.value == 'struct']

    for struct_symbol in struct_symbols:
        variable_symbols = [d for d in struct_symbol.inner_scope.definitions.values() if d.arity == 'name']
        properties = [Property(v.value, v.type.value, get_comment(v)) for v in variable_symbols]

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