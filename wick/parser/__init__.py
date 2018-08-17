from wick.common import Program
from . import parser


def parse(uri, source):
    """Parses the given source text

    Args:
        uri: The file URI for the source text.

        source: C source text that only contains structs with simple types.

    Returns:
        A Program
    """

    parse_tree = parser.parse(source)
    program = Program(uri, parse_tree)

    return program
