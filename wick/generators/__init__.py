import sys

from . import csharp
from . import javascript
from . import markdown
from . import python
from . import template

_language_modules = [
    csharp,
    javascript,
    markdown,
    python
]


def is_valid_language(language):
    for module in _language_modules:
        if module.is_valid_language(language):
            return True

    return False


class factory:
    @staticmethod
    def from_language(language):
        """Get a generator for the given language

        Args:
            language: A language name

        Returns:
            A Python module
        """

        if not is_valid_language(language):
            print(f'Unsupported languge: "{language}"', file=sys.stderr)
            sys.exit(1)

        for module in _language_modules:
            generator = module.get_generator(language)

            if generator:
                return generator

    @staticmethod
    def from_template(template_string, filters):
        return template.get_generator(template_string, filters)