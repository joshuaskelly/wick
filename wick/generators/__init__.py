from . import python
from . import markdown
from . import template

_language_modules = [
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

    @staticmethod
    def from_template(template_string):
        return template.get_generator(template_string)