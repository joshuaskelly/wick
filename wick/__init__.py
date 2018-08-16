__version__ = '0.0.1'

from . import generators
from . import parse


def generate(source, language='markdown'):
    generator = generators.factory(language)
    print(generator.generate(parse.parse(source)))
