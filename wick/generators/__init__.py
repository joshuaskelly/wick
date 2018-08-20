from . import python
from . import markdown

_language_modules = [
    markdown,
    python
]


class factory:
    def get(language):
        """Get a generator for the given language

        Args:
            language: A language name

        Returns:
            A Python module
        """

        for module in _language_modules:
            generator = module.get_generator(language)

            if generator:
                return generator
