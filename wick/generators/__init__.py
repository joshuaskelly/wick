from . import python
from . import markdown


def factory(language):
    if language.lower() == 'python':
        return python

    if language.lower() == 'markdown':
        return markdown