from . import python
from . import markdown


def factory(language):
    """Get a generator for the given language

    Args:
        language: A language name

    Returns:
        A Python module
    """

    if language.lower() == 'python':
        return python

    if language.lower() == 'markdown':
        return markdown