import sys

from . import csharp
from . import markdown
from . import python
from . import template

_language_modules = [
    csharp,
    markdown,
    python
]


class factory:
    @staticmethod
    def from_language(language):
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

        print(f'Unsupported languge: "{language}"', file=sys.stderr)

    @staticmethod
    def from_template(template_string, filters):
        return template.get_generator(template_string, filters)