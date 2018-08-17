__version__ = '0.1.0'

from . import generators
from . import parser


def generate(source, uri='', language='python'):
    generator = generators.factory(language)

    return generator.generate(parser.parse(uri, source))
