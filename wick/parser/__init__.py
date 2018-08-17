from wick.common import Program
from . import parser


def parse(uri, source):
    parse_tree = parser.parse(source)
    program = Program(uri, parse_tree)

    return program
