from collections import namedtuple
from . import document


Generator = namedtuple('Generator', ['generate'])


def get_generator(language):
    if language.lower() == 'markdown':
        return Generator(generate=generate)


def generate(program):
    """Generate Markdown text

    Args:
        program: A Program object to generate text for

    Returns:
        The Markdown text
    """

    return document.generate_source(program)
