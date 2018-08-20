__version__ = '0.4.0'

from . import generators
from . import parser


def generate(source, uri='', language='python'):
    """For the given C struct source code, generate source code to read and
    write that data in the given languge.

    Args:
        source: C source text that only contains structs with simple types.

        uri: An optional file URI for the source text.

        language: The desired language to generate code for.

    Returns:
        The generated source text
    """

    generator = generators.factory.get(language)

    return generator.generate(parser.parse(uri, source))
