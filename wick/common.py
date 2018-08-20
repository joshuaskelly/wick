import os
import re

from collections import namedtuple

Property = namedtuple('Property', ['name', 'type', 'description'])
Struct = namedtuple('Struct', ['name', 'description', 'properties'])


def _expand_type(symbol):
    t = symbol.type.value

    if hasattr(symbol, 'dimension'):
        t = f'{t}[{symbol.dimension.value}]'

    return t


def _sanitize_comment(text):
    """Remove comment syntax from comment text.

    Args:
        text: The raw comment text

    Returns:
        The cleaned up comment text
    """

    is_multiline_comment = text.startswith('/*')

    # Remove C style comments
    text = re.sub('(\/\*|\*\/|\/\/)', '', text)

    # Remove leading asterisks in multiline comments.
    if is_multiline_comment:
        lines = text.split('\n')
        lines = [line.lstrip(' *') for line in lines]
        text = '\n'.join(lines)

    # Clean up whitespace
    text = text.strip()

    return text


def _get_comment(comments, symbol):
    """Get the nearest comment for the given symbol.

    Args:
        comments: The ParseTree comments to consider

        symbol: The symbol to find a comment for

    Returns:
        The text of the comment as a string
    """

    # Grab all symbols in current scope
    symbols = [s for s in symbol.scope.definitions.values()]

    # Grab symbols in the inner scope if the symbol is a struct
    if hasattr(symbol, 'inner_scope') and symbol.type.value == 'struct':
        symbols += [s for s in symbol.inner_scope.definitions.values()]

    # Only consider name symbols
    symbols = [s for s in symbols if s.arity == 'name' and s != symbol]

    symbols_on_line_above = [s for s in symbols if s.range.end.line == symbol.range.start.line - 1]

    for comment in comments:
        # Comments are in line number order
        if comment.range.end.line > symbol.range.end.line:
            break

        # Prefer comments immediately above a symbol, unless there is
        # another symbol immediately above.
        if comment.range.end.line == symbol.range.start.line - 1 and not symbols_on_line_above:
            return _sanitize_comment(comment.value)

        # Also consider comments on the same line as the symbol
        if comment.range.start.line == symbol.range.start.line:
            return _sanitize_comment(comment.value)

    return ''


class Program:
    """
    Attributes:
        uri: An optional string uri for the source file

        structs: A sequence of Struct objects
    """

    def __init__(self, uri, parse_tree):
        """Constructor

        Args:
            uri: The source document uri

            parse_tree: The ParseTree object to process
        """
        self.uri = uri
        self.name = os.path.basename(uri).split('.')[0]
        self.structs = []

        # Only consider symbols that are structs and not struct aliases
        struct_symbols = [d for d in parse_tree.scope.definitions.values() if hasattr(d, 'type') and d.type.value == 'struct' and not hasattr(d, 'is_alias')]

        for symbol in struct_symbols:
            # Only consider named symbols (variables)
            variable_symbols = [d for d in symbol.inner_scope.definitions.values() if d.arity == 'name']
            properties = [Property(v.value, _expand_type(v), _get_comment(parse_tree.comments, v)) for v in variable_symbols]

            struct = Struct(
                name=symbol.value,
                description=_get_comment(parse_tree.comments, symbol),
                properties=properties
            )

            self.structs.append(struct)
