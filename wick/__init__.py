__version__ = '0.0.1'

from . import generators
from .generators import python as generator
from . import parse


def generate(source, language='python'):
    print(generator.generate(parse.parse(source)))
