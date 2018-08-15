from . import python as python


def factory(language):
    if language.lower() == 'python':
        return python